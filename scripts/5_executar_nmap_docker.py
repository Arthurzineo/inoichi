import subprocess
import os
import sys
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from requests.auth import HTTPBasicAuth

OPENSEARCH_URL = "https://localhost:9200"
INDEX_NAME = "reconhecimento_hosts"
USERNAME = "admin"
PASSWORD = os.environ.get("OPENSEARCH_PASS")
OUTPUT_DIR = "/inoichi/temp"
DOCKER_IMAGE = "kali-recon"

def executar_nmap_docker(ip):
    output_file = f"{OUTPUT_DIR}/{ip}.xml"

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{OUTPUT_DIR}:/data",
        DOCKER_IMAGE,
        "bash", "-c", f"nmap -O -oX /data/{ip}.xml {ip}"
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Erro ao executar o Nmap para {ip}: {e}")
        return None

    return output_file

def parsear_os_do_nmap_xml(path):
    try:
        tree = ET.parse(path)
        root = tree.getroot()
    except Exception as e:
        print(f"⚠️ Erro ao parsear o XML: {e}")
        return "Desconhecido", []

    os_details = "Desconhecido"
    cpe_list = []

    for host in root.findall("host"):
        os_elem = host.find("os")
        if os_elem is not None:
            osmatch = os_elem.find("osmatch")
            if osmatch is not None:
                os_details = osmatch.attrib.get("name", "Desconhecido")

                # Extrai CPEs dos osclass
                for osclass in osmatch.findall("osclass"):
                    for cpe in osclass.findall("cpe"):
                        if cpe.text and cpe.text not in cpe_list:
                            cpe_list.append(cpe.text)

                # CPEs diretamente no osmatch
                for cpe in osmatch.findall("cpe"):
                    if cpe.text and cpe.text not in cpe_list:
                        cpe_list.append(cpe.text)
                break  # Pega apenas o primeiro match

    return os_details, cpe_list

def atualizar_opensearch(ip, sistema_os, cpes):
    now = datetime.now(timezone.utc).isoformat()

    doc = {
        "script": {
            "source": """
                ctx._source.nmap_resultado.os = params.os;
                ctx._source.nmap_resultado.cpe = params.cpe;
                ctx._source.data_escaneamento = params.data;
            """,
            "lang": "painless",
            "params": {
                "os": sistema_os,
                "cpe": cpes,
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

    if response.status_code not in (200, 201):
        print(f"⚠️ Erro ao atualizar IP {ip}: {response.text}")
    else:
        print(f"✅ IP {ip} atualizado com OS: {sistema_os}")

def main():
    if len(sys.argv) != 2:
        print("Uso: python3 executar_nmap_docker.py <IP>")
        sys.exit(1)

    if not PASSWORD:
        print("⚠️  Variável de ambiente OPENSEARCH_PASS não definida.")
        sys.exit(1)

    ip = sys.argv[1]
    print(f"🚀 Executando Nmap via Docker com saída XML para {ip}...")

    output_path = executar_nmap_docker(ip)

    if output_path:
        sistema_os, cpes = parsear_os_do_nmap_xml(output_path)
        atualizar_opensearch(ip, sistema_os, cpes)

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings()
    main()
