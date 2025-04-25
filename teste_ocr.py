from pdf2image import convert_from_path
import pytesseract
import re

# Caminho do executável do Tesseract no seu PC
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Caminho do PDF de teste (certifique-se que está na mesma pasta do script ou coloque o caminho completo)
pdf_path = "C:\Users\natan\OneDrive\Área de Trabalho\testeOcr\pdf_teste_ocr.pdf"

# Caminho do Poppler no seu computador
poppler_path = r"C:\poppler\poppler-24.08.0\Library\bin"

# Converte o PDF em imagens usando poppler direto
pages = convert_from_path(pdf_path, poppler_path=poppler_path)

# OCR nas páginas
texto_total = ""
for page in pages:
    texto = pytesseract.image_to_string(page, lang="por")  # ou 'eng' se português não estiver instalado
    texto_total += texto + "\n"

# Extração de metadados simples (exemplo com regex)
nome = re.search(r"Nome:\s*(.+)", texto_total)
cpf = re.search(r"CPF:\s*([\d\.\-]+)", texto_total)
data = re.search(r"Data:\s*(\d{2}/\d{2}/\d{4})", texto_total)
valor = re.search(r"R\$[\s]*([\d\.,]+)", texto_total)

print("Texto completo extraído:\n")
print(texto_total)

print("\nMetadados extraídos:")
print("Nome:", nome.group(1) if nome else "Não encontrado")
print("CPF:", cpf.group(1) if cpf else "Não encontrado")
print("Data:", data.group(1) if data else "Não encontrada")
print("Valor:", valor.group(1) if valor else "Não encontrado")
