from pdf2image import convert_from_path
import easyocr
import re
import os
import csv
from tqdm import tqdm  # Biblioteca para a barra de progresso
from concurrent.futures import ThreadPoolExecutor  # Para processamento paralelo

# Caminho da pasta com os PDFs
pdf_folder = "C:\\Users\\paulo\\Desktop\\PASTA TESTE\\UENF CAIXA A-2002"
poppler_path = "C:\\Program Files\\poppler\\poppler-24.08.0\\Library\\bin"

# Inicializa o leitor do EasyOCR
reader = easyocr.Reader(['pt', 'en'], gpu=False)

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

    # Itera sobre todas as páginas do PDF
    for i, page in enumerate(pages):
        # Salva a página como imagem temporária
        temp_image_path = os.path.join(os.getcwd(), f"_temp_page_{i + 1}.png")
        page.save(temp_image_path, "PNG")

        # Realiza OCR com EasyOCR
        resultados = reader.readtext(temp_image_path, detail=0)
        texto = "\n".join(resultados)

        # Remove imagem temporária
        os.remove(temp_image_path)

        # Extrai informações usando regex
        data = re.search(r"Data\s*(\d{2}/\d{2}/\d{4})", texto)
        assunto = re.search(r"Assunto:\s*(.+)", texto)

        # Se encontrar os dados, armazena e pula para o próximo PDF
        if data or assunto:
            data_encontrada = data.group(1).strip() if data else None
            assunto_encontrado = assunto.group(1).strip() if assunto else None
            print(f"✅ Dados encontrados no arquivo {pdf_file}, página {i + 1}. Pulando para o próximo PDF.")
            break  # Pula para o próximo PDF

    # Retorna os metadados do arquivo atual
    return {
        "arquivo": pdf_file,
        "processo": processo,
        "data": data_encontrada,
        "assunto": assunto_encontrado
    }

# Processa os PDFs em paralelo
with ThreadPoolExecutor() as executor:
    metadados_totais = list(tqdm(executor.map(process_pdf, pdf_files), total=len(pdf_files), desc="Processando PDFs"))

# Define o nome do arquivo CSV com base no nome da pasta
csv_file_name = os.path.basename(pdf_folder.rstrip("\\"))
csv_file_path = os.path.join(pdf_folder, f"{csv_file_name}.csv")

# Salva os metadados encontrados em um arquivo CSV na mesma pasta dos PDFs
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["arquivo", "processo", "data", "assunto"])
    writer.writeheader()
    writer.writerows(metadados_totais)

print("\n✅ OCR concluído!")
print(f"✅ Metadados extraídos e salvos no arquivo '{csv_file_path}'.")
