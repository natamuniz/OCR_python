from pdf2image import convert_from_path

pdf_path = "C:\\Users\\natan\OneDrive\\Área de Trabalho\\testeOcr\\pdf_teste_ocr.pdf"
poppler_path = "C:\\poppler\\poppler-24.08.0\\Library\\bin"

# Teste: converte o PDF em imagens
pages = convert_from_path(pdf_path, poppler_path=poppler_path)

# Salva a primeira página como imagem de teste
pages[0].save("pagina1.png", "PNG")
print("PDF convertido com sucesso para imagem!")
