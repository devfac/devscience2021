from pdfme import build_pdf

document = {}

def create_certificat(num_carte: str) -> str:
    document['style'] = {
    'margin_bottom': 15,
    'text_align': 'j'
    }

    with open('document.pdf', 'wb') as f:
        build_pdf(document, f)

if __name__ =="__main__":
    create_certificat("4465")