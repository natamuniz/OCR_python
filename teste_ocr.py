from pdf2image import convert_from_path

pdf_path = "C:\\Users\\natan\OneDrive\\Área de Trabalho\\testeOcr\\pdf_teste_ocr.pdf"
poppler_path = "C:\\poppler\\poppler-24.08.0\\Library\\bin"

# Teste: converte o PDF em imagens
pages = convert_from_path(pdf_path, poppler_path=poppler_path)

# Salva a primeira página como imagem de teste
pages[0].save("pagina1.png", "PNG")
print("PDF convertido com sucesso para imagem!")

import pytesseract
import re
import json

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Faz OCR na imagem gerada
texto = pytesseract.image_to_string("pagina1.png", lang="eng")  # Usa português

# Extrai informações usando regex
nome = re.search(r"Nome:\s*(.+)", texto)
cpf = re.search(r"CPF:\s*([\d\.\-]+)", texto)
data = re.search(r"Data:\s*(\d{2}/\d{2}/\d{4})", texto)
valor = re.search(r"R\$[\s]*([\d\.,]+)", texto)

# Monta um dicionário com os dados extraídos
metadados = {
    "nome": nome.group(1).strip() if nome else None,
    "cpf": cpf.group(1).strip() if cpf else None,
    "data": data.group(1).strip() if data else None,
    "valor": valor.group(1).strip() if valor else None
}

# Salva os metadados em JSON
with open("metadados_extraidos.json", "w", encoding="utf-8") as f:
    json.dump(metadados, f, indent=4, ensure_ascii=False)

print("✅ OCR concluído!")
print("✅ Metadados extraídos e salvos no arquivo 'metadados_extraidos.json'.")

# Mostrar os dados extraídos no terminal
print("\n📄 Dados extraídos:")
for chave, valor in metadados.items():
    print(f"{chave.capitalize()}: {valor if valor else 'Não encontrado'}")
