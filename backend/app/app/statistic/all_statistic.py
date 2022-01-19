from typing import Any, List
from fpdf import FPDF
from app import crud

def get_nbr_etudiant(schemas:str,niveau:str, etat:str,sexe:str,uuid_parcours:str)-> str:
    if etat == 'N':
        etat = "Passant"
    elif etat == "R":
        etat = "Redoublant"
    elif etat == "T+":
        etat = "Triplant ou plus"

    if niveau == "L1":
        niveau = "S2"
    elif niveau == "L2":
        niveau = "S4"
    elif niveau == "L3":
        niveau = "S6"
    elif niveau == "M1":
        niveau = "S8"
    else:
        niveau = "S10"

    all_etudiant = []
    print(etat)
    if etat != "M" and etat != "F" and etat != "Total":
        all_etudiant = crud.ancien_etudiant.get_for_stat(schemas,uuid_parcours,niveau,sexe,etat)
    elif etat == "M":
        all_etudiant = crud.ancien_etudiant.get_by_sexe_for_stat(schemas,uuid_parcours,niveau,"MASCULIN")

    elif etat == "F":
        all_etudiant = crud.ancien_etudiant.get_by_sexe_for_stat(schemas,uuid_parcours,niveau,"FEMININ")

    elif etat == "Total":
        all_etudiant = crud.ancien_etudiant.get_by_parcours_for_stat(schemas,uuid_parcours,niveau)
        print(len(all_etudiant))

    return len(all_etudiant)


class PDF(FPDF):
    def add_title(pdf:FPDF, data:Any):

        pdf.add_font("alger","","Algerian.ttf",uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"


        pdf.add_font("alger","","Algerian.ttf",uni=True)

        pdf.image(image_univ,x=30,y=6,w=30, h=30)
        pdf.image(image_fac,x=155,y=6,w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTE DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"
        titre_1 = "Etudiants inscritent par filiere et option au titre de l'année"
        anne_univ = f"{data['anne']}"

        pdf.set_font("arial","B",12)
        pdf.cell(0,6,titre4,0,1,"C")

        pdf.set_font("arial","B",10)
        pdf.cell(0,6,titre5,0,1,"C")

        pdf.cell(0,18,"",0,1,"C")

        pdf.set_font("arial","BI",12)
        pdf.cell(35,6,"",0,0,"L")
        pdf.cell(24,6,mention,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,6,mention_etudiant,0,1)

        pdf.cell(35,6,"",0,0,"L")
        pdf.set_font("arial","BI",12)
        pdf.cell(34,6,localisation,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,6,localisation_,0,1)

        pdf.cell(20,6,"",0,0,"L")
        pdf.cell(107,6,titre_1,0,0,"L")
        pdf.cell(0,6,anne_univ,0,1)

        pdf.cell(15,10,"",0,1,"L")

    def create_all_statistic(data:Any, etudiant:Any, schemas:str):
        titre_stat = [{"name":'',"value":["Niveau","Parcours"]},{"name":"masculin","value":["N","R","T+"]},{"name":"feminin","value":["N","R","T+"]},
                      {"name":"ensemble","value":["M","F","Total"]}]
        
        niveau_ = ["L1","L2","L3","M1","M2","H"]
        
        width:int = 39
        height:int = 7

        pdf = PDF("P","mm","a4")
        pdf.add_page()
        PDF.add_title(pdf=pdf,data=data)
        pdf.set_margin(20) 
        for titre in titre_stat:
            if titre["name"] != '':
                pdf.set_font("arial","BI",10)
                pdf.cell(width,height,titre["name"].upper(),1,0,"C")
            else:
                pdf.cell(width,height,"",0,0,"C")
        pdf.cell(0,height,"",0,1,"L")

        for titre in titre_stat:
            for value in titre["value"]:
                pdf.set_font("arial","BI",10)
                pdf.cell(width/(len(titre["value"])),height,value,1,0,"C")
        pdf.cell(0,height,"",0,1,"L")        


        pdf.cell(0,1,"",0,1,"L")   
        for index, parcours in enumerate(etudiant):
            for index_1, titre in enumerate(titre_stat):
                for index_2, value in enumerate(titre["value"]):
                    if index_1 == 0 :
                        if index_2 == 0:
                            if index == len(etudiant) -1:
                                pdf.cell(width/(len(titre["value"])),height*len(parcours[niveau_[index]]),"",1,0,"C")
                            else:
                                pdf.cell(width/(len(titre["value"])),height*len(parcours[niveau_[index]]),niveau_[index],1,0,"C")
                        elif index_2 == 1:
                            for index_3, parc in enumerate(parcours[niveau_[index]]):
                                if index_3 == 0:
                                    pdf.cell(width/(len(titre["value"])),height,parc["name"],1,0,"C")
                                    for index_4, titre_1 in enumerate(titre_stat):
                                        if index_4 != 0:
                                            for value in titre_1["value"]:
                                                pdf.set_font("arial","BI",10)
                                                if index == len(etudiant) -1:
                                                    pdf.cell(width/(len(titre_1["value"])),height,str(0),1,0,"C")
                                                else:
                                                    value_stat = get_nbr_etudiant(schemas,niveau_[index],value,titre_1["name"].upper(),str(parc["uuid"]))
                                                    pdf.cell(width/(len(titre_1["value"])),height,str(value_stat),1,0,"C")
                                    pdf.cell(0,height,"",0,1,"L")        
                                else:
                                    pdf.cell(width/(len(titre["value"])),height,'',0,0,"C")
                                    pdf.cell(width/(len(titre["value"])),height,parc["name"],1,0,"C")
                                    for index_4, titre_1 in enumerate(titre_stat):
                                        if index_4 != 0:
                                            for value in titre_1["value"]:
                                                pdf.set_font("arial","BI",10)
                                                if index == len(etudiant) -1:
                                                    pdf.cell(width/(len(titre_1["value"])),height,str(0),1,0,"C")
                                                else:
                                                    value_stat = get_nbr_etudiant(schemas,niveau_[index],value,titre_1["name"].upper(),str(parc["uuid"]))
                                                    pdf.cell(width/(len(titre_1["value"])),height,str(value_stat),1,0,"C")
                                    pdf.cell(0,height,"",0,1,"L")             
            pdf.cell(0,1,"",0,1,"L")        
        bas_1 = "N: Nouveau, R: Redoublant, T+: Triplant et plus"
        bas_2 = "Veuillez remplir séparement le canevas par filière, type de formation et année des études"

        pdf.cell(0,5,bas_1,0,1,"L")                    
        pdf.cell(0,5,bas_2,0,1,"L")        


        


        pdf.output(f"files/statistic_total.pdf","F")
        return f"files/statistic_total.pdf"

