import random
from typing import Any
from fpdf import FPDF
import unidecode

def validation(ue:float)-> str:
        if float(ue) < 10:
            return "Compensé"
        else:
            return "Validé"

class PDF(FPDF):
    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("arial","",9)
        self.cell(1,4,"N.B: Ce relevé de Notes ne doit être en aucun cas remis",0,1)
        self.cell(12,6,"",0,0,"L")
        self.cell(1,6,"à l'intéressé sous peine d'annulation.",0,0)

    
    def relever_note(num_carte:str,date: str, anne_univ:str, data:Any, note:Any) -> str:
           
        pdf = PDF('P','mm','A4')
        pdf.add_page()
        pdf.l_margin = 0
        pdf.rect(5,5,200,287)
        pdf.rect(4,4,202,289)
        pdf.l_margin = 8

        titre1 = "REPOBLIKAN'I MADAGASIKARA"
        titre1_2 = "Universtité de fianarantsoa"

        titre2 = "Fitiavana - Tanindrazana - Fandrosoana"
        titre2_1 = "Faculté des sciences"
        titre3 = "Ministère de l'Enseignement Supérieur"
        titre3_1 = "Service scolarité"
        titre4 = "et de la recherche scientifique"
        titre4_1 = f"Année universitaire {anne_univ}"
        titre5 = "releve de notes"
        titre6 = f"N° ___/{date}/UF/FAC.S/S.SCO"

        
        nom = "Nom:"
        nom_etudiant = f"{data['nom']}"
        prenom = "Prénom:"
        prenom_etudiant = f"{data['prenom']}"
        naiss = "Né(e) le:"
        naiss_etudiant = f"{data['date_naiss']} à {data['lieu_naiss']}"
        numero = "N° carte:"
        semestre = f"Semestre:"
        semestre_etudiant = f"{data['semestre']}"
        mention = "Mention:"
        mention_etudiant = f"{data['mention']}"
        parcours = "Parcours:"
        parcours_etudiant = f"{data['parcours']}"
        session = f"Session:"
        session_etudiant = f"{data['session']}"


        titre_1 = "Les unité d'enseignements"
        titre_2 = "Notes(/20)"
        titre_3 = "Coéfficients"
        titre_4 = 'Crédits'
        titre_5 = "Status de l'UE"
        text_6 = "Décision du jury:"
        text_7 = "Fianarantsoa, le "
        moyenne = "moyenne générale"



        pdf.add_font("alger","","Algerian.ttf",uni=True)
        pdf.add_font("aparaj","","aparaji.ttf",uni=True)


        pdf.set_font("arial","B",12)
        pdf.cell(10,6,"",0,0,"L")
        pdf.cell(110,6,titre1,0,0,"L")

        pdf.set_font("arial","B",12)
        pdf.cell(0,5,titre1_2.upper(),0,1)


        pdf.set_font("arial","",8)
        pdf.cell(20,6,"",0,0,"L")
        pdf.cell(115,6,titre2,0,0,"L")

        pdf.set_font("arial","B",10)
        pdf.cell(0,5,titre2_1.upper(),0,1)


        pdf.set_font("arial","B",12)
        pdf.cell(139,6,titre3.upper(),0,0,"L")

        pdf.set_font("arial","B",10)
        pdf.cell(0,5,titre3_1.upper(),0,1)


        pdf.set_font("arial","B",12)
        pdf.cell(8,6,"",0,0,"L")
        pdf.cell(124,6,titre4.upper(),0,0,"L")

        pdf.set_font("arial","",10)
        pdf.cell(0,5,titre4_1,0,1)


        pdf.set_font("arial","B",12)
        pdf.ln(3)
        pdf.cell(193,6,titre5.upper(),0,1,"C")
        pdf.cell(193,6,titre6.upper(),0,1,"C")

        pdf.ln(6)
        pdf.rect(20,48,170,52)


        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(12,6,nom,0,0,"L")

        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,nom_etudiant,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(18,6,prenom,0,0,"L")

        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,prenom_etudiant,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(18,6,naiss,0,0,"L")

        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,naiss_etudiant,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(18,6,numero,0,0,"L")
        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,num_carte,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(19,6,mention,0,0,"L")

        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,mention_etudiant,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(21,6,parcours,0,0,"L")

        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,parcours_etudiant,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(21,6,semestre,0,0,"L")


        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,semestre_etudiant,0,1)

        pdf.set_font("arial","BI",12)
        pdf.cell(18,6,"",0,0,"L")
        pdf.cell(19,6,session,0,0,"L")

        pdf.set_font("aparaj","",14)
        pdf.cell(0,6,session_etudiant,0,1)


    # debut de creation du tableau
        pdf.cell(30,2,"",0,1)
        pdf.set_font("arial","I",11)
        pdf.cell(12,2,"",0,0)

        pdf.set_fill_color(210,210,210)
        pdf.cell(80,6,titre_1.upper(),1,0,"C",fill=True)

        pdf.cell(20,6,titre_2,1,0,"C",fill=True)
        
        pdf.cell(25,6,titre_3,1,0,"C",fill=True)
        
        pdf.cell(15,6,titre_4,1,0,"C",fill=True)

        pdf.cell(30,6,titre_5,1,1,"C",fill=True)

        for index_ue, value_ue in enumerate(note['ue']):
            pdf.set_top_margin(20)
            pdf.cell(30,1,"",0,1)
            pdf.cell(12,2,"",0,0)
            pdf.set_font("arial","BI",10)
            pdf.cell(80,5,f"U.E-{index_ue+1}: {value_ue['name']}",1,0,"C")
            pdf.set_font("arial","I",11)
            pdf.cell(1,1,"",0,0)
            pdf.cell(19,5,"",1,0,"C")
            pdf.cell(1,1,"",0,0)
            pdf.cell(24,5,"",1,0,"C")
            pdf.cell(1,1,"",0,0)
            pdf.cell(14,5,"",1,0,"C")
            pdf.cell(1,1,"",0,0)
            pdf.cell(29,5,"",1,1,"C")
            for index, value in enumerate(value_ue['ec']):
                pdf.set_top_margin(20)
                pdf.cell(30,1,"",0,1)
                pdf.cell(12,2,"",0,0)
                pdf.set_font("arial","I",10)
                pdf.cell(80,5,f"E.C-{index+1}: {value['name']}",1,0,"L")
                pdf.set_font("arial","I",11)
                pdf.cell(1,1,"",0,0)
                pdf.cell(19,5,str(value['note']),1,0,"C")
                pdf.cell(1,1,"",0,0)
                pdf.cell(24,5,str(value['poids']),1,0,"C")
                pdf.cell(1,1,"",0,0)
                pdf.cell(14,5,"",1,0,"C")
                pdf.cell(1,1,"",0,0)
                pdf.cell(29,5,"",1,1,"C")
            pdf.set_top_margin(20)
            pdf.cell(30,1,"",0,1)
            pdf.cell(12,2,"",0,0)
            pdf.set_font("arial","BI",10)
            pdf.cell(80,5,f"NOTE SOUS TOTAL U.E-{index_ue+1}",1,0,"C")
            pdf.set_font("arial","I",11)
            pdf.cell(1,1,"",0,0)
            pdf.cell(19,5,str(value_ue['note']),1,0,"C")
            pdf.cell(1,1,"",0,0)
            pdf.cell(24,5,"",1,0,"C")
            pdf.cell(1,1,"",0,0)
            pdf.cell(14,5,str(value_ue['credit']),1,0,"C")
            pdf.cell(1,1,"",0,0)
            pdf.set_font("alger","",12)
            pdf.cell(29,5,validation(value_ue['note']),1,1,"C")

        pdf.set_top_margin(20)
        pdf.cell(30,1,"",0,1)
        pdf.cell(12,2,"",0,0)
        pdf.set_font("arial","BI",10)
        pdf.cell(80,6,moyenne.upper(),1,0,"C")
        pdf.set_font("arial","I",11)
        pdf.cell(1,1,"",0,0)
        pdf.cell(19,6,str(format(note['moyenne'], '.3f')),1,0,"C")
        pdf.cell(1,1,"",0,0)
        pdf.cell(24,5,"",0,0,"C")
        pdf.cell(1,1,"",0,0)
        pdf.cell(14,5,"",0,0,"C")
        pdf.cell(1,1,"",0,0)
        pdf.cell(29,5,"",0,1,"C")
        
        pdf.set_font("Times","Bui",12)
        pdf.cell(40,10,"",0,0)
        pdf.cell(0,10,text_6,0,1)
        pdf.set_font("arial","I",10)
        pdf.cell(120,1,"",0,1)
        pdf.cell(120,10,"",0,0)
        pdf.cell(0,8,text_7,0,1)

        pdf.output(f"files/{num_carte}_relever.pdf","F")

        return (f"files/{num_carte}_relever.pdf")
