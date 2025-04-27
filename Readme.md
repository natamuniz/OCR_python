OCR Extrator de Metadados - Projeto Python

Este projeto realiza a extração automática de metadados (Nome, CPF, Data, Valor e Assunto) de documentos PDF usando OCR. Ele converte os PDFs em imagens, faz a leitura dos textos e gera arquivos JSON organizados para integrações futuras.

💡 Funcionalidades

Conversão de arquivos PDF para imagens.

Leitura de texto usando Tesseract OCR.

Extração de dados específicos via expressões regulares.

Geração automática de arquivos JSON com os metadados extraídos.

Tratamento de erros de OCR e conversão.

📝 Requisitos

Python 3.10+

Tesseract OCR instalado.

Poppler for Windows instalado.

Pacotes Python:

pdf2image

pytesseract

Para instalar os pacotes:

pip install pdf2image pytesseract

🔢 Configuração de Caminhos

Defina o caminho do Tesseract:

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

Defina o caminho do Poppler na função convert_from_path:

pages = convert_from_path(pdf_path, poppler_path=poppler_path)

📚 Como usar

1. Coloque seu PDF na pasta do projeto.

2. Altere o pdf_path para o nome do seu arquivo.

3. Execute o script.

4. O arquivo metadados_extraidos.json será gerado com os campos:

Nome

CPF

Data

Valor

Assunto

📊 Possíveis Melhorias Futuras

Processamento em lote de vários PDFs.

Integração automática com sistemas RDC-Arq ou AtoM.

Geração de CSV de relatório de erros.

Validação de OCR e qualidade do texto.

📢 Licença

Este projeto é de uso livre para fins educativos e comerciais.
