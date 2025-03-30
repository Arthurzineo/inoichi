import csv
import os
import sys
import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth

OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")

def ip_existe(ip):
    query = {
        "query": {
            "term": {
                "ip": ip
            }
        }
    }

    response = requests.get(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_search",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=query,
        verify=False
    )

    if response.status_code == 200:
        result = response.json()
        return result["hits"]["total"]["value"] > 0
    else:
        print(f"❌ Erro ao verificar IP {ip}: {response.text}")
        return False

def atualizar_ip(ip, comentario):
    script = {
        "script": {
            "source": """
                ctx._source.excecao = true;
                ctx._source.comentario = params.comentario;
            """,
            "lang": "painless",
            "params": {
                "comentario": comentario
            }
        },
        "query": {
            "term": {
                "ip": ip
            }
        }
    }

    response = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_update_by_query",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=script,
        verify=False
    )

    if response.status_code == 200:
        print(f"✅ IP {ip} atualizado com exceção: {comentario}")
    else:
        print(f"❌ Erro ao atualizar IP {ip}: {response.text}")

def criar_ip(ip, comentario):
    doc = {
        "ip": ip,
        "excecao": True,
        "comentario": comentario,
        "timestamp": datetime.utcnow().isoformat()
    }

    response = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_doc",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=doc,
        verify=False
    )

    if response.status_code in [200, 201]:
        print(f"🆕 IP {ip} criado com exceção: {comentario}")
    else:
        print(f"❌ Erro ao criar IP {ip}: {response.text}")

def aplicar_excecao(ip, comentario):
    if ip_existe(ip):
        atualizar_ip(ip, comentario)
    else:
        criar_ip(ip, comentario)

def processar_csv(caminho):
    try:
        with open(caminho, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for linha in reader:
                if len(linha) >= 2:
                    ip = linha[0].strip()
                    comentario = linha[1].strip()
                    aplicar_excecao(ip, comentario)
    except Exception as e:
        print(f"⚠️ Erro ao ler o arquivo CSV: {e}")

def main():
    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        return

    if len(sys.argv) != 2:
        print("Uso: python3 adicionar_excecoes_csv.py <caminho_para_csv>")
        return

    caminho_csv = sys.argv[1]
    processar_csv(caminho_csv)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
