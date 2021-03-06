from typing import Any
from fpdf import FPDF


def set_orientation(nbr: int) -> str:
    if nbr >= 3:
        return "L"
    return "P"


def set_police(mot: str) -> int:
    if len(mot) <= 27:
        return 8
    elif len(mot) <= 31:
        return 7
    elif len(mot) <= 36:
        return 6
    return 5


def set_police_name(mot: str, dim: int) -> int:
    if dim == 73:
        if len(mot) <= 35:
            return 10
        elif len(mot) <= 47:
            return 7
        elif len(mot) <= 54:
            return 6
    elif dim == 108:
        if len(mot) <= 50:
            return 10
        else:
            return 8
    return 10


def set_dimention(nbr: int) -> int:
    if nbr == 1:
        return 158
    elif nbr == 2:
        return 107
    elif nbr == 3:
        return 142
    else:
        return 90


class PDF(FPDF):
    def add_title(pdf: FPDF, data: Any, sems: str, title: str):

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        image_univ = "images/logo_univ.jpg"
        image_fac = "images/logo_science.jpg"

        pdf.add_font("alger", "", "Algerian.ttf", uni=True)

        pdf.image(image_univ, x=30, y=6, w=30, h=30)
        pdf.image(image_fac, x=155, y=6, w=30, h=30)

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

        pdf.set_font("arial", "B", 12)
        pdf.cell(0, 6, txt=titre4, ln=1, align="C")

        pdf.set_font("arial", "B", 10)
        pdf.cell(0, 6, txt=titre5, ln=1, align="C")
        pdf.set_font("alger", "", 22)
        pdf.cell(0, 15, txt="", ln=1, align="C")
        pdf.cell(0, 15, txt=title, ln=1, align="C")

        pdf.set_font("arial", "BI", 13)
        pdf.cell(24, 8, txt=mention, ln=0, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=mention_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(29, 8, txt=parcours, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=parcours_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(28, 8, txt=semestre, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=semestre_etudiant, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(56, 8, txt=anne, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=anne_univ, ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(23, 8, txt=session, align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=session_class.upper(), ln=1)

        pdf.set_font("arial", "BI", 13)
        pdf.cell(17, 8, txt=salle.upper(), align="L")

        pdf.set_font("arial", "I", 12)
        pdf.cell(11, 8, txt=salle_et)

        pdf.set_font("arial", "I", 12)
        pdf.cell(0, 8, txt=numero, ln=1)

    def create_list_examen(sems: str, parcour: str, data: Any, matiers: Any, etudiants: Any):
        pdf = PDF("P", "mm", "a4")
        pdf.add_page()

        titre = "FICHE DE PRÉSENCE PAR U.E"
        PDF.add_title(pdf=pdf, data=data, sems=sems, title=titre)

        num = "N°"
        num_c = "N° Carte"
        nom_et_prenom = "Nom et prénom"

        pdf.set_font("arial", "B", 10)
        pdf.cell(0, 5, txt="", ln=1, align="C")

        for i, ue in enumerate(matiers['ue']):
            pdf.set_margin(1)
            pdf.set_top_margin(12)
            num_ = int(data['skip'])
            titre_ue = f"Unité d'enseignement {ue['name']}"
            dim = set_dimention(ue['nbr_ec'])
            pdf.add_page(orientation=set_orientation(ue['nbr_ec']))
            pdf.set_left_margin(1)
            pdf.set_font("alger", "", 10)
            pdf.cell(dim - 1, 6, txt=titre_ue)
            for j, ec in enumerate(ue['ec']):
                pdf.cell(1, 6, txt="")
                pdf.set_font("arial", "I", 12)
                date = "le,__/__/____"
                pdf.cell(50, 6, txt=date, border=1, align='C')
            pdf.cell(1, 7, txt="", ln=1)
            pdf.set_font("arial", "BI", 10)
            pdf.cell(1, 5, txt="")
            pdf.cell(12, 5, txt=num, border=1)
            pdf.cell(1, 5, txt="")
            pdf.cell(18, 5, txt=num_c, border=1)
            pdf.cell(1, 5, txt="")
            pdf.cell(dim - 34, 5, txt=nom_et_prenom, border=1, align="C")
            for j, ec in enumerate(ue['ec']):
                taille = set_police(ec['name'])
                pdf.cell(1, 8, txt="")
                pdf.set_font("arial", "I", taille)
                titre_ec = f"{ec['name']}"
                pdf.cell(50, 5, txt=titre_ec.upper(), border=1)

            for i, etudiant in enumerate(etudiants):
                num_carte_ = f"{etudiant['num_carte']}"
                name = f"{etudiant['nom']} {etudiant['prenom']}"
                pdf.cell(1, 7, txt="", ln=1)
                pdf.set_font("arial", "I", 10)
                pdf.cell(1, 5, txt="")
                pdf.cell(12, 5, txt=str(num_), border=1)
                pdf.cell(1, 5, txt="")
                pdf.cell(18, 5, txt=num_carte_, border=1)
                pdf.cell(1, 5, txt="")
                pdf.set_font("arial", "I", set_police_name(name, dim - 34))
                pdf.cell(dim - 34, 5, txt=name, border=1, align="L")
                num_ += 1
                for i in range(ue['nbr_ec']):
                    pdf.cell(2, 5, txt="")
                    pdf.cell(24, 5, txt="", border=1)
                    pdf.cell(1, 5, txt="")
                    pdf.cell(24, 5, txt="", border=1)
        pdf.add_page()
        pdf.set_margin(10)
        titre = "LISTE DES ETUDIANTS INSCRITS AUX EXAMENS"
        PDF.add_title(pdf=pdf, data=data, sems=sems, title=titre)
        pdf.cell(1, 7, txt="", ln=1)
        pdf.set_font("arial", "BI", 10)
        pdf.cell(1, 5, txt="")
        pdf.cell(12, 5, txt=num, border=1)
        pdf.cell(1, 5, txt="")
        pdf.cell(18, 5, txt=num_c, border=1)
        pdf.cell(1, 5, txt="")
        pdf.cell(160, 5, txt=nom_et_prenom, border=1, align="C")
        num_ = int(data['skip'])
        for i, etudiant in enumerate(etudiants):
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

        pdf.output(f"files/list_exam_{sems}_{parcour.abreviation}_{data['skip']}_à_{data['limit']}.pdf", "F")
        return f"files/list_exam_{sems}_{parcour.abreviation}_{data['skip']}_à_{data['limit']}.pdf"
