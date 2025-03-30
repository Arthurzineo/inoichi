import requests
from requests.auth import HTTPBasicAuth
import os

OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")



def carregar_ips_resultado(caminho):
    with open(caminho, "r") as f:
        return set(linha.strip() for linha in f if linha.strip())

def salvar_ips(lista, caminho):
    with open(caminho, "w") as f:
        for ip in sorted(lista):
            f.write(ip + "\n")

def buscar_ips_excecao():
    query = {
        "size": 10000,
        "_source": ["ip"],
        "query": {
            "term": {
                "excecao": True
            }
        }
    }

    response = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_search",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=query,
        verify=False  
    )

    if response.status_code != 200:
        print(f"⚠️ Falha ao consultar o OpenSearch: {response.text}")
        return set()

    dados = response.json()
    ips = {hit["_source"]["ip"] for hit in dados["hits"]["hits"] if "ip" in hit["_source"]}
    return ips

def main():
    path_resultado = "/inoichi/temp/resultado.txt"
    path_saida = "/inoichi/temp/resultado_filtrado.txt"

    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        return

    lista_ips = carregar_ips_resultado(path_resultado)
    lista_excecoes = buscar_ips_excecao()
    lista_filtrada = lista_ips - lista_excecoes

    salvar_ips(lista_filtrada, path_saida)
    print(f"✅ {len(lista_filtrada)} IPs salvos em {path_saida} (exceções removidas)")
    
if __name__ == "__main__":
    import os
    import urllib3
    urllib3.disable_warnings() 
    main()
