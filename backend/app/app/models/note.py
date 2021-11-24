from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String, Float
from sqlalchemy.dialects.postgresql.base import UUID
import uuid
from sqlalchemy import MetaData, Table
from sqlalchemy.sql.sqltypes import Float
from app.db.session import engine
from sqlalchemy.engine.reflection import Inspector


def create_table_note(schemas, parcours, semestre, matiers):
        base =  MetaData()
        # table notes
        note = Table(f"note_{semestre}_{parcours}",base,
            Column("num_carte",String, primary_key=True),
            schema=schemas
        )
        note.create(engine)
        for value_ue in enumerate(matiers['ue']):
            column_ue = Column(f"ue_{value_ue['name']}",Float)
            add_column(schemas=schemas,table_name=f"note_{semestre}_{parcours}",column=column_ue)
            for value_ec in enumerate(value_ue['ec']):
                column_ec = Column(f"ec_{value_ec['name']}",Float)
                add_column(schemas=schemas,table_name=f"note_{semestre}e_{parcours}",column=column_ec)
            

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