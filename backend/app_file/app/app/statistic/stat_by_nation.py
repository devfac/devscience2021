from datetime import date
from typing import Any, List
from fpdf import FPDF
from app import crud


def get_by_params(niveau: str, all_etudiant: any, sexe: str, nation: str) -> int:
    all_niveau = ["L1", "L2", "L3", "M1", "M2"]
    if sexe == "M":
        sexe = "Masculin"
    else:
        sexe = "Feminin"
    stat_etudiant = []
    if niveau in all_niveau:
        etudiants = all_etudiant[niveau]
        for etudiant in etudiants:
            if etudiant.sexe == sexe.upper() and etudiant.nation == nation:
                stat_etudiant.append(etudiant)
    return len(stat_etudiant)


class PDF(FPDF):

    def add_title(pdf: FPDF, data: Any):

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
        localisation = "LOCALISATION:"
        localisation_ = "ANDRAINJATO FIANARANTSOA"
        titre_1 = f"Etudiants étrangères inscritent par établissement au titre de l'année{data['anne']}"
        anne_univ = f"{data['anne']}"

        tabulation: int = 35
        ln: int = 1

        pdf.set_font("arial", "B", 12)
        pdf.cell(0, 6, titre4, 0, 1, "C")

        pdf.set_font("arial", "B", 10)
        pdf.cell(0, 6, titre5, 0, 1, "C")

        pdf.cell(0, 18, "", 0, 1, "C")

        pdf.cell(tabulation, 6, "", 0, 0, "L")
        pdf.set_font("arial", "BI", 12)
        pdf.cell(34, 6, localisation, 0, 0, "L")
        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 6, localisation_, 0, 1)

        pdf.set_font("arial", "BI", 12)
        pdf.cell(tabulation, 6, "", 0, 0, "L")
        pdf.cell(24, 6, mention, 0, 0, "L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(70, 6, mention_etudiant, 0, ln)

        pdf.cell(20, 6, "", 0, 0, "L")
        pdf.cell(107, 6, titre_1, 0, 0, "L")

        pdf.cell(15, 10, "", 0, 1, "L")

    def create_statistic_by_nation(data: Any, all_etudiant, schemas: str):
        titre_stat = [{"name": '', "value": ["Niveau"]}, {"name": "Africaine", "value": ["M", "F"]},
                      {"name": "Asiatique", "value": ["M", "F"]},
                      {"name": "Comorienne", "value": ["M", "F"]}, {"name": "Européene", "value": ["M", "F"]},
                      {"name": "Autre à préciser", "value": ["M", "F"]}]

        width: int = 30
        height: int = 7

        pdf = PDF("P", "mm", "a4")

        niveau_ = ["L1", "L2", "L3", "M1", "M2", "6eme", "7eme", "Doctorat"]
        pdf.add_page()
        PDF.add_title(pdf=pdf, data=data)
        pdf.set_margin(9)
        for titre in titre_stat:
            pdf.set_font("arial", "BI", 10)
            if titre["name"] == '':
                pdf.cell(width, height, titre["name"], 0, 0, "C")
            elif titre["name"] != 'Autre à préciser':
                pdf.cell(width, height, titre["name"], 1, 0, "C")
            else:
                pdf.cell(width + 10, height, titre["name"], 1, 0, "C")
                pdf.cell(0, height, "", 0, 1, "L")

        for titre in titre_stat:
            for value in titre["value"]:
                pdf.set_font("arial", "BI", 10)
                if titre["name"] != 'Autre à préciser':
                    pdf.cell(width / (len(titre["value"])), height, value, 1, 0, "C")
                else:
                    pdf.cell((width + 10) / (len(titre["value"])), height, value, 1, 0, "C")
        pdf.cell(0, height, "", 0, 1, "L")

        for niveau in niveau_:
            for index_1, titre in enumerate(titre_stat):
                for value in titre["value"]:
                    pdf.set_font("arial", "BI", 10)
                    response = get_by_params(niveau, all_etudiant, value, titre["name"])
                    if index_1 == 0:
                        pdf.cell(width / (len(titre["value"])), height, niveau, 1, 0, "C")
                    else:
                        if titre["name"] != 'Autre à préciser':
                            pdf.cell(width / (len(titre["value"])), height, str(response), 1, 0, "C")
                        else:
                            pdf.cell((width + 10) / (len(titre["value"])), height, str(0), 1, 0, "C")

            pdf.cell(0, height, "", 0, 1, "L")

        bas_1 = " M: Masculin, F: Feminin"

        pdf.cell(0, height, "", 0, 1, "L")
        pdf.cell(0, 5, bas_1, 0, 1, "L")

        pdf.output(f"files/statistic_by_nation.pdf", "F")
        return f"files/statistic_by_nation.pdf"
