
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import MetaData, Table
from sqlalchemy.sql.sqltypes import Float
from app.db.session import engine


def create_table_note(schema, journey, semester,session ,matiers) -> bool:
   
    try:
        base =  MetaData()
        # table notes
        note = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}",base,
            Column("num_carte",String, primary_key=True),
            schema=schema
        )
        note.create(engine)
        for index, value_ue in enumerate(matiers):
            column_matier = Column(f"{value_ue}",Float)
            add_column(schema=schema,table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}",column=column_matier)
        column_moyenne = Column("moyenne",Float,default=0.0)
        add_column(schema=schema,table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}",column=column_moyenne)
        column_credit = Column("credit",Integer,default=0)
        add_column(schema=schema,table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}",column=column_credit)
        return True
    except Exception as e:
        print(e)
        return False

def update_table_note(schema, journey, semester,session ,matiers) -> bool:
   
    try:
        for index, value_ue in enumerate(matiers):
            column_matier = Column(f"{value_ue}",Float)
            add_column(schema=schema,table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}",column=column_matier)
        return True
    except:
        return False
            

def drop_table_note(schema, journey,session, semester) -> bool:
    try:
        base =  MetaData(schema=schema, bind=engine)
        # table notes
        note = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}",base,autoload=True )
        note.drop(engine)
        return True
    except Exception as e:
        print("error:",e)
        return False

        
def add_column(schema, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {schema}.{table_name} ADD COLUMN {column_name} {column_type}' )

   


"""
inspector = Inspector.from_engine(engine)
table_name in inpector.get_table_name()
"""