import random
from typing import Any
from fpdf import FPDF
import unidecode

from app.utils import convert_date


def attestation_inscription(num_carte: str, date: str, anne_univ: str, data: Any) -> str:
    pdf = FPDF("P", "mm", "a4")
    pdf.add_page()
    pdf.l_margin = 20

    titre1 = "REPOBLIKAN'I MADAGASIKARA"
    titre2 = "Fitiavana - Tanindrazana - Fandrosoana"
    titre3 = "Ministère de l'Enseignement Supérieur et de la Recherche Scientifique"

    titre4 = "UNIVERSITE DE FIANARANTSOA"
    titre5 = "FACULTE DES SCIENCES"
    titre6 = f"N° ___/{date}/UF/FAC.S/S.SCO"
    nom_certificat = f"ATTESTATION D'INSCRIPTION"

    text_1 = "Le DOYEN de la FACULTE des SCIENCES de L'Université de Fianarantsoa"
    text_2 = "Soussigné, atteste que:"

    nom = "Nom:"
    nom_etudiant = f"{data['nom']}"
    prenom = "Prénom:"
    prenom_etudiant = f"{data['prenom']}"
    naiss = "Né(e) le:"
    naiss_etudiant = f"{convert_date(data['date_naiss'])} à {data['lieu_naiss']}"
    niveau = "est régulièrement inscrit(e) comme étudiant(e) en "
    niveau_etudiant = f"{data['niveau']}"
    mention = "MENTION:"
    mention_etudiant = f"{data['mention']}"
    parcours = "PARCOURS:"
    parcours_etudiant = f"{data['parcours']}"
    registre = f"N° sur le registre:"
    registre_etudiant = f"{num_carte} RI-{data['registre']}"

    text_3 = f"Durant, l'année Universitaire {anne_univ}"
    text_4 = "En foi de quoi, la présence d'attestation lui est delivré pour servir et valoir ce que le droit"

    text_5 = "Fianarantsoa, le "

    pdf.add_font("alger", "", "Algerian.ttf", uni=True)
    pdf.add_font("aparaj", "", "aparaji.ttf", uni=True)

    pdf.set_font("arial", "B", 14)
    pdf.cell(0, 15, txt="", ln=1)

    pdf.set_font("arial", "B", 14)
    pdf.cell(0, 2, txt=titre1, ln=1, align="C")

    pdf.set_font("aparaj", "", 11)
    pdf.cell(0, 10, txt=titre2, ln=1, align="C")

    pdf.set_font("arial", "BI", 12)
    pdf.cell(0, 0, txt=titre3, ln=1, align="C")

    pdf.set_font("arial", "BI", 12)
    pdf.cell(0, 10, txt="", ln=1)

    pdf.set_font("arial", "B", 14)
    pdf.cell(0, 6, txt=titre4, ln=1, align="C")

    pdf.set_font("arial", "B", 12)
    pdf.cell(0, 6, txt=titre5, ln=1, align="C")

    pdf.set_font("arial", "BI", 12)
    pdf.cell(0, 6, txt=titre6, ln=1, align="C")

    pdf.cell(0, 6, txt="", ln=1)
    pdf.set_font("alger", "", 18)
    pdf.cell(105, 20, txt=nom_certificat, border=1, ln=1, align="C", center=True)

    pdf.cell(0, 5, txt="", ln=1)
    pdf.set_font("arial", "", 12)
    pdf.cell(0, 8, txt=text_1, ln=1, align="L")

    pdf.set_font("arial", "", 12)
    pdf.cell(0, 8, txt=text_2, ln=1, align="L")

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(12, 8, txt=nom, ln=0)

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=nom_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(18, 8, txt=prenom, ln=0)

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=prenom_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(18, 8, txt=naiss, ln=0)

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=naiss_etudiant, ln=1)

    pdf.set_font("arial", "", 12)
    pdf.cell(93, 8, txt=niveau, ln=0)

    pdf.set_font("arial", "BI", 12)
    pdf.cell(0, 8, txt=niveau_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(22, 8, txt=mention, ln=0)

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=mention_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(27, 8, txt=parcours, ln=0)

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=parcours_etudiant, ln=1)

    pdf.set_font("arial", "BUI", 12)
    pdf.cell(37, 8, txt=registre, ln=0)

    pdf.set_font("arial", "I", 12)
    pdf.cell(0, 8, txt=registre_etudiant, ln=1)

    pdf.set_font("arial", "", 12)
    pdf.cell(0, 8, txt=text_3, ln=1)

    pdf.cell(0, 8, txt="", ln=1)
    pdf.cell(0, 8, txt=text_4, ln=1)
    pdf.cell(94, 12, txt="", ln=0)
    pdf.cell(0, 12, txt=text_5, ln=1)

    pdf.cell(0, 40, txt="", ln=1)

    pdf.output(f"files/{num_carte}_inscription.pdf", "F")

    return f"files/{num_carte}_inscription.pdf"


if __name__ == "__main__":
    # string = "éôfèçdn&n sdgfgz"
    # strd = string.replace(" ","_")
    # print(unidecode.unidecode(strd))
    data = {"nom": "RALAITSIMANOLAKAVANA", "prenom": "Henri Franck",
            "date_naiss": "07 octobre 1995 ", "lieu_naiss": " Fianarantsoa",
            "niveau": "M2", "mention": "Mathématiques et Applications",
            "parcours": "Mathématiques et Informatiques pous la Sciences Social",
            "registre": "20"}

    attestation_inscription("4465", "2020", "2020-2021", data)
