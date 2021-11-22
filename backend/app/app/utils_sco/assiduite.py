import random
from typing import Any
from fpdf import FPDF
import unidecode

def create_certificat_assidute( num_carte:str, num: int, date: str, rentre_univ:str, data:Any):
    pdf = FPDF("P","mm","a4")
    pdf.add_page()
    pdf.l_margin = 20

    titre1 = "REPOBLIKAN'I MADAGASIKARA"
    titre2 = "Fitiavana - Tanindrazana - Fandrosoana"
    titre3 = "Ministère de l'Enseignement Supérieur et de la Recherche Scientifique"

    titre4 = "UNIVERSITE DE FIANARANTSOA"
    titre5 = "FACULTE DES SCIENCES"
    titre6 = f"N° {num}/{date}/UF/FAC.S/S.SCO"
    nom_certificat = f"CERTIFICAT D'ASSIDUITE"

    text_1 = "Le DOYEN de la FACULTE des SCIENCES de L'Université de Fianarantsoa"
    text_2 = "Soussigné, certifie que:"

    nom = "Nom:"
    nom_etudiant = f"{data['nom']}"
    prenom = "Prénom:"
    prenom_etudiant = f"{data['prenom']}"
    naiss = "Né(e) le:"
    naiss_etudiant = f"{data['date_naiss']} à {data['lieu_naiss']}"
    niveau = "est régulièrement inscrit(e) comme étudiant(e) en "
    niveau_etudiant = f"{data['niveau']}"
    mention = "MENTION:"
    mention_etudiant = f"{data['mention']}"
    parcours = "PARCOURS:"
    parcours_etudiant = f"{data['parcours']}"
    registre = f"N° sur le registre:"
    registre_etudiant = f"{num_carte} RI-{data['registre']}"


    text_3 = f"a été assidue dépuis le {rentre_univ}, date de la rentrée universitaire jusqu'à ce jour"
    text_4 = "En foi de quoi, ce certificat lui est delivré pour servir et valoir ce que le droit"

    text_5 = "Fianarantsoa, le "


    pdf.set_font("arial","B",14)
    pdf.cell(0,15,"",0,1,"C")

    pdf.set_font("arial","B",14)
    pdf.cell(0,2,titre1,0,1,"C")

    pdf.set_font("arial","B",8)
    pdf.cell(0,10,titre2,0,1,"C")

    pdf.set_font("arial","BI",12)
    pdf.cell(0,0,titre3,0,1,"C")

    pdf.set_font("arial","BI",12)
    pdf.cell(0,10,"",0,1,"C")

    pdf.set_font("arial","B",14)
    pdf.cell(0,6,titre4,0,1,"C")

    pdf.set_font("arial","B",12)
    pdf.cell(0,6,titre5,0,1,"C")

    pdf.set_font("arial","BI",12)
    pdf.cell(0,6,titre6,0,1,"C")


    pdf.cell(0,6,"",0,2,"C")
    pdf.set_font("Times","BI",18)
    pdf.cell(90,20,nom_certificat,1,1,"C", center=True)

    pdf.cell(0,5,"",0,2,"C")
    pdf.set_font("arial","",12)
    pdf.cell(0,8,text_1,0,1,"L")

    pdf.set_font("arial","",12)
    pdf.cell(0,8,text_2,0,1,"L")

    pdf.set_font("arial","BUI",12)
    pdf.cell(12,8,nom,0,0,"L")

    pdf.set_font("arial","I",12)
    pdf.cell(0,8,nom_etudiant,0,1)

    pdf.set_font("arial","BUI",12)
    pdf.cell(18,8,prenom,0,0,"L")

    pdf.set_font("arial","I",12)
    pdf.cell(0,8,prenom_etudiant,0,1)

    pdf.set_font("arial","BUI",12)
    pdf.cell(18,8,naiss,0,0,"L")

    pdf.set_font("arial","I",12)
    pdf.cell(0,8,naiss_etudiant,0,1)

    pdf.set_font("arial","",12)
    pdf.cell(93,8,niveau,0,0,"L")

    pdf.set_font("arial","BI",12)
    pdf.cell(0,8,niveau_etudiant,0,1)

    pdf.set_font("arial","BUI",12)
    pdf.cell(22,8,mention,0,0,"L")

    pdf.set_font("arial","I",12)
    pdf.cell(0,8,mention_etudiant,0,1)

    pdf.set_font("arial","BUI",12)
    pdf.cell(27,8,parcours,0,0,"L")

    pdf.set_font("arial","I",12)
    pdf.cell(0,8,parcours_etudiant,0,1)

    pdf.set_font("arial","BUI",12)
    pdf.cell(37,8,registre,0,0,"L")

    pdf.set_font("arial","I",12)
    pdf.cell(0,8,registre_etudiant,0,1)

    pdf.set_font("arial","",12)
    pdf.cell(0,8,text_3,0,1)


    pdf.cell(0,8,"",0,3)
    pdf.cell(0,8,text_4,0,1)
    pdf.cell(94,12,"",0,0)
    pdf.cell(0,12,text_5,0,1)


    pdf.cell(0,40,"",0,5)


    pdf.output(f"{num_carte}_assiduite_.pdf","F")

if __name__=="__main__":
    # string = "éôfèçdn&n sdgfgz"
    # strd = string.replace(" ","_")
    # print(unidecode.unidecode(strd))
    data = {"nom":"RALAITSIMANOLAKAVANA","prenom":"Henri Franck",
            "date_naiss":"07 octobre 1995 ", "lieu_naiss":" Fianarantsoa",
            "niveau":"M2", "mention":"Mathématiques et Applications",
            "parcours":"Mathématiques et Informatiques pous la Sciences Social",
            "registre":"20"}

    create_certificat_assidute( "4465", 50,"2020", "3 Mars 2021", data)