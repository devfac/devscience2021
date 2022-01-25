from datetime import date
from typing import Any, List
from fpdf import FPDF
from app import crud


def get_by_params(sexe:str, all_etudiant:any,  diplome:str) -> int:
    
    stat_etudiant = []
    for etudiant in all_etudiant:
        if sexe == "Total":
            if etudiant["diplome"] == diplome:
                stat_etudiant.append(etudiant)
            
        if sexe == "Total" and diplome == "Total":
            stat_etudiant.append(etudiant)
        if diplome == "Total":
            if etudiant["info"].sexe == sexe:
                stat_etudiant.append(etudiant)
        else:
            if etudiant["info"].sexe == sexe and etudiant["diplome"] == diplome:
                stat_etudiant.append(etudiant)
    return len(stat_etudiant)

class PDF(FPDF):


    def add_title(pdf:FPDF, data:Any):

        pdf.add_font("alger","","Algerian.ttf",uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"


        pdf.add_font("alger","","Algerian.ttf",uni=True)

        pdf.image(image_univ,x=30,y=26,w=30, h=30)
        pdf.image(image_fac,x=155,y=26,w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTE DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"

        tabulation: int  = 35
        ln:int = 1

        
        pdf.set_font("arial","B",12)
        pdf.cell(15,20,"",0,1,"L")
        pdf.cell(0,6,titre4,0,1,"C")

        pdf.set_font("arial","B",10)
        pdf.cell(0,6,titre5,0,1,"C")

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

        pdf.cell(15,10,"",0,1,"L")

    def create_statistic_by_diplome(data:Any,all_etudiant, schemas:str):
        titre_stat = [{"name":'Sexe',"value":["Sexe"]},{"name":"Diplome","value":["Licence","Master"]},{"name":"Total","value":["Total"]}]
        
        width:int = 50
        height:int = 10

        pdf = PDF("P","mm","a4")

        sexe_ = ["MASCULIN","FEMININ","Total"]
        pdf.add_page()
        PDF.add_title(pdf=pdf,data=data)
        pdf.set_margin(30) 
        pdf.set_font("arial","BI",10)
        for titre in titre_stat:
            if titre["name"] == "Sexe" or titre["name"] == "Total":
                pdf.cell(width,height*2,titre["name"],1,0,"C")
            else:
                pdf.cell(width,height,titre["name"],1,0,"C")
        pdf.cell(0,height,"",0,1,"L")

        for titre in titre_stat:
            for value in titre["value"]:
                if titre["name"] == "Sexe" or titre["name"] == "Total":
                    pdf.cell(width/(len(titre["value"])),height,"",0,0,"C")
                else:
                    pdf.cell(width/(len(titre["value"])),height,value,1,0,"C")
        pdf.cell(0,height,"",0,1,"L")      

        for sexe in sexe_:
            for index_1, titre in enumerate(titre_stat):
                for value in titre["value"]:
                    pdf.set_font("arial","BI",10)
                    response = get_by_params(sexe,all_etudiant,value)
                    if index_1 == 0:
                        pdf.cell(width/(len(titre["value"])),height,sexe,1,0,"C")
                    else:
                        pdf.cell(width/(len(titre["value"])),height,str(response),1,0,"C")
                       

            pdf.cell(0,height,"",0,1,"L")  
           
        pdf.output(f"files/statistic_by_diplome.pdf","F")
        return f"files/statistic_by_diplome.pdf"

        