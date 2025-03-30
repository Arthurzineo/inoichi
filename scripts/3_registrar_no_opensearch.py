import requests
import os
from datetime import datetime, timezone
from requests.auth import HTTPBasicAuth

ARQUIVO_IPS = "/inoichi/temp/resultado_filtrado.txt"

OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")
TOKEN = "0"  # coloque seu token aqui
CHAT_ID = "0"  # coloque seu chat_id aqui

def enviar_alerta(mensagem):
    if TOKEN != "0":
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": mensagem
        }

        response = requests.post(url, json=payload)

        if response.status_code != 200:
            print(f"❌ Erro ao enviar mensagem: {response.text}")
        else:
            print("✅ Alerta enviado para o Telegram!")

def carregar_ips(caminho):
    with open(caminho, "r") as f:
        return [linha.strip() for linha in f if linha.strip()]

def ip_ja_existe(ip):
    query = {
        "size": 1,
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

    if response.status_code != 200:
        print(f"⚠️ Erro ao verificar duplicidade do IP {ip}: {response.text}")
        return True  
    hits = response.json().get("hits", {}).get("total", {}).get("value", 0)
    return hits > 0

def adicionar_documento(ip):
    if ip_ja_existe(ip):
        return

    now = datetime.now(timezone.utc).isoformat()

    doc = {
        "@timestamp": now,
        "data_escaneamento": now,
        "ip": ip,
        "status_online": None,
        "excecao": False,
        "comentario": "",
        "host_ja_scan": False,
        "notificado": False,
        "erro": None,
        "nmap_resultado": {
            "os": None
        },
        "nbtscan_resultado": {
            "hostname": None,
            "mac": None
        }
    }

    response = requests.post(
        f"{OPENSEARCH_URL}/{INDEX_NAME}/_doc/",
        auth=HTTPBasicAuth(USERNAME, PASSWORD),
        headers={"Content-Type": "application/json"},
        json=doc,
        verify=False
    )

    if response.status_code not in (200, 201):
        print(f"⚠️  Falha ao inserir IP {ip}: {response.text}")
    else:
        print(f"✅ IP {ip} registrado com sucesso.")


def main():
    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        return

    ips = carregar_ips(ARQUIVO_IPS)
    enviar_alerta(f"📡 {len(ips)} IPs novos identificados!")
    for ip in ips:
        adicionar_documento(ip)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
