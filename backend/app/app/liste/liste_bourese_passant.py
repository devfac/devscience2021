from typing import Any
from fpdf import FPDF
    
class PDF(FPDF):
    
    def add_title(pdf:FPDF, data:Any,title:str):

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
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"


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
        pdf.cell(56,8,anne,0,0,"L")

        pdf.set_font("arial","I",12)
        pdf.cell(0,8,anne_univ,0,1)

    def create_list_bourse_passant(mention:str,all_data:Any):
        pdf = PDF("P","mm","a4")
        pdf.add_page()
        data = {}
        data['mention'] = all_data['mention']
        data['anne'] = all_data['anne']


        titre = "LISTE DES ÉTUDIANTS BOURSIER PASSANT"
        PDF.add_title(pdf=pdf,data=data,title=titre)

        num = "N°"
        num_c = "N° Carte"
        nom_et_prenom = "Nom et prénom"

        pdf.cell(1,7,"",0,1)
        pdf.set_font("arial","BI",10)
        pdf.cell(1,5,"",0,0)
        pdf.cell(12,5,num,1,0)
        pdf.cell(1,5,"",0,0)
        pdf.cell(18,5,num_c,1,0)
        pdf.cell(1,5,"",0,0)
        pdf.cell(160,5,nom_et_prenom,1,0,"C")
        num_ = 1
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

        pdf.output(f"files/list_bourse_{mention}.pdf","F")
        return f"files/list_bourse_{mention}.pdf"