import requests
import os
import sys
from datetime import datetime, timezone
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

    response = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_search",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=query,
        verify=False
    )

    return response.status_code == 200 and response.json()["hits"]["total"]["value"] > 0

def criar_documento(ip, comentario):
    now = datetime.now(timezone.utc).isoformat()
    doc = {
        "@timestamp": now,
        "data_escaneamento": now,
        "ip": ip,
        "status_online": None,
        "excecao": True,
        "comentario": comentario,
        "host_ja_scan": False,
        "notificado": False,
        "erro": None,
        "nmap_resultado": {"os": None, "cpe": []},
        "nbtscan_resultado": {"hostname": None, "mac": None}
    }

    response = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_doc/",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=doc,
        verify=False
    )

    if response.status_code in (200, 201):
        print(f"✅ IP {ip} criado e marcado como exceção.")
    else:
        print(f"❌ Falha ao criar IP {ip}: {response.text}")

def aplicar_excecao(ip, comentario):
    if not ip_existe(ip):
        criar_documento(ip, comentario)
        return

    doc = {
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
        json=doc,
        verify=False
    )

    if response.status_code == 200:
        print(f"✅ IP {ip} marcado como exceção com comentário: {comentario}")
    else:
        print(f"❌ Erro ao aplicar exceção para {ip}: {response.text}")

def main():
    if len(sys.argv) != 3:
        print("Uso: python3 adicionar_excecao_manual.py <IP> <comentario>")
        return

    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        return

    ip = sys.argv[1]
    comentario = sys.argv[2]
    aplicar_excecao(ip, comentario)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
