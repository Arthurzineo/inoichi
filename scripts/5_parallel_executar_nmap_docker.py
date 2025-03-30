import requests
import os
import subprocess
from requests.auth import HTTPBasicAuth

TMP_LIST = "/inoichi/temp/ips_para_nmap.txt"
OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")

def buscar_ips_para_nmap():
    query = {
        "size": 10000,
        "_source": ["ip"],
        "query": {
            "bool": {
                "must": [
                    {"term": {"status_online": True}}
                ],
                "must_not": [
                    {"term": {"host_ja_scan": True}}
                ]
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
        print(f"⚠️ Erro ao buscar IPs: {response.text}")
        return []

    resultado = response.json()
    return [hit["_source"]["ip"] for hit in resultado["hits"]["hits"]]

def salvar_lista_para_parallel(ips):
    with open(TMP_LIST, "w") as f:
        for ip in sorted(ips):
            f.write(ip + "\n")

def executar_parallel():
    print("⚙️ Executando Nmap com parallel + docker...")
    cmd = f"parallel -j 10 'python3 5_executar_nmap_docker.py {{}}' :::: {TMP_LIST}"
    subprocess.run(cmd, shell=True)

def main():
    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        return

    ips = buscar_ips_para_nmap()

    if not ips:
        print("⚠️ Nenhum IP disponível para escaneamento. nmap.")
        return

    salvar_lista_para_parallel(ips)
    executar_parallel()

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
