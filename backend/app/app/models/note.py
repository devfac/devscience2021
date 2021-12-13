
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import MetaData, Table
from sqlalchemy.sql.sqltypes import Float
from app.db.session import engine


def create_table_note(schemas, parcours, semestre,session ,matiers) -> bool:
   
    try:
        base =  MetaData()
        # table notes
        note = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}",base,
            Column("num_carte",String, primary_key=True),
            schema=schemas
        )
        note.create(engine)
        for index, value_ue in enumerate(matiers):
<<<<<<< HEAD
            column_matier = Column(f"{value_ue}",Float,default=0.0)
=======
            column_matier = Column(f"{value_ue}",Float)
>>>>>>> excel
            add_column(schemas=schemas,table_name=f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}",column=column_matier)
        column_moyenne = Column("moyenne",Float,default=0.0)
        add_column(schemas=schemas,table_name=f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}",column=column_moyenne)
        column_credit = Column("credit",Integer,default=0)
        add_column(schemas=schemas,table_name=f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}",column=column_credit)
<<<<<<< HEAD
=======
        return True
    except:
        return False

def update_table_note(schemas, parcours, semestre,session ,matiers) -> bool:
   
    try:
        for index, value_ue in enumerate(matiers):
            column_matier = Column(f"{value_ue}",Float)
            add_column(schemas=schemas,table_name=f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}",column=column_matier)
>>>>>>> excel
        return True
    except:
        return False
            

def drop_table_note(schemas, parcours,session, semestre) -> bool:
    try:
        base =  MetaData(schema=schemas, bind=engine)
        # table notes
        note = Table(f"note_{parcours.lower()}_{semestre.lower()}_{session.lower()}",base,autoload=True )
        note.drop(engine)
        return True
    except Exception as e:
        print("error:",e)
        return False

        
def add_column(schemas, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute(f'ALTER TABLE {schemas}.{table_name} ADD COLUMN {column_name} {column_type}' )

   


"""
inspector = Inspector.from_engine(engine)
table_name in inpector.get_table_name()
"""