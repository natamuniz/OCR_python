from pdf2image import convert_from_path
import pytesseract
import re
import os
import csv
from tqdm import tqdm  # Biblioteca para a barra de progresso
from concurrent.futures import ThreadPoolExecutor  # Para processamento paralelo

# Caminho da pasta com os PDFs
pdf_folder = "D:\\UENF\\1- ORGANIZADO\\13.12.08.40\\2019\\UENF - FORNECEDORES - CAIXA B -2019"
poppler_path = "C:\\Program Files\\poppler\\poppler-24.08.0\\Library\\bin"

# Caminho do executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Inicializa uma lista para armazenar os metadados de todos os PDFs
metadados_totais = []

# Lista de arquivos PDF na pasta
pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]

# Função para processar um único PDF
def process_pdf(pdf_file):
    pdf_path = os.path.join(pdf_folder, pdf_file)
    print(f"\n🔍 Processando: {pdf_file}")

    # Extrai o número do processo diretamente do nome do arquivo
    processo = os.path.splitext(pdf_file)[0]  # Remove a extensão do arquivo

    # Converte o PDF em imagens com DPI reduzido
    pages = convert_from_path(pdf_path, poppler_path=poppler_path, dpi=150)

    # Inicializa os dados do arquivo atual
    data_encontrada = None
    assunto_encontrado = None
    autor_encontrado = None

    # Itera sobre todas as páginas do PDF
    for i, page in enumerate(pages):
        # Realiza OCR diretamente na imagem da página com configuração otimizada
        texto = pytesseract.image_to_string(page, lang="por", config="--psm 6 --oem 1")

        # Extrai informações usando regex
        data = re.search(r"Data: \s*(\d{2}/\d{2}/\d{4})", texto)
        assunto = re.search(r"Assunto:\s*(.+)", texto)
        autor = re.search(r"De:\s*(.+)", texto)  # Regex para encontrar o autor

        # Se encontrar os dados, armazena e pula para o próximo PDF
        if data or assunto or autor:
            data_encontrada = data.group(1).strip() if data else None
            assunto_encontrado = assunto.group(1).strip() if assunto else None
            autor_encontrado = autor.group(1).strip() if autor else None
            print(f"✅ Dados encontrados no arquivo {pdf_file}, página {i + 1}. Pulando para o próximo PDF.")
            break  # Pula para o próximo PDF

    # Retorna os metadados do arquivo atual
    return {
        "arquivo": pdf_file,
        "processo": processo,
        "data": data_encontrada,
        "assunto": assunto_encontrado,
        "autor": autor_encontrado
    }

# Processa os PDFs em paralelo
with ThreadPoolExecutor() as executor:
    metadados_totais = list(tqdm(executor.map(process_pdf, pdf_files), total=len(pdf_files), desc="Processando PDFs"))

# Define o nome do arquivo CSV com base no nome da pasta
csv_file_name = os.path.basename(pdf_folder.rstrip("\\"))
csv_file_path = os.path.join(pdf_folder, f"{csv_file_name}.csv")

# Salva os metadados encontrados em um arquivo CSV na mesma pasta dos PDFs
with open(csv_file_path, mode="w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["arquivo", "processo", "data", "assunto", "autor"])
    writer.writeheader()
    writer.writerows(metadados_totais)

print("\n✅ OCR concluído!")
print(f"✅ Metadados extraídos e salvos no arquivo '{csv_file_path}'.")