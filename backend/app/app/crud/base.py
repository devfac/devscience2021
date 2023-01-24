from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db: Session, uuid: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.uuid == uuid).first()

    def get_multi(
            self, db: Session, limit: int = 100, skip: int = 0,
            order_by: str = "title", order: str = "ASC",
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .order_by(text(f"{order_by} {order}"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_count(
            self, db: Session
    ) -> List[ModelType]:
        return (
            db.query(self.model)
            .all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data and field is not  None:
                setattr(db_obj, field, update_data[field])
        print(jsonable_encoder(db_obj), update_data, obj_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def remove_uuid(self, db: Session, *, uuid: str) -> ModelType:
        obj = db.query(self.model).get(uuid)
        db.delete(obj)
        db.commit()
        return obj

    def dynamic_filter(self,db: Session, *,
                       limit: int = 100, skip: int = 0,
                       order_by: str = "title",
                       order: str = "ASC",
                       filter_condition: List
                       ) -> ModelType:
        """
        eq for ==
        lt for <
        ge for >
        in for _in
        like for like
        """
        __query = db.query(self.model)
        for raw in filter_condition:
            try:
                key, op, value = raw
            except ValueError:
                raise Exception(f'invalid filter {raw}')
            column = getattr(self.model, key, None)
            if not column:
                raise Exception(f'invalid filter column {key}')
            if op == 'in':
                if isinstance(value, list):
                    filt = column.in_(value)
                else:
                    filt = column.in_(value.split(','))
            else:
                try:
                    attr = list(filter(lambda e: hasattr(column, e % op), ['%s', '%s_', '__%s__']))[0] % op
                except IndexError:
                    raise Exception(f'invalid filter operator {op}')
                if value == 'null':
                    value = None
                filt = getattr(column, attr)(value)
            __query = __query.filter(filt)
        return( __query.order_by(text(f"{order_by} {order}"))
                        .offset(skip)
                        .limit(limit)
                        .all())
