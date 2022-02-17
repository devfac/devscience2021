from typing import Any, List
from fpdf import FPDF


def set_orientation(nbr:int) -> str:
    if nbr >= 8 :
        return "L"
    return "P"

def set_police(mot:str, nbr:int) -> int:
    if nbr >= 7:
        if len(mot) >= 25 :
            return 8
        elif len(mot) >= 31 :
            return 7
        elif len(mot) >= 36 :
            return 6
    return 10

def set_police_name(mot:str, dim:int) -> int:
    if dim == 73:
        if len(mot) <= 35 :
            return 10
        elif len(mot) <= 47 :
            return 7
        elif len(mot) <= 54 :
            return 6
    elif dim == 108:
        if len(mot) <= 50 :
            return 10
        else:
            return 8
    return 10

def set_dimention(nbr:int) -> int:
    if nbr ==1 :
        return 158
    elif nbr == 2:
        return 107
    elif nbr == 3:
        return 142
    else:
        return 90

def get_dime(nbr:int) -> int:
    if nbr == 6:
        return 320
    elif nbr == 5:
        return 396
    elif nbr == 7:
        return 286
    else:
        return 400

class PDF(FPDF):
    def add_title(pdf:FPDF, data:Any,sems:str,title:str, nbr:int):

        pdf.add_font("alger","","Algerian.ttf",uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"


        pdf.add_font("alger","","Algerian.ttf",uni=True)

        pdf.image(image_univ,x=30,y=6,w=30, h=30)
        if nbr >= 8:
            pdf.image(image_fac,x=240,y=6,w=30, h=30)
        else:
            pdf.image(image_fac,x=155,y=6,w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTE DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        parcours = "PARCOURS:"
        parcours_etudiant = f"{data['parcours']}"
        semestre = "SEMESTRE:"
        semestre_etudiant = f"{sems.upper()}"
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"
        session = "SESSION:"
        session_class = f"{data['session']}"

        pdf.set_font("arial","B",12)
        pdf.cell(0,6,titre4,0,1,"C")

        pdf.set_font("arial","B",10)
        pdf.cell(0,6,titre5,0,1,"C")
        pdf.set_font("alger","",15)
        pdf.cell(0,15,"",0,1,"C")
        pdf.cell(0,15,title,0,1,"C")


        pdf.set_font("arial","BI",13)
        pdf.cell(24,8,mention,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,8,mention_etudiant,0,1)

        pdf.set_font("arial","BI",13)
        pdf.cell(29,8,parcours,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,8,parcours_etudiant,0,1)

        pdf.set_font("arial","BI",13)
        pdf.cell(28,8,semestre,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,8,semestre_etudiant,0,1)

        pdf.set_font("arial","BI",13)
        pdf.cell(56,8,anne,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,8,anne_univ,0,1)

        pdf.set_font("arial","BI",13)
        pdf.cell(23,8,session,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,8,session_class.upper(),0,1)
        
    def add_corp(pdf:FPDF, data:Any,sems:str,matiers:List[str], admis:Any, type:str):
        pdf.add_page()
        pdf.set_margin(10)  
        titre = f"RESULTAT DE L'UNITÉ D'ESEIGNEMENTS {matiers[1].upper()}"
        PDF.add_title(pdf=pdf,data=data,sems=sems,title=titre,nbr=2)
        pdf.cell(1,7,"",0,1)
        pdf.set_font("arial","BI",10)
        pdf.cell(1,5,"",0,0)
        pdf.cell(18,5,"N° Carte",1,0)
        pdf.cell(1,5,"",0,0)
        pdf.cell(160,5,"Nom et prénom",1,0,"C")
        nbr = 0
        for i,etudiant in enumerate(admis):
            nbr += 1
            num_carte_ = etudiant['N° Carte']
            name = f"{etudiant['nom']} {etudiant['prenom']}"
            pdf.cell(1,7,"",0,1)
            pdf.set_font("arial","I",10)
            pdf.cell(1,5,"",0,0)
            pdf.cell(18,5,num_carte_,1,0)
            pdf.cell(1,5,"",0,0)
            pdf.set_font("arial","I",10)
            pdf.cell(160,5,name,1,0,"L")

        text_1 = f"ARRÉTÉE LA PRÉSENTE LISTE AU NOMBRE DE {nbr} ÉTUDIANT(S) AYANT VALIDÉ(S) L'UNITE D'ENSEIGNEMENT "
        if type =="compense":
            text_2 = f"{matiers[1].upper()} PAR COMPENSATION"
        else:
            text_2 = f"{matiers[1].upper()} "

        text_3 = "Le PRÉSIDENT DU JURY"
        text_4 = "Fianarantsoa, le"
        pdf.set_font("arial","BI",10)
        pdf.cell(1,7,"",0,1)
        pdf.cell(0,5,text_1,0,1,"L")
        pdf.cell(0,5,text_2,0,1,"L")
        pdf.cell(1,2,"",0,1)

        pdf.set_font("arial","BI",10)
        pdf.cell(100,5,"",0,0,"L")
        pdf.cell(0,5,text_3,0,1,"L")
        pdf.cell(1,22,"",0,1)
        pdf.cell(100,5,"",0,0,"L")
        pdf.cell(0,5,text_4,0,1,"L")



    def create_result_by_ue(sems:str, parcour:str, data:Any,matiers:List[str],etudiants:Any, admis:Any, admis_comp:Any):
        pdf = PDF(set_orientation(len(matiers)),"mm","a4")
        pdf.add_page()
        
        titre = f"RÉSULTAT PROVISOIR DE L'UNITÉ D'ENSEIGNEMENT {matiers[1].upper()}"
        PDF.add_title(pdf=pdf,data=data,sems=sems,title=titre,nbr=len(matiers))

        pdf.set_font("arial","B",10)
        pdf.cell(0,5,"",0,1,"C")

        for i, ue in enumerate(matiers):
            dim = set_dimention(len(ue))
            pdf.set_left_margin(1)
            taille = set_police(ue, len(matiers))
            pdf.cell(1,8,"",0,0)
            pdf.set_font("arial","I",10)
            titre = f"{ue}"
            dim = get_dime(len(matiers))/len(matiers)-3
            if titre == "Status":
                dim = 20
            elif titre ==  "Crédit" or titre == "N° Carte":
                dim = 15
            pdf.set_font("arial","",taille)
            pdf.cell(dim,5,titre,1,0,"C")
    
        for i,etudiant in enumerate(etudiants):

            pdf.cell(1,5,"",0,1)
            pdf.cell(1,1,"",0,1)
            for i, ue in enumerate(matiers):
                titre = f"{ue}"
                dim = get_dime(len(matiers))/len(matiers)-3
                if titre == "Status":
                    dim = 20
                    value = str(etudiant[ue])
                elif titre ==  "Crédit" or titre == "N° Carte":
                    dim = 15
                    value = str(etudiant[ue])
                else:
                    if str(etudiant[ue]) == "None" or str(etudiant[ue]) == "":
                        value = "Absent"
                    else:
                        value = str(format(float(etudiant[ue]),'.3f') )
                pdf.set_font("arial","I",10)
                pdf.cell(1,5,"",0,0)
                if value == "None" or value == "":
                    value = "Absent"
                pdf.cell(dim,5,value,1,0,'C')
        PDF.add_corp(pdf=pdf,data=data,sems=sems,matiers=matiers,admis=admis,type="definitive")
        if len(admis_comp) != 0:
            PDF.add_corp(pdf=pdf,data=data,sems=sems,matiers=matiers,admis=admis_comp,type="compense")




        pdf.output(f"files/resultat_{sems}_{parcour.abreviation}_{matiers[1]}.pdf","F")
        return f"files/resultat_{sems}_{parcour.abreviation}_{matiers[1]}.pdf"

