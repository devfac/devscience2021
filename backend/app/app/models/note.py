
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import MetaData, Table
from sqlalchemy.sql.sqltypes import Float
from app.db.session import engine


def create_table_note( journey, semester,session ,matiers) -> bool:
    try:
        base =  MetaData()
        # table note
        note = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}",base,
            Column("num_carte",String, primary_key=True),
        )
        note.create(engine)
        for index, value_ue in enumerate(matiers):
            column_ = Column(f"{value_ue}", Float)
            add_column(table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", column=column_)
        column_mean = Column("mean",Float,default=0.0)
        add_column(table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", column=column_mean)
        column_credit = Column("credit",Integer,default=0)
        add_column(table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", column=column_credit)
        column_year = Column("year",String)
        add_column(table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", column=column_year)
        return True
    except Exception as e:
        print(e)
        return False


def update_table_note(journey, semester,session ,column) -> bool:
    try:
        for index, on_column in enumerate(column):
            column_ = Column(f"{on_column}", Float)
            add_column(table_name=f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", column=column_)
        return True
    except Exception as e:
        print("error:",e)
        return False
            

def drop_table_note(journey,session, semester) -> bool:
    try:
        base =  MetaData(bind=engine)
        # table note
        note = Table(f"note_{journey.lower()}_{semester.lower()}_{session.lower()}", base, autoload=True )
        note.drop(engine)
        return True
    except Exception as e:
        print("error:",e)
        return False

        
def add_column(table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}' )

   


"""
inspector = Inspector.from_engine(engine)
table_name in inpector.get_table_name()
"""