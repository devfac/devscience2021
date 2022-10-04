from typing import Any
from fpdf import FPDF
from .header import header


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, sems: str, title: str):
        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        header(pdf)
        mention = "MENTION:"
        mention_etudiant = f"{data['mention']}"
        journey = "journey:"
        journey_etudiant = f"{data['journey']}"
        semester = "semester:"
        semester_etudiant = f"{sems.upper()}"
        anne = "ANNÉE UNIVERSITAIRE:"
        anne_univ = f"{data['anne']}"

        pdf.set_font("alger", "", 22)
        pdf.cell(0, 15, txt="", ln=1, align="C")
        pdf.cell(0, 15, txt=title, ln=1, align="C")

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=mention, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, mention_etudiant, 0, 1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(29, 8, txt=journey, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=journey_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(28, 8, txt=semester, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=semester_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(56, 8, txt=anne, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=anne_univ, ln=1)

    def create_list_inscrit(sems: str, parcour: str, data: Any, etudiants: Any):
        pdf = PDF("P", "mm", "a4")
        pdf.add_page()

        titre = "LISTE DES ÉTUDIANTS INSCRITS"
        PDF.add_title(pdf=pdf, data=data, sems=sems, title=titre)

        num = "N°"
        num_c = "N° Carte"
        nom_et_prenom = "Nom et prénom"

        pdf.cell(1, 7, txt="", ln=1)
        pdf.set_font("arial", "BI", 10)
        pdf.cell(1, 5, txt="")
        pdf.cell(12, 5, txt=num, border=1)
        pdf.cell(1, 5, txt="")
        pdf.cell(18, 5, txt=num_c, border=1)
        pdf.cell(1, 5, txt="")
        pdf.cell(160, 5, txt=nom_et_prenom, border=1, align="C")
        num_ = 1
        for i, etudiant in enumerate(etudiants):
            num_carte_ = etudiant["num_carte"]
            name = f"{etudiant['last_name']} {etudiant['first_name']}"
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

        pdf.output(f"files/list_inscit_{sems}_{parcour}.pdf", "F")
        return f"files/list_inscit_{sems}_{parcour}.pdf"
