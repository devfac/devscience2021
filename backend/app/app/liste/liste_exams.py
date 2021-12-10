from typing import Any
from fpdf import FPDF

def set_orientation(nbr:int) -> str:
    if nbr >= 3 :
        return "L"
    return "P"

def set_police(mot:str) -> int:
    if len(mot) <= 27 :
        return 8
    elif len(mot) <= 31 :
        return 7
    elif len(mot) <= 36 :
        return 6
    return 5

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

class PDF(FPDF):
    def add_title(pdf:FPDF, data:Any,sems:str,title:str):

        pdf.add_font("alger","","Algerian.ttf",uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"


        pdf.add_font("alger","","Algerian.ttf",uni=True)

        pdf.image(image_univ,x=30,y=6,w=30, h=30)
        pdf.image(image_fac,x=155,y=6,w=30, h=30)

        numero = f" N° {data['skip']} à {data['limit']}"
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
        salle = "SALLE:"
        salle_et = f"{data['salle']}"


        pdf.set_font("arial","B",12)
        pdf.cell(0,6,titre4,0,1,"C")

        pdf.set_font("arial","B",10)
        pdf.cell(0,6,titre5,0,1,"C")
        pdf.set_font("alger","",22)
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

        pdf.set_font("arial","BI",13)
        pdf.cell(17,8,salle.upper(),0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(11,8,salle_et,0,0) 

        pdf.set_font("arial","I",12)
        pdf.cell(0,8,numero,0,1)



    def create_list_examen(sems:str, parcour:str, data:Any,matiers:Any,etudiants:Any):
        pdf = PDF("P","mm","a4")
        pdf.add_page()

        titre = "FICHE DE PRÉSENCE PAR U.E"
        PDF.add_title(pdf=pdf,data=data,sems=sems,title=titre)

        num = "N°"
        num_c = "N° Carte"
        nom_et_prenom = "Nom et prénom"

        pdf.set_font("arial","B",10)
        pdf.cell(0,5,"",0,1,"C")

        for i,ue in enumerate(matiers['ue']):
            pdf.set_margin(1)  
            pdf.set_top_margin(12)  
            num_ = int(data['skip'])
            titre_ue = f"Unité d'enseignement {ue['name']}"
            dim = set_dimention(ue['nbr_ec'])
            pdf.add_page(orientation=set_orientation(ue['nbr_ec'])) 
            pdf.set_left_margin(1)  
            pdf.set_font("alger","",10)
            pdf.cell(dim-1,6,titre_ue,0,0)
            for j, ec in enumerate(ue['ec']):
                pdf.cell(1,6,"",0,0)
                pdf.set_font("arial","I",12)
                date = "le,__/__/____"
                pdf.cell(50,6,date,1,0,'C')
            pdf.cell(1,7,"",0,1)
            pdf.set_font("arial","BI",10)
            pdf.cell(1,5,"",0,0)
            pdf.cell(12,5,num,1,0)
            pdf.cell(1,5,"",0,0)
            pdf.cell(18,5,num_c,1,0)
            pdf.cell(1,5,"",0,0)
            pdf.cell(dim-34,5,nom_et_prenom,1,0,"C")
            for j, ec in enumerate(ue['ec']):
                taille = set_police(ec['name'])
                pdf.cell(1,8,"",0,0)
                pdf.set_font("arial","I",taille)
                titre_ec = f"{ec['name']}"
                pdf.cell(50,5,titre_ec.upper(),1,0)
            
            for i,etudiant in enumerate(etudiants):
                num_carte_ =f"{etudiant['num_carte']}"
                name = f"{etudiant['nom']} {etudiant['prenom']}"
                pdf.cell(1,7,"",0,1)
                pdf.set_font("arial","I",10)
                pdf.cell(1,5,"",0,0)
                pdf.cell(12,5,str(num_),1,0)
                pdf.cell(1,5,"",0,0)
                pdf.cell(18,5,num_carte_,1,0)
                pdf.cell(1,5,"",0,0)
                pdf.set_font("arial","I",set_police_name(name,dim-34))
                pdf.cell(dim-34,5,name,1,0,"L")
                num_ +=1
                for i in range(ue['nbr_ec']):
                    pdf.cell(2,5,"",0,0)
                    pdf.cell(24,5,"",1,0)
                    pdf.cell(1,5,"",0,0)
                    pdf.cell(24,5,"",1,0)
        pdf.add_page()
        pdf.set_margin(10)  
        titre = "LISTE DES ETUDIANTS INSCRITS AUX EXAMENS"
        PDF.add_title(pdf=pdf,data=data,sems=sems,title=titre)
        pdf.cell(1,7,"",0,1)
        pdf.set_font("arial","BI",10)
        pdf.cell(1,5,"",0,0)
        pdf.cell(12,5,num,1,0)
        pdf.cell(1,5,"",0,0)
        pdf.cell(18,5,num_c,1,0)
        pdf.cell(1,5,"",0,0)
        pdf.cell(160,5,nom_et_prenom,1,0,"C")
        num_ = int(data['skip'])
        for i,etudiant in enumerate(etudiants):
            num_carte_ = etudiant["num_carte"]
            name = f"{etudiant['nom']} {etudiant['prenom']}"
            pdf.cell(1,7,"",0,1)
            pdf.set_font("arial","I",10)
            pdf.cell(1,5,"",0,0)
            pdf.cell(12,5,str(num_),1,0)
            pdf.cell(1,5,"",0,0)
            pdf.cell(18,5,num_carte_,1,0)
            pdf.cell(1,5,"",0,0)
            pdf.set_font("arial","I",10)
            pdf.cell(160,5,name,1,0,"L")
            num_ +=1


        pdf.output(f"files/list_exam_{sems}_{parcour.abreviation}_{data['skip']}_à_{data['limit']}.pdf","F")
        return f"files/list_exam_{sems}_{parcour.abreviation}_{data['skip']}_à_{data['limit']}.pdf"

