import sqlite3
import json


# Função para criar o banco de dados e as tabelas
def criar_banco_de_dados(nome_banco):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    # Criação das tabelas
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS eventos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        tipo TEXT NOT NULL
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS dados_eventos (
        id INTEGER PRIMARY KEY,
        data TEXT NOT NULL,
        localizacao TEXT NOT NULL
    )
    """
    )

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS metadados (
        id INTEGER PRIMARY KEY,
        descricao TEXT NOT NULL,
        link TEXT NOT NULL
    )
    """
    )

    conn.commit()
    conn.close()
    print(
        f"Banco de dados '{nome_banco}' criado com sucesso, com tabelas configuradas."
    )


# Função para carregar os dados do arquivo JSON
def carregar_dados_json(nome_arquivo):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)
        return dados["eventos"]
    except Exception as e:
        print(f"Erro ao carregar o arquivo JSON: {e}")
        return []


# Função para inserir os dados nas tabelas
def inserir_dados_no_banco(nome_banco, eventos):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()

    for evento in eventos:
        try:
            # Inserir na tabela eventos
            cursor.execute(
                """
            INSERT INTO eventos (id, nome, tipo)
            VALUES (?, ?, ?)
            """,
                (evento["id"], evento["nome"], evento["tipo"]),
            )

            # Inserir na tabela dados_eventos
            cursor.execute(
                """
            INSERT INTO dados_eventos (id, data, localizacao)
            VALUES (?, ?, ?)
            """,
                (
                    evento["id"],
                    evento["dados_evento"]["data"],
                    evento["dados_evento"]["localizacao"],
                ),
            )

            # Inserir na tabela metadados
            cursor.execute(
                """
            INSERT INTO metadados (id, descricao, link)
            VALUES (?, ?, ?)
            """,
                (
                    evento["id"],
                    evento["metadados"]["descricao"],
                    evento["metadados"]["link"],
                ),
            )

        except sqlite3.IntegrityError as e:
            print(f"Erro ao inserir dados: {e}")
            continue

    conn.commit()
    conn.close()
    print(f"Dados inseridos com sucesso no banco de dados '{nome_banco}'.")


# Função principal para executar o processo
def main():
    nome_banco = "eventos_culturais.db"
    nome_arquivo = "dados_culturais_html_atualizado.json"

    # Criar o banco de dados e as tabelas
    criar_banco_de_dados(nome_banco)

    # Carregar os dados do arquivo JSON
    eventos = carregar_dados_json(nome_arquivo)

    if eventos:
        # Inserir os dados no banco
        inserir_dados_no_banco(nome_banco, eventos)
    else:
        print("Nenhum dado encontrado no arquivo JSON.")


if __name__ == "__main__":
    main()
