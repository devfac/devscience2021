from typing import Any, List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import MetaData, Table, update, insert

from sqlalchemy import and_, or_
from app.crud.base import CRUDBase
from app.db.session import engine
from app.schemas.matier import MatierECUpdate, MatierECCreate, MatierEC


class CRUDNote(CRUDBase[MatierEC, MatierECCreate, MatierECUpdate]):

    def check_table_exist( self, semester: str, journey: str, session: str) -> bool:
        metadata = MetaData()
        metadata.reflect(bind=engine)
        for table in metadata.tables:
            table_name = table.replace('.', '')
            if table_name == f"note_{journey.lower()}_{semester.lower()}_{session.lower()}":
                return True
        return False

    def check_columns_exist(self, semester: str, journey: str, session: str) -> Optional[List[str]]:
        metadata = MetaData(bind=engine)
        columns = []
        table_ = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        for index, table in enumerate(table_.columns):
            if str(table).partition(".")[2] != 'num_carte' and str(table).partition(".")[2] != 'mean' \
                    and str(table).partition(".")[2] != 'credit':
                columns.append(str(table).partition(".")[2])
        return columns

    def insert_note(self, semester: str, journey: str, session: str, num_carte: str, year: str):
        obj_in_data = jsonable_encoder({"num_carte":num_carte, "year":year, "validation":False})
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        ins = insert(table=table)
        ins = ins.values(obj_in_data)
        conn.execute(ins)
        conn.close()

    def read_all_note(
            self,
            semester: str,
            journey: str,
            session: str,
            year:str,
            limit: int = 1000,
            skip: int = 0,
            value_ue: str = "",
            credit: str = "",
            mean: str = "",
            value: float = 10,
            value_ec: str = "",
            type_:str = "success"
        ):

        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        filter_ = [table.columns["year"] == year]
        if value_ue != "" and value_ue is not None and value_ue != "null" and value_ec != "" and value_ec is not None and value_ec != "null":
            filter_.append(and_(or_(table.columns[f'ec_{value_ec}'] < 10,table.columns[f'ec_{value_ec}'] is None),
                                table.columns[f'ue_{value_ue}'] < 10))
        else:
            if type_ == "success":
                if credit != "" and credit is not None and credit != "null":
                    filter_.append(or_(table.columns[credit] > value, table.columns[credit] == value))

                if mean != "" and mean is not None and mean != "null":
                    filter_.append(or_(table.columns[mean] > value, table.columns[mean] == value))

                if value_ue != "" and value_ue is not None and value_ue != "null":
                    filter_.append(or_(table.columns[f'ue_{value_ue}'] > 10, table.columns[f'ue_{value_ue}'] == 10))

                if value_ec != "" and value_ec is not None and value_ec != "null":
                    filter_.append(or_(table.columns[f'ec_{value_ec}'] > 10, table.columns[f'ec_{value_ec}'] == 10))
            else:
                if credit != "" and credit is not None and credit != "null":
                    filter_.append(or_(table.columns[credit] > value, table.columns[credit] is None))

                if mean != "" and mean is not None and mean != "null":
                    filter_.append(or_(table.columns[mean] < value, table.columns[credit] is None))

                if value_ue != "" and value_ue is not None and value_ue != "null":
                    filter_.append(or_(table.columns[f'ue_{value_ue}'] < 10, table.columns[f'ue_{value_ue}'] is None))

                if value_ec != "" and value_ec is not None and value_ec != "null":
                    filter_.append(or_(table.columns[f'ec_{value_ec}'] < 10, table.columns[f'ec_{value_ec}'] is None))
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(and_(*filter_))
        sel = sel.offset(skip)
        sel = sel.limit(limit)
        sel = sel.order_by(table.columns.num_carte.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def read_all_note_count(
            self,
            semester: str,
            journey: str,
            session: str,
            year:str,
            credit: str = "",
            mean: str = "",
            value: float = 10,
            value_ue: str = "",
            value_ec: str = "",
            type_:str = "success"):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        filter_ = [table.columns["year"] == year]
        if value_ue != "" and value_ue is not None and value_ue != "null" and value_ec != "" and value_ec is not None and value_ec != "null":
            filter_.append(and_(or_(table.columns[f'ec_{value_ec}'] < 10,table.columns[f'ec_{value_ec}'] is None),
                                table.columns[f'ue_{value_ue}'] < 10))

        else:
            if type_ == "success":
                if credit != "" and credit is not None and credit != "null":
                    filter_.append(or_(table.columns[credit] > value, table.columns[credit] == value))

                if mean != "" and mean is not None and mean != "null":
                    filter_.append(or_(table.columns[mean] > value, table.columns[mean] == value))

                if value_ue != "" and value_ue is not None and value_ue != "null":
                    filter_.append(or_(table.columns[f'ue_{value_ue}'] > 10, table.columns[f'ue_{value_ue}'] == 10))

                if value_ec != "" and value_ec is not None and value_ec != "null":
                    filter_.append(or_(table.columns[f'ec_{value_ec}'] > 10, table.columns[f'ec_{value_ec}'] == 10))
            else:
                if credit != "" and credit is not None and credit != "null":
                    filter_.append(or_(table.columns[credit] > value, table.columns[credit] is None))

                if mean != "" and mean is not None and mean != "null":
                    filter_.append(or_(table.columns[mean] < value, table.columns[credit] is None))

                if value_ue != "" and value_ue is not None and value_ue != "null":
                    filter_.append(or_(table.columns[f'ue_{value_ue}'] < 10, table.columns[f'ue_{value_ue}'] is None))

                if value_ec != "" and value_ec is not None and value_ec != "null":
                    filter_.append(or_(table.columns[f'ec_{value_ec}'] < 10, table.columns[f'ec_{value_ec}'] is None))

        conn = engine.connect()
        sel = table.select()
        sel = sel.where(and_(*filter_))
        sel = sel.order_by(table.columns.num_carte.asc())
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def read_note_succes(self, semester: str,
                         journey: str,
                         session: str,
                         year: str,
                         value_matier: str,
                         operator: str = ">=",
                         value: float = 10,
                         limit: int = 1000,
                         skip: int = 0):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT * FROM {table} WHERE {value_matier} {operator} {value} AND year = '{year}'")
        result = result.where(table.columns.year == year)
        result = result.offset(skip)
        result = result.limit(limit)
        out = result.fetchall()
        conn.close()
        return out


    def search_notes(self, semester: str,
                         journey: str,
                         session: str,
                         year: str,
                         num_carte: str,
                         limit: int = 1000,
                         skip: int = 0):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        sel = table.select()
        sel = sel.where(and_(table.columns["year"] == year, table.columns["num_carte"] == num_carte))
        sel = sel.order_by(table.columns.num_carte.asc())
        sel = sel.offset(skip)
        sel = sel.limit(limit)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_ue(self,semester: str, journey: str, session: str, list_ue: list, year: str):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte, {list_ue}, validation FROM {table} WHERE year = '{year}'")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_failed(self, semester: str,
                         journey: str,
                         session: str,
                         year: str,
                         value_matier: str,
                         operator: str = "<",
                         value: float = 10,
                         limit: int = 1000,
                         skip: int = 0):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT * FROM {table} WHERE {value_matier} {operator} {value}  OR {value_matier} IS NULL  AND year = '{year}'")
        result = result.offset(skip)
        result = result.limit(limit)
        out = result.fetchall()
        conn.close()
        return out

    def read_note_fails(self, semester: str,
                         journey: str,
                         session: str,
                         year: str,
                         value_ue: str,
                         value_ec: str,
                         operator: str = "<",
                         value: float = 10,
                         limit: int = 1000,
                         skip: int = 0):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT * FROM {table} WHERE ({value_ec} {operator} {value}  OR {value_ec} IS NULL) AND {value_ue} {operator} {value} AND year = '{year}'")
        result = result.offset(skip)
        result = result.limit(limit)
        out = result.fetchall()
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean_and_credit_equals(self, schema: str,
                                            semester: str,
                                            journey: str,
                                            session: str,
                                            mean: float,
                                            credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT num_carte,mean,credit FROM {table} WHERE mean >= {mean} and credit = {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean_and_credit_sup(self, schema: str, semester: str, journey: str, session: str,
                                            mean: float, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT num_carte,mean,credit FROM {table} WHERE mean >= {mean} and credit >= {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean_and_credit_inf(self, schema: str, semester: str, journey: str, session: str,
                                            mean: float, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(
            f"SELECT num_carte,mean,credit FROM {table} WHERE mean >= {mean} and credit <= {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_credit(self, schema: str, semester: str, journey: str, session: str, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte,credit FROM {table} WHERE credit = {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_credit_inf(self, schema: str, semester: str, journey: str, session: str, credit: int):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte,credit FROM {table} WHERE credit < {credit}")
        out = result.fetchall()
        conn.close()
        return out

    def read_note_by_mean(self, schema: str, semester: str, journey: str, session: str, mean: float):
        metadata = MetaData(schema=schema, bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        result = conn.execute(f"SELECT num_carte,mean FROM {table} WHERE mean >= {mean}")
        out = result.fetchall()
        conn.close()
        return out

    def update_note(self, semester: str, journey: str, session: str, num_carte: str, ue_in: Any):
        metadata = MetaData(bind=engine)
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        conn = engine.connect()
        up = update(table=table)
        up = up.values(ue_in)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)

    def read_by_num_carte(self, semester: str, journey: str, session: str, num_carte: str) -> Any:
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        sel = table.select()
        sel = sel.where(table.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out

    def update_auto(self, semester: str, journey: str, session: str, num_carte: str):
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        table_norm = Table(f"note_{journey.lower()}_{semester.lower()}_normal", metadata, autoload=True)
        sel = table_norm.select()
        sel = sel.where(table_norm.columns.num_carte == num_carte)
        result = conn.execute(sel)
        out = result.fetchone()
        up = table.update()
        up = up.values(out)
        up = up.where(table.columns.num_carte == num_carte)
        conn.execute(up)
        conn.close()

    def read_by_credit(self, semester: str, journey: str, session: str, credit: int, year:str) -> Any:
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        sel = table.select()
        sel = sel.where(table.columns.credit < credit)
        sel = sel.where(table.columns.year == year)
        result = conn.execute(sel)
        out = result.fetchall()
        conn.close()
        return out

    def delete_by_num_carte(self,semester: str, journey: str, session: str, num_carte: str):
        metadata = MetaData(bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        dele = table.delete()
        dele = dele.where(table.columns.num_carte == num_carte)
        conn.execute(dele)
        conn.close()

    def read_ue_mean(self, schema: str, semester: str, journey: str, session: str, num_carte: str,
                        obj_in: str) -> Any:
        metadata = MetaData(schema=schema, bind=engine)
        conn = engine.connect()
        table = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", metadata, autoload=True)
        sel = table.select()
        sel = sel.where(f"table.columns.{num_carte} == {num_carte}")
        result = conn.execute(sel)
        out = result.fetchone()
        conn.close()
        return out


note = CRUDNote(MatierEC)
