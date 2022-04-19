import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.sql.ddl import CreateSchema

from app.db.base import Base
from app import crud, schemas, models
from app.core.config import settings
from app.db import base  # noqa: F401
from app.db.session import engine

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
from app.utils import create_anne

Base.metadata.create_all(bind=engine)


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            first_name=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_admin=True,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
    anne_univ_in = schemas.AnneUnivCreate(**{"title": "2020-2021", "moyenne": 9.5})
    anne_univ = crud.anne_univ.get_by_title(db, title=anne_univ_in.title)
    if not anne_univ:
        anne_univ = crud.anne_univ.create(db=db, obj_in=anne_univ_in)
        try:
            schem_et = create_anne(anne_univ.title)
            engine.execute(CreateSchema(schem_et))
            models.etudiant.create(schem_et)
        except sqlalchemy.exc.ProgrammingError as e:
            print(e)
