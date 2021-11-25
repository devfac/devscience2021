from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql.base import UUID
import uuid
from sqlalchemy import MetaData, Table
from sqlalchemy.sql.sqltypes import Float
from app.db.session import engine
from sqlalchemy.engine.reflection import Inspector


def create_table_note(schemas, parcours, semestre, matiers) -> bool:
    try:
        base =  MetaData()
        # table notes
        note = Table(f"note_{semestre.lower()}_{parcours.lower()}",base,
            Column("num_carte",String, primary_key=True),
            schema=schemas
        )
        note.create(engine)
        for indexn,value_ue in enumerate(matiers):
            column_ue = Column(f"{value_ue}",Float)
            add_column(schemas=schemas,table_name=f"note_{semestre.lower()}_{parcours.lower()}",column=column_ue)
        return True
    except:
        return False
            

def drop_table_note(schemas, parcours, semestre):
        base =  MetaData(schema=schemas)
        # table notes
        note = Table(f"note_{semestre}_{parcours}",base,autoload=True
        )
        note.drop(engine)

        
def add_column(schemas, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {schemas}.{table_name} ADD COLUMN {column_name} {column_type}' )

   


"""
inspector = Inspector.from_engine(engine)
table_name in inpector.get_table_name()
"""