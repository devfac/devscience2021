from datetime import date
from typing import Any, List
from fpdf import FPDF
from app import crud
from sqlalchemy.orm import Session


def get_by_params( all_etudiant:any,  titre:str) -> int:
    etdiant = []
    if titre == "Ensemble" :
        return len(all_etudiant["L1"])
    else:
        for un_etudiant in all_etudiant["L1"]:
            if un_etudiant.bacc_serie == titre:
                etdiant.append(un_etudiant)
    return len(etdiant)

class PDF(FPDF):

    def add_title(pdf:FPDF, data:Any, niveau:str):

        pdf.add_font("alger","","Algerian.ttf",uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"

        pdf.add_font("alger","","Algerian.ttf",uni=True)

        pdf.image(image_univ,x=60,y=26,w=30, h=30)
        pdf.image(image_fac,x=210,y=26,w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTÉ DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"
        anne_etude = f"Année d'etude : {niveau}"
        titre = f"Renseignement sur le filiere et option au titre de l'année {data['annee']}"
        tabulation: int  = 80
        ln:int = 1

        
        pdf.set_font("arial","B",18)
        pdf.cell(15,20,"",0,1,"L")
        pdf.cell(0,10,titre4,0,1,"C")

        pdf.set_font("arial","B",16)
        pdf.cell(0,10,titre5,0,1,"C")

        pdf.cell(0,18,"",0,1,"C")

        pdf.cell(tabulation,6,"",0,0,"L")
        pdf.set_font("arial","BI",12)
        pdf.cell(34,6,localisation,0,0,"L")
        pdf.set_font("arial","I",12)
        pdf.cell(0,6,localisation_,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(tabulation,6,"",0,0,"L")
        pdf.cell(24,6,mention,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(70,6,mention_etudiant,0,ln)

        pdf.set_font("arial","BI",12)
        pdf.cell(tabulation,6,"",0,0,"L")
        pdf.cell(70,6,anne_etude,0,ln)

        pdf.set_font("arial","I",12)
        pdf.cell(tabulation,6,"",0,1,"L")
        pdf.cell(tabulation-15,6,"",0,0,"L")
        pdf.cell(60,6,titre,0,ln)

        pdf.cell(15,10,"",0,1,"L")

    def create_stat_bachelier(data:Any,all_etudiant, schemas:str, db: Session,uuid_mention:str):
        titre_stat = [{"name":"Nouveau Bachelier en : ",
            "value":["Serie A1","Serie A2","Serie C","Serie D","Technique \n Génie civile","Technique Industrielle","Technique Tertiaire",
            "Technique Agricole","Technologique","Autre","Ensemble"]}]
        
        width:int = 285
        height:int = 10

        niveau_ = ["L1","M1","M2"]
        pdf = PDF("L","mm","a4")
        pdf.add_page()
        PDF.add_title(pdf=pdf,data=data,niveau="L1")
        pdf.set_font("arial","BI",8)
        pdf.set_left_margin(5)
        for index,titre in enumerate(titre_stat):
            pdf.cell(width,height,f'{titre["name"]}{data["annee"]}',1,0,"C")
        pdf.cell(0,height,"",0,1,"L")

        for titre in titre_stat:
            for index, value in enumerate(titre["value"]):
                if index < 4 or index > 8:
                    pdf.cell((width/len(titre["value"]))-10,height,value,1,0,"C")
                elif index == 10:
                    pdf.cell((width/len(titre["value"])),height,value,1,0,"C")
                else:
                    pdf.cell((width/len(titre["value"]))+12,height,value,1,0,"C")
            pdf.cell(0,height,"",0,1,"L")

        for titre in titre_stat:
            for index, value in enumerate(titre["value"]):
                response = get_by_params(all_etudiant,value)
                if index < 4 or index > 8:
                    pdf.cell((width/len(titre["value"]))-10,height,str(response),1,0,"C")
                elif index == 10:
                    pdf.cell((width/len(titre["value"])),height,str(response),1,0,"")
                else:
                    pdf.cell((width/len(titre["value"]))+12,height,str(response),1,0,"C")
            pdf.cell(0,height,"",0,1,"L")
       
        bas_1 = "N.B: Veuillez remplir séparement le canevas par filière, type de formation et année d' études "

        pdf.set_font("arial","BI",12)
        pdf.cell(0,height,"",0,1,"L")  
        pdf.cell(0,5,bas_1,0,1,"L")  
           
        pdf.output(f"files/bachelier.pdf","F")
        return f"files/bachelier.pdf"

        