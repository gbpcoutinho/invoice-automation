"""
extrator.py

Extrai os campos de PDFs de "Protocolo de Solicitação de Reembolso" (Bradesco Seguros).

Campos extraídos:
    - Nº PROCESSO   (número do protocolo, código de barras)
    - SEGURADO
    - CPF
    - NÚMERO DO CARTÃO
    - PROCEDIMENTO
    - VALOR RECIBO  (valor total solicitado)
    - DATA EVENTO   (data do procedimento)
    - DATA PROTOCOLO (data de recepção)

Campos que o modelo atual de PDF não possui e por isso NÃO são extraídos
(deixados de fora por enquanto, conforme decidido):
    - Nº NOTA FISCAL
    - Especialidade
    - PAGO EM
    - VALOR PAGO

Se você tiver PDFs de outro layout (ex: comprovante de pagamento com esses
campos), me envie um exemplo que eu adapto o extrator.
"""

import re
from pathlib import Path

import pdfplumber

# Colunas de saída, na ordem desejada
COLUNAS_SAIDA = [
    "ARQUIVO",
    "SEGURADO",
    "Nº PROCESSO",
    "VALOR RECIBO",
    "NÚMERO DO CARTÃO",
    "PROCEDIMENTO",
    "DATA EVENTO",
    "DATA PROTOCOLO",
    "CPF",
]


def _texto_do_pdf(caminho_pdf: str) -> str:
    """Extrai o texto de todas as páginas preservando o layout (colunas)."""
    with pdfplumber.open(caminho_pdf) as pdf:
        paginas = [p.extract_text(layout=True) or "" for p in pdf.pages]
    return "\n".join(paginas)


def _buscar(padrao: str, texto: str):
    m = re.search(padrao, texto, re.MULTILINE)
    return m.groups() if m else None


def extrair_dados_pdf(caminho_pdf: str) -> dict:
    """
    Recebe o caminho de um PDF de protocolo de reembolso e devolve um dicionário
    com os campos extraídos. Campos não encontrados voltam como None.
    """
    texto = _texto_do_pdf(caminho_pdf)
    dados = {coluna: None for coluna in COLUNAS_SAIDA}
    dados["ARQUIVO"] = Path(caminho_pdf).name

    # Nº PROCESSO (código de barras / nº do protocolo, 16 dígitos)
    r = _buscar(r"(\d{16})", texto)
    if r:
        dados["Nº PROCESSO"] = r[0]

    # SEGURADO (nome que aparece logo abaixo do rótulo "Segurado ... Cartão ... Tipo:")
    r = _buscar(
        r"Segurado\s+Cart[ãa]o\s+Tipo:?\s*\n\s*(.+?)\s+\d{3}\s\d{3}\s\d{6}\s\d{2}\s\d",
        texto,
    )
    if r:
        dados["SEGURADO"] = r[0].strip()

    # CPF (primeiro CPF encontrado no documento)
    r = _buscar(r"(\d{3}\.\d{3}\.\d{3}-\d{2})", texto)
    if r:
        dados["CPF"] = r[0]

    # NÚMERO DO CARTÃO (primeiro cartão encontrado no documento)
    r = _buscar(r"(\d{3}\s\d{3}\s\d{6}\s\d{2}\s\d)", texto)
    if r:
        dados["NÚMERO DO CARTÃO"] = r[0]

    # PROCEDIMENTO + VALOR RECIBO (valor total solicitado)
    r = _buscar(
        r"Procedimento\s+Qtd\.\s+Documentos\s+Entregues\s+Valor total solicitado\s*\n\s*"
        r"(.+?)\s+(\d+)\s+([\d.,]+)\s*\n",
        texto,
    )
    if r:
        dados["PROCEDIMENTO"] = r[0].strip()
        dados["VALOR RECIBO"] = r[2].replace(".", "").replace(",", ".")

    # DATA PROTOCOLO (data de recepção) e DATA EVENTO (data do procedimento)
    r = _buscar(
        r"Sucursal de Entrada\s+Data de recep[çc][ãa]o\s+Data do Procedimento\s+"
        r"(.+?)\s+(\d{2}/\d{2}/\d{4})\s+(\d{2}/\d{2}/\d{4})",
        texto,
    )
    if r:
        dados["DATA PROTOCOLO"] = r[1]
        dados["DATA EVENTO"] = r[2]

    return dados


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python extrator.py caminho_do_pdf.pdf")
        sys.exit(1)

    resultado = extrair_dados_pdf(sys.argv[1])
    for campo, valor in resultado.items():
        print(f"{campo}: {valor}")
