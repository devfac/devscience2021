from typing import Any
from fpdf import FPDF

from app.utils import get_niveau_long


class PDF(FPDF):

    def add_title(pdf: FPDF, data: Any, title: str):

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        pdf.image(image_univ, x=30, y=6, w=30, h=30)
        pdf.image(image_fac, x=155, y=6, w=30, h=30)

        titre4 = "UNIVERSITE DE FIANARANTSOA"
        titre5 = "FACULTE DES SCIENCES"

        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"

        pdf.set_font("arial", "B", 12)
        pdf.cell(0, 6, txt=titre4, ln=1, align="C")

        pdf.set_font("arial", "B", 10)
        pdf.cell(0, 6, txt=titre5, ln=1, align="C")
        pdf.set_font("alger", "", 22)
        pdf.cell(0, 15, txt="", ln=1, align="C")
        pdf.cell(0, 15, txt=title, ln=1, align="C")

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=mention, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=mention_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(56, 8, txt=anne, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=anne_univ, ln=1)

    def create_list_bourse(mention: str, all_data: Any, etat: str):
        pdf = PDF("P", "mm", "a4")
        pdf.add_page()
        data = {'mention': all_data['mention'], 'anne': all_data['anne']}

        titre = f"LISTE DES ÉTUDIANTS BOURSIER {etat.upper()}"
        PDF.add_title(pdf=pdf, data=data, title=titre)

        num = "N°"
        num_c = "N° Carte"
        nom_et_prenom = "Nom et prénom"
        niveau = ['l1', 'l2', 'l3', 'm1', 'm2']
        for i, parcour in enumerate(all_data['parcour']):
            for niv in niveau:
                if len(parcour[niv]) != 0:
                    pdf.add_page()
                    pdf.set_font("arial", "B", 12)
                    pdf.cell(0, 5, txt=f"journey: {parcour['name']}", ln=1, align="L")
                    pdf.cell(1, 1, txt="", ln=1)
                    pdf.cell(0, 5, txt=f"Niveau:{get_niveau_long(niv)}", ln=1, align="L")
                    pdf.cell(1, 4, txt="", ln=1)
                    pdf.set_font("arial", "BI", 10)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(12, 5, txt=num, border=1)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(18, 5, txt=num_c, border=1)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(160, 5, txt=nom_et_prenom, border=1, align="C")
                    num_ = 1
                    for j, etudiant in enumerate(parcour[niv]):
                        num_carte_ = etudiant["num_carte"]
                        name = f"{etudiant['nom']} {etudiant['prenom']}"
                        pdf.cell(1, 7, txt="", ln=1)
                        pdf.set_font("arial", "I", 10)
                        pdf.cell(1, 5, txt="")
                        pdf.cell(12, 5, txt=str(num_), border=1)
                        pdf.cell(1, 5, txt="")
                        pdf.cell(18, 5, txt=num_carte_, border=1)
                        pdf.cell(1, 5, txt="")
                        pdf.set_font("arial", "I", 10)
                        pdf.cell(160, 5, txt=name, border=1, align="L")
                        num_ += 1

        pdf.output(f"files/list_bourse_{etat.lower()}_{mention}.pdf", "F")
        return f"files/list_bourse_{etat.lower()}_{mention}.pdf"
