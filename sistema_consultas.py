import sqlite3
from datetime import datetime
import csv

# função para mostrar todos os eventos com suas datas, localização e tipo de evento
def consultar_todos_eventos(nome_banco):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    query = """
    SELECT eventos.nome, dados_eventos.data, dados_eventos.localizacao, eventos.tipo
    FROM eventos
    JOIN dados_eventos ON eventos.id = dados_eventos.id
    """

    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# função para mostrar os 2 eventos mais próximos de iniciar (Considera data atual 01/01/2024)
def consultar_eventos_proximos(nome_banco):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    data_atual = "2024-01-01"

    query = """
    SELECT eventos.nome, dados_eventos.data, dados_eventos.localizacao
    FROM eventos
    JOIN dados_eventos ON eventos.id = dados_eventos.id
    WHERE date(dados_eventos.data) >= ?
    ORDER BY date(dados_eventos.data) ASC
    LIMIT 2
    """

    cursor.execute(query, (data_atual,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# função para mostrar os eventos que acontecem na localização São Paulo, Itararé
def consultar_eventos_em_itarare(nome_banco):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    query = """
    SELECT eventos.nome, dados_eventos.data, dados_eventos.localizacao
    FROM eventos
    JOIN dados_eventos ON eventos.id = dados_eventos.id
    WHERE dados_eventos.localizacao = "São Paulo, Itararé"
    """

    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# função para mostrar os eventos ao ar livre (contendo palavras-chave específicas na descrição)
def consultar_eventos_ao_ar_livre(nome_banco):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    palavras_chave = ["Parque", "Praça", "Nações"]
    condicoes = " OR ".join(
        [f"metadados.descricao LIKE '%{palavra}%'" for palavra in palavras_chave]
    )

    query = f"""
    SELECT eventos.nome, dados_eventos.data, metadados.descricao
    FROM eventos
    JOIN metadados ON eventos.id = metadados.id
    JOIN dados_eventos ON eventos.id = dados_eventos.id
    WHERE {condicoes}
    """

    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# função para mostrar todos os metadados por evento
def consultar_todos_metadados(nome_banco):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    query = """
    SELECT eventos.nome, metadados.descricao, metadados.link
    FROM eventos
    JOIN metadados ON eventos.id = metadados.id
    """

    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()
    return resultados

# função para salvar resultados em um arquivo CSV
def salvar_csv(nome_arquivo, cabecalhos, resultados):
    try:
        with open(nome_arquivo, mode="w", encoding="utf-8", newline="") as arquivo:
            escritor = csv.writer(arquivo)
            escritor.writerow(cabecalhos)  # Escreve os cabeçalhos
            escritor.writerows(resultados)  # Escreve os dados
        print(f"Arquivo CSV '{nome_arquivo}' criado com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")

# sistema interativo
def sistema_interativo(nome_banco):
    while True:
        print("\nSelecione uma consulta para realizar:")
        print(
            "1 - Mostrar todos os eventos com suas datas, localização e tipo de evento"
        )
        print("2 - Mostrar os 2 eventos mais próximos de iniciar")
        print("3 - Mostrar eventos que acontecem na localização São Paulo, Itararé")
        print("4 - Mostrar eventos ao ar livre")
        print("5 - Mostrar todos os metadados por evento")
        print("6 - Gerar CSV de uma consulta")
        print("7 - Sair")

        escolha = input("Digite o número da consulta desejada: ")

        if escolha == "1":
            resultados = consultar_todos_eventos(nome_banco)
            print("\nEventos:")
            for resultado in resultados:
                print(
                    f"Nome: {resultado[0]} | Data: {resultado[1]} | Localização: {resultado[2]} | Tipo: {resultado[3]}"
                )
        elif escolha == "2":
            resultados = consultar_eventos_proximos(nome_banco)
            print("\nPróximos Eventos:")
            for resultado in resultados:
                print(
                    f"Nome: {resultado[0]} | Data: {resultado[1]} | Localização: {resultado[2]}"
                )
        elif escolha == "3":
            resultados = consultar_eventos_em_itarare(nome_banco)
            print("\nEventos em São Paulo, Itararé:")
            for resultado in resultados:
                print(
                    f"Nome: {resultado[0]} | Data: {resultado[1]} | Localização: {resultado[2]}"
                )
        elif escolha == "4":
            resultados = consultar_eventos_ao_ar_livre(nome_banco)
            print("\nEventos ao Ar Livre:")
            for resultado in resultados:
                print(
                    f"Nome: {resultado[0]} | Data: {resultado[1]} | Descrição: {resultado[2]}"
                )
        elif escolha == "5":
            resultados = consultar_todos_metadados(nome_banco)
            print("\nMetadados por Evento:")
            for resultado in resultados:
                print(
                    f"Nome: {resultado[0]} | Descrição: {resultado[1]} | Link: {resultado[2]}"
                )
        elif escolha == "6":
            print("\nSelecione a consulta para gerar o CSV:")
            print("1 - Todos os eventos")
            print("2 - Próximos eventos")
            print("3 - Eventos em São Paulo, Itararé")
            print("4 - Eventos ao ar livre")
            print("5 - Metadados por evento")

            escolha_csv = input("Digite o número da consulta desejada: ")

            if escolha_csv == "1":
                resultados = consultar_todos_eventos(nome_banco)
                salvar_csv("todos_eventos.csv", ["Nome", "Data", "Localização", "Tipo"], resultados)
            elif escolha_csv == "2":
                resultados = consultar_eventos_proximos(nome_banco)
                salvar_csv("proximos_eventos.csv", ["Nome", "Data", "Localização"], resultados)
            elif escolha_csv == "3":
                resultados = consultar_eventos_em_itarare(nome_banco)
                salvar_csv("eventos_em_itarare.csv", ["Nome", "Data", "Localização"], resultados)
            elif escolha_csv == "4":
                resultados = consultar_eventos_ao_ar_livre(nome_banco)
                salvar_csv("eventos_ao_ar_livre.csv", ["Nome", "Data", "Descrição"], resultados)
            elif escolha_csv == "5":
                resultados = consultar_todos_metadados(nome_banco)
                salvar_csv("todos_metadados.csv", ["Nome", "Descrição", "Link"], resultados)
            else:
                print("Opção inválida para geração de CSV.")
        elif escolha == "7":
            print("Saindo do sistema. Até mais!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# executa o script
def main():
    nome_banco = "eventos_culturais.db"
    sistema_interativo(nome_banco)

if __name__ == "__main__":
    main()
