# generierenPDF.py

from fpdf import FPDF

def gerar_pdf(valores, caminho_pdf='relatorio_angulos.pdf', caminho_imagem='grafico.png'):
    """Gera o relatório PDF"""

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, 'Relatório de Análise de Ângulos', ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.ln(10)

    # Joelho
    pdf.cell(0, 10, f"Joelho - Min: {valores['joelho']['min']:.2f} | Max: {valores['joelho']['max']:.2f}", ln=True)
    pdf.cell(0, 10, f"Joelho - Mediana Min: {valores['joelho']['mediana_min']:.2f} | Mediana Max: {valores['joelho']['mediana_max']:.2f}", ln=True)

    pdf.ln(5)

    # Tornozelo
    pdf.cell(0, 10, f"Tornozelo - Min: {valores['tornozelo']['min']:.2f} | Max: {valores['tornozelo']['max']:.2f}", ln=True)
    pdf.cell(0, 10, f"Tornozelo - Mediana Min: {valores['tornozelo']['mediana_min']:.2f} | Mediana Max: {valores['tornozelo']['mediana_max']:.2f}", ln=True)

    pdf.ln(10)
    pdf.image(caminho_imagem, x=10, w=190)
    pdf.output(caminho_pdf)
    
    
    

