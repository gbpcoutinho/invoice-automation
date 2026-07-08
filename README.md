# Raspagem de Dados - Protocolos de Reembolso (Bradesco Seguros)

Extrai dados de PDFs de "Protocolo de Solicitação de Reembolso" e consolida
tudo em uma planilha Excel.

## Campos extraídos

- SEGURADO
- Nº PROCESSO
- VALOR RECIBO
- NÚMERO DO CARTÃO
- PROCEDIMENTO
- DATA EVENTO
- DATA PROTOCOLO
- CPF

> Os campos **Nº NOTA FISCAL**, **Especialidade**, **PAGO EM** e **VALOR PAGO**
> não existem no modelo de PDF atual (protocolo de solicitação) e por isso
> ainda não são extraídos. Se você tiver PDFs de outro tipo de documento
> (ex: comprovante de pagamento) que contenham esses campos, é só enviar um
> exemplo para adaptarmos o extrator.

## Instalação

```bash
pip install -r requirements.txt
```

## Uso

1. Coloque os PDFs a processar dentro da pasta `pdfs_entrada/`.
2. Rode:

```bash
python processar_lote.py
```

3. A planilha é gerada em `saida/dados_extraidos_<data_hora>.xlsx`.

Também é possível especificar pastas customizadas:

```bash
python processar_lote.py caminho/para/pdfs caminho/para/saida.xlsx
```

## Testar um PDF isolado

```bash
python extrator.py caminho/para/arquivo.pdf
```
Imprime no terminal os campos extraídos daquele PDF, útil para depurar.

## Estrutura do projeto

```
.
├── extrator.py          # Lógica de extração de um único PDF
├── processar_lote.py    # Processa uma pasta inteira e gera o Excel
├── requirements.txt
├── pdfs_entrada/         # Coloque os PDFs aqui
└── saida/                # Planilhas geradas
```
