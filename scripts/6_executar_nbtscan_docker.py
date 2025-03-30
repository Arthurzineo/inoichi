import subprocess
import sys
import os
import re
import requests
from datetime import datetime, timezone
from requests.auth import HTTPBasicAuth

OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")

OUTPUT_DIR = "/inoichi/temp"

def executar_nbtscan(ip):
    output_file = f"{OUTPUT_DIR}/{ip}.nbtscan"
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{OUTPUT_DIR}:/data",
        "kali-recon",
        "bash", "-c", f"nbtscan -v {ip} > /data/{ip}.nbtscan"
    ]

    try:
        subprocess.run(cmd, check=True)
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erro ao executar nbtscan para {ip}: {e}")
        return None

def parsear_nbtscan(path):
    try:
        with open(path, "r") as f:
            conteudo = f.read()
    except FileNotFoundError:
        return None, None

    match = re.search(r"(\d+\.\d+\.\d+\.\d+)\s+([\w\-\.\$]*)?\s+([\w:\-]*)?", conteudo)
    if match:
        hostname = match.group(2) or None
        mac = match.group(3) or None
        return hostname, mac

    return None, None

def atualizar_opensearch(ip, hostname, mac):
    now = datetime.now(timezone.utc).isoformat()

    doc = {
        "script": {
            "source": """
                ctx._source.nbtscan_resultado.hostname = params.hostname;
                ctx._source.nbtscan_resultado.mac = params.mac;
                ctx._source.host_ja_scan = true;
                ctx._source.data_escaneamento = params.data;
            """,
            "lang": "painless",
            "params": {
                "hostname": hostname,
                "mac": mac,
                "data": now
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

    if response.status_code != 200:
        print(f"⚠️ Falha ao atualizar {ip}: {response.text}")
    else:
        print(f"✅ IP {ip} atualizado com hostname: {hostname}, MAC: {mac}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 executar_nbtscan_docker.py <IP>")
        sys.exit(1)

    if not PASSWORD:
        print("⚠️ Variável de ambiente OPENSEARCH_PASS não definida.")
        sys.exit(1)

    ip = sys.argv[1]

    print(f"🚀 Executando nbtscan via Docker para {ip}...")
    output_path = executar_nbtscan(ip)
    hostname, mac = parsear_nbtscan(output_path) if output_path else (None, None)
    atualizar_opensearch(ip, hostname, mac)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
