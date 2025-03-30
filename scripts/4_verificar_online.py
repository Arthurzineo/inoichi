import subprocess
import os
import requests
from concurrent.futures import ThreadPoolExecutor
from requests.auth import HTTPBasicAuth

OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")
TOKEN = "0"
CHAT_ID = "0"

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

def buscar_ips_no_opensearch():
    query = {
        "size": 10000,
        "_source": ["ip"],
        "query": {
            "bool": {
                "must_not": [
                    {"term": {"excecao": True}}
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
    
def ping_host(ip):
    try:
        resultado = subprocess.run(
            ["ping", "-c", "1", "-W", "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return ip, resultado.returncode == 0
    except Exception:
        return ip, False

def atualizar_status_online(ip, status):
    script = {
        "script": {
            "source": "ctx._source.status_online = params.status",
            "lang": "painless",
            "params": {"status": status}
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

    if response.status_code != 200:
        print(f"⚠️ Erro ao atualizar IP {ip}: {response.text}")
    else:
        print(f"✅ IP {ip} atualizado como {'online' if status else 'offline'}.")

def main():
    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        return

    print("🔍 Buscando IPs no OpenSearch...")
    ips = buscar_ips_no_opensearch()

    if not ips:
        print("⚠️ Nenhum IP encontrado para verificar.")
        return

    print(f"☑️ Verificando {len(ips)} IPs com ping...")
    online_ips = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        for ip, status in executor.map(ping_host, ips):
            atualizar_status_online(ip, status)
            if status:
                online_ips.append(ip)

    if online_ips:
        lista = "\n".join(f"• {ip}" for ip in online_ips)
        mensagem = f"🟢 Hosts online identificados ({len(online_ips)}):\n{lista}"
        enviar_alerta(mensagem)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
