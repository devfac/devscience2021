from fpdf import FPDF


def create_pdf(data: any):
    pdf = FPDF("P", "mm", "A4")
    pdf.add_page()
    pdf.set_font("Times", size=9)
    pdf.set_margins(4, 4, 4)
    line_height = pdf.font_size * 2.5
    col_width = pdf.epw / 4

    lh_list = []  # list with proper line_height for each row
    use_default_height = 0  # flag

    # create lh_list of line_heights which size is equal to num rows of data
    for row in data:
        for datum in row:
            word_list = datum.split()
            number_of_words = len(word_list)  # how many words
            if number_of_words > 2:  # names and cities formed by 2 words like Los Angeles are ok)
                use_default_height = 1
                new_line_height = pdf.font_size * (number_of_words / 2)  # new height change according to data
        if not use_default_height:
            lh_list.append(line_height)
        else:
            lh_list.append(new_line_height)
            use_default_height = 0

    # create your fpdf table ..passing also max_line_height!
    align: str = "C"
    for j, row in enumerate(data):
        if j == 0:
            pdf.set_font("arial", "B", size=9)
            align = "C"
        else:
            pdf.set_font("arial", size=9)
            align = "L"

        for i, datum in enumerate(row):
            if i == 0 or i == 2:
                col_width = 30
            else:
                col_width = 130
            line_height = lh_list[j]  # choose right height for current row
            pdf.multi_cell(
                col_width,
                line_height,
                datum,
                border=1,
                align=align,
                ln=3,
                max_line_height=pdf.font_size,
            )
        pdf.ln(line_height)

    pdf.output("table_with_cells.pdf")


if __name__ == '__main__':
    data = [["numero", "nom et prenom", "matier"], ["45", "RALAITSIMANOLAKAVANA Henri Franck ralaytsim", "lklskdjlfj"]]
    create_pdf(data)
