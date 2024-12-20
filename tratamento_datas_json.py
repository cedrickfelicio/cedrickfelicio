import json
from datetime import datetime

def converter_data(data):
    """Converte uma data no formato '12 de junho de 2024' para o formato ISO '2024-06-12'."""
    try:
        meses = {
            "janeiro": "01", "fevereiro": "02", "março": "03", "abril": "04", "maio": "05", "junho": "06",
            "julho": "07", "agosto": "08", "setembro": "09", "outubro": "10", "novembro": "11", "dezembro": "12"
        }
        partes = data.lower().split(" de ")
        dia = partes[0]
        mes = meses[partes[1]]
        ano = partes[2]
        return f"{ano}-{mes}-{int(dia):02d}"
    except Exception as e:
        print(f"Erro ao converter data: {data}. Detalhes: {e}")
        return data  # Retorna a data original em caso de falha

def atualizar_dados_json(input_file, output_file):
    """Atualiza as datas no arquivo JSON para o formato ISO e salva em um novo arquivo."""
    try:
        with open(input_file, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        for evento in dados.get("eventos", []):
            if "dados_evento" in evento and "data" in evento["dados_evento"]:
                evento["dados_evento"]["data"] = converter_data(evento["dados_evento"]["data"])

        with open(output_file, 'w', encoding='utf-8') as arquivo_atualizado:
            json.dump(dados, arquivo_atualizado, ensure_ascii=False, indent=4)

        print(f"Conversão concluída. Arquivo salvo como '{output_file}'.")
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

def main():
    input_file = 'dados_culturais_html_todas_paginas.json'
    output_file = 'dados_culturais_html_atualizado.json'
    atualizar_dados_json(input_file, output_file)

if __name__ == "__main__":
    main()
