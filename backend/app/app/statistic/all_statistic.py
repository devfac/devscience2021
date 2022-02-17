from datetime import date
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
    if etat != "M" and etat != "F" and etat != "Total":
        all_etudiant = crud.ancien_etudiant.get_for_stat(schemas,uuid_parcours,niveau,sexe,etat)
    elif etat == "M":
        all_etudiant = crud.ancien_etudiant.get_by_sexe_for_stat(schemas,uuid_parcours,niveau,"MASCULIN")

    elif etat == "F":
        all_etudiant = crud.ancien_etudiant.get_by_sexe_for_stat(schemas,uuid_parcours,niveau,"FEMININ")

    elif etat == "Total":
        all_etudiant = crud.ancien_etudiant.get_by_parcours_for_stat(schemas,uuid_parcours,niveau)

    return len(all_etudiant)
    


def get_by_params(all_niveau:Any, sexe:str, etat:str, age_:int )-> int:
    if etat == "R":
        etat = "Redoublant"
    elif etat =="T+":
        etat = "Triplant ou plus"
    elif etat == "N":
        etat = "Passant"
    now = date.today().year
    all_etudiant = []
    for etudiant in all_niveau:
        date_ = etudiant.date_naiss
        naiss = date_[0:4]
        age :int = int(now) - int(naiss)
        if sexe == "ENSEMBLE":
            if etat == "Total":
                if age_ == 15:
                    if  age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if  age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                        all_etudiant.append(etudiant)
                else:
                    if age == age_:
                        all_etudiant.append(etudiant)
            else:
                if age_ == 15:
                    if etudiant.etat == etat and age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if etudiant.etat == etat and age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                    if etudiant.etat == etat :
                        all_etudiant.append(etudiant)
                else:
                    if etudiant.etat == etat and age == age_:
                        all_etudiant.append(etudiant)
        else:
            if etat == "S/Tot":
                if age_ == 15:
                    if etudiant.sexe == sexe  and age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if etudiant.sexe == sexe and age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                    if etudiant.sexe == sexe :
                        all_etudiant.append(etudiant)
                else:
                    if etudiant.sexe == sexe  and age == age_:
                        all_etudiant.append(etudiant)
            else:
                if age_ == 15:
                    if etudiant.sexe == sexe and etudiant.etat == etat and age <= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 29:
                    if etudiant.sexe == sexe and etudiant.etat == etat and age >= age_:
                        all_etudiant.append(etudiant)
                elif age_ == 30:
                    if etudiant.sexe == sexe and etudiant.etat == etat :
                        all_etudiant.append(etudiant)
                else:
                    if etudiant.sexe == sexe and etudiant.etat == etat and age == age_:
                        all_etudiant.append(etudiant)
    return len(all_etudiant)
class PDF(FPDF):
    def add_title(pdf:FPDF, data:Any, type:str = "total"):

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

        tabulation: int  = 35
        ln:int = 1
        if type != "total":
            pdf.rect(195,47.5,5,3)
            pdf.rect(195,53.5,5,3)
            type_formation = "Type de Formation*:"
            cocher = "(Veuillez cochez)"
            type_1 = "Formation initial"
            type_2 = "Formation continue"
            anne_ = "Année d'etude :"
            anne_etude = f'{data["niveau"]} {data["parcours"]}'
            ln = 0
            tabulation = 10

        pdf.set_font("arial","B",12)
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

        if type !="total":
            pdf.cell(40,6,type_formation,0,ln)
            pdf.cell(0,6,type_1,0,1)


        if type !="total":
            pdf.cell(tabulation,6,"",0,0,"L")
            pdf.cell(30,6,anne_,0,ln)
            pdf.cell(65,6,anne_etude,0,ln)
            pdf.cell(38,6,cocher,0,ln)
            pdf.cell(0,6,type_2,0,1)

        else:
            pdf.cell(20,6,"",0,0,"L")
            pdf.cell(107,6,titre_1,0,0,"L")
            pdf.cell(0,6,anne_univ,0,ln)

        pdf.cell(15,10,"",0,1,"L")

    def create_all_statistic(data:Any, etudiant:Any, schemas:str):
        titre_stat = [{"name":'',"value":["Niveau","Parcours"]},{"name":"masculin","value":["N","R","T+"]},{"name":"feminin","value":["N","R","T+"]},
                      {"name":"ensemble","value":["M","F","Total"]}]
        
        niveau_ = ["L1","L2","L3","M1","M2","H"]
        
        width:int = 39
        height:int = 7

        pdf = PDF("P","mm","a4")
        pdf.add_page()
        PDF.add_title(pdf=pdf,data=data,type="total")
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

    def create_statistic_by_years(data:Any, all_niveau:Any, schemas:str):
        titre_stat = [{"name":'',"value":["Age"]},{"name":"masculin","value":["N","R","T+","S/Tot"]},{"name":"feminin","value":["N","R","T+","S/Tot"]},
                      {"name":"ensemble","value":["N","R","T+","Total"]}]
        
        width:int = 48
        height:int = 7

        pdf = PDF("P","mm","a4")

        niveau_ = ["L1","L2","L3","M1","M2","H"]
        for index, niveau in enumerate(all_niveau):
            data["niveau"] = niveau_[index]
            for index_3, parc in enumerate(niveau[niveau_[index]]):
                if len(parc["etudiants"]) != 0:
                    data["parcours"] = f'{parc["name"]}'
                    pdf.add_page()
                    PDF.add_title(pdf=pdf,data=data,type="age")
                    pdf.set_margin(9) 
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

                    for index in range(16):
                        for index_1, titre in enumerate(titre_stat):
                            for value in titre["value"]:
                                pdf.set_font("arial","BI",10)
                                response = get_by_params(parc["etudiants"],titre["name"].upper(),value,index+15)
                                if index == 0:
                                    if index_1 == 0:
                                        pdf.cell(width/(len(titre["value"])),height,"Moins de 16 ans",1,0,"C")
                                    else:
                                        pdf.cell(width/(len(titre["value"])),height,str(response),1,0,"C")
                                elif index == 14:
                                    if index_1 == 0:
                                        pdf.cell(width/(len(titre["value"])),height,"29+",1,0,"C")
                                    else:
                                        pdf.cell(width/(len(titre["value"])),height,str(response),1,0,"C")
                                elif index == 15:
                                    if index_1 == 0:
                                        pdf.cell(width/(len(titre["value"])),height,"Total",1,0,"C")
                                    else:
                                        pdf.cell(width/(len(titre["value"])),height,str(response),1,0,"C")
                                else:
                                    if index_1 == 0:
                                        pdf.cell(width/(len(titre["value"])),height,str(index+15),1,0,"C")
                                    else:
                                        pdf.cell(width/(len(titre["value"])),height,str(response),1,0,"C")

                        pdf.cell(0,height,"",0,1,"L")  


                    bas_1 = "*la plupart des filières sont des types de formation; initiale pour les étudiants à plein temps"
                    bas_2 = "On attend par formation continue celle qui est donnée aux travailleurs à temps partiels"
                    bas_3 = "N.B: Veuillez remplir séparement le canevas par filière, type de formation et année d' études"

                    pdf.cell(0,height,"",0,1,"L")  
                    pdf.cell(0,5,bas_1,0,1,"L")                    
                    pdf.cell(0,5,bas_2,0,1,"L")                      
                    pdf.cell(0,5,bas_3,0,1,"L")        

        pdf.output(f"files/statistic_by_years.pdf","F")
        return f"files/statistic_by_years.pdf"

