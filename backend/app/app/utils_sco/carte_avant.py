from fpdf import FPDF
from typing import Any
import qrcode
import os


class PDF(FPDF):
    def footer(self) -> None:
        self.set_y(-6)

    def create_carte(pdf: FPDF, pos_init_y: int, long_init_y: int, deux_et: list, data: Any):
        j: int = 0

        image_fac = f"images/{data['img_carte']}_avant.jpg"
        logo_fac = "images/logo_science.jpg"

        titre_1 = "Université de Fanarantsoa \n"
        titre_1 += "Faculté des Sciences \n"

        titre_2 = "Le Chef de service de scolarité:"
        titre_3 = f"{data['supperadmin']}"

        titre_4 = "Faculté des Sciences"
        i: int = 0
        pos_init_x: int = 0.2
        long_init_x: int = 3.9
        absci: int = 1.25
        ordon: int = 0.06

        i = 0
        while i < len(deux_et):
            num_carte = f"{deux_et[i]['num_carte']}"
            niveau = f"Niveau: {deux_et[i]['niveau']}"

            image = f"photos/4465.jpg"
            if os.path.exists(f"photos/{num_carte}.jpg"):
                image = f"photos/{num_carte}.jpg"
            info = f"{deux_et[i]['nom'].upper()}\n"
            info += f"{deux_et[i]['prenom']}\n"

            info_ = f" {data['mention']} \n "
            info_ += f"Parcours: {deux_et[i]['parcours'].upper()} \n "
            info_ += f"Né(e) le {deux_et[i]['date_naiss']} "
            info_ += f"à {deux_et[i]['lieu_naiss']} \n "

            data_et = [deux_et[i]['num_carte'],data['key']]

            if {deux_et[i]['num_cin']}:
                info_ += f"CIN {deux_et[i]['num_cin']} "
                info_ += f"du {deux_et[i]['date_cin']} \n "
                info_ += f"à {deux_et[i]['lieu_cin']} \n "

            qr = qrcode.make(f"{data_et}")

            pdf.set_font('Times', '', 8.0)
            pdf.image(image_fac, x=pos_init_x, y=pos_init_y, w=long_init_x, h=long_init_y)
            pdf.rect(pos_init_x, pos_init_y, w=long_init_x, h=long_init_y)
            pdf.image(image, x=pos_init_x, y=pos_init_y, w=1, h=1.18)
            pdf.set_text_color(0, 0, 0)

            pdf.set_font('Times', 'B', 7.0)
            if i == 0:
                pdf.set_xy(absci, pos_init_y + ordon)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2, pos_init_y + ordon)

            pdf.multi_cell(1.8, 0.15, info, 0, fill=0, align='L')
            pdf.ln(0.1)

            pdf.set_font('Times', '', 8.0)
            if i == 0:
                pdf.set_xy(absci, pos_init_y + ordon + 0.4)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2, pos_init_y + ordon + 0.4)
            pdf.cell(1.5, 0.15, titre_2, 0, 1, "L")

            if i == 0:
                pdf.set_xy(absci, pos_init_y + ordon + 0.63)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2, pos_init_y + ordon + 0.63)
            pdf.cell(1.5, 0.15, titre_3, 0, 0, "L")

            pdf.set_font('Times', 'B', 8.0)
            if i == 0:
                pdf.set_xy(absci + 2.18, pos_init_y + ordon + 0.65)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 2.18, pos_init_y + ordon + 0.65)
            pdf.image(logo_fac, w=0.4, h=0.4)

            if i == 0:
                pdf.set_xy(absci + 2.19, pos_init_y + ordon + 1.85)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 2.19, pos_init_y + ordon + 1.85)
            pdf.image(qr.get_image(), w=0.5, h=0.5)

            if i == 0:
                pdf.set_xy(absci + 1.8, pos_init_y + ordon + 1.1)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 1.8, pos_init_y + ordon + 1.1)
            pdf.cell(0, 0.15, titre_4, 0, 0, "L")

            if i == 0:
                pdf.set_xy(0.3, pos_init_y + ordon + 1.3)
            else:
                pdf.set_xy(0.9 + pos_init_x - 0.2 - 0.6, pos_init_y + ordon + 1.3)

            pdf.set_font('Times', '', 9.0)
            pdf.set_text_color(255, 255, 255)
            pdf.multi_cell(2.2, 0.15, info_, 0, fill=0, align='J')

            pdf.set_font('Times', 'B', 14.0)
            if i == 0:
                pdf.set_xy(absci + 1.9, pos_init_y + ordon + 0.06)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 1.9, pos_init_y + ordon + 0.06)
            pdf.cell(1, 0.15, num_carte, 0, 1, "C")

            pdf.set_font('Times', 'BI', 10.0)
            if i == 0:
                pdf.set_xy(absci + 1.9, pos_init_y + ordon + 0.36)
            else:
                pdf.set_xy(absci + pos_init_x - 0.2 + 1.9, pos_init_y + ordon + 0.36)
            pdf.cell(1, 0.15, niveau, 0, 1, "C")
            pdf.ln(0.1)

            pos_init_x = long_init_x + 0.3
            i = i + 1

    def boucle_carte(pdf: FPDF, huit_etudiant: list, data: Any):
        pdf.add_page()
        pos_init_y: int = 0.2
        long_init_y: int = 2.5
        nbr: int = 0
        if len(huit_etudiant) % 2 == 0:
            nbr = len(huit_etudiant) // 2
        else:
            nbr = (len(huit_etudiant) // 2) + 1
        n = 0
        p: int = 0
        k = 0
        while n < nbr:
            PDF.create_carte(pdf, pos_init_y, long_init_y, huit_etudiant[p:p + 2], data)
            p += 2
            pos_init_y = pos_init_y + long_init_y + 0.1
            n += 1

        pdf.line(4.15, 0.2, 4.15, pos_init_y - 0.05)

    def parcourir_et(etudiant: list, data: Any):

        pdf = PDF("P", "in", "a4")
        nbr: int = 0

        if len(etudiant) % 8 == 0:
            nbr = len(etudiant) // 8
        else:
            nbr = (len(etudiant) // 8) + 1
        k: int = 0
        l: int = 0

        while k < nbr:
            PDF.boucle_carte(pdf, etudiant[l:l + 8], data)
            k += 1
            l += 8
        pdf.output(f"files/carte_{data['mention']}.pdf", "F")

        return (f"files/carte_{data['mention']}.pdf")
