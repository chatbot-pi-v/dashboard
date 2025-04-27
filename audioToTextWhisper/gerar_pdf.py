from fpdf import FPDF

def salvar_pdf(texto, caminho_saida):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for linha in texto.split("\n"):
        pdf.multi_cell(0, 10, linha)
    pdf.output(caminho_saida)
