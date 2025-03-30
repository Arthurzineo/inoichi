
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")

def remover_documento(ip):
    query = {
        "query": {
            "term": {
                "ip": ip
            }
        }
    }

    response = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_delete_by_query",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=query,
        verify=False
    )

    if response.status_code == 200:
        print(f"🗑️ IP {ip} removido do índice com sucesso.")
    else:
        print(f"❌ Erro ao remover IP {ip}: {response.text}")

def main():
    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        return

    if len(sys.argv) != 2:
        print("Uso: python3 remover_ip.py <IP>")
        return

    ip = sys.argv[1]
    remover_documento(ip)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
