import urllib.request
from bs4 import BeautifulSoup
import json
import re


# função para baixar o conteúdo HTML da página
def baixar_html(url):
    try:
        response = urllib.request.urlopen(url)
        html_content = response.read().decode("utf-8")
        return html_content
    except Exception as e:
        print(f"Erro ao acessar a URL: {e}")
        return None


# função para extrair informações específicas de eventos culturais no site
def extrair_dados(html_content, id_inicial):
    soup = BeautifulSoup(html_content, "html.parser")
    eventos = []
    id_atual = id_inicial

    # procura todos os artigos na página
    artigos = soup.find_all("article", class_="row d-flex align-items-center")
    for artigo in artigos:
        try:
            # extrai o título do evento
            titulo_tag = artigo.find("h6")
            link_tag = titulo_tag.find("a") if titulo_tag else None
            nome_evento = (
                link_tag.get("title", "Título não encontrado")
                if link_tag
                else "Título não encontrado"
            )
            link_evento = link_tag["href"] if link_tag else "Link não encontrado"

            # extrai a descrição do evento
            descricao_tag = artigo.find("p")
            descricao_evento = (
                descricao_tag.get_text(strip=True)
                if descricao_tag
                else "Descrição não encontrada"
            )

            # extrai a data do evento
            data_tag = artigo.find("time")
            data_evento = (
                data_tag.get_text(strip=True) if data_tag else "Data não especificada"
            )

            # adiciona o evento à lista
            eventos.append(
                {
                    "id": id_atual,
                    "nome": nome_evento,
                    "tipo": "Cultura",  # Tipo fixo com base no contexto
                    "dados_evento": {
                        "data": data_evento,
                        "localizacao": "São Paulo, Itararé",
                    },
                    "metadados": {"descricao": descricao_evento, "link": link_evento},
                }
            )
            id_atual += 1
        except AttributeError:
            continue

    return eventos, id_atual


# função para salvar os dados no formato JSON
def salvar_json(eventos, nome_arquivo):
    try:
        data = {"eventos": eventos}
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Dados salvos no arquivo JSON: {nome_arquivo}")
    except Exception as e:
        print(f"Erro ao salvar JSON: {e}")


# função principal para processar todas as páginas e extrair os eventos
def processar_todas_as_paginas(base_url):
    print("Processando todas as páginas de eventos...")
    eventos_totais = []
    id_atual = 1
    pagina_atual = 1

    # loop para percorrer todas as páginas que contém os eventos
    while True:
        url = f"{base_url}/page/{pagina_atual}/" if pagina_atual > 1 else base_url
        print(f"Baixando conteúdo da página: {url}")
        html_content = baixar_html(url)

        if not html_content:
            print("Falha ao obter o conteúdo HTML. Encerrando coleta.")
            break

        eventos, id_atual = extrair_dados(html_content, id_atual)
        if not eventos:
            print(
                f"Sem eventos encontrados na página {pagina_atual}. Parando a coleta."
            )
            break

        eventos_totais.extend(eventos)
        pagina_atual += 1

    if eventos_totais:
        print("Salvando dados no formato JSON...")
        salvar_json(eventos_totais, "dados_culturais_html_todas_paginas.json")
    else:
        print("Nenhum dado foi extraído de nenhuma página.")


# executa o script
def main():
    base_url = "https://itarare.sp.gov.br/categorias/cultura"
    processar_todas_as_paginas(base_url)


if __name__ == "__main__":
    main()
