import subprocess
import os
import sys
import time


def executar_script():
    print(f"\n[●] Executando: ")
    try:
        subprocess.run(["python3", "1_filtra_ips_sem_endpoint.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao executar : {e}")
        sys.exit(1)
    try:
        subprocess.run(["python3", "2_filtrar_exececoes_opensearch.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao executar : {e}")
        sys.exit(1)
    try:
        subprocess.run(["python3", "3_registrar_no_opensearch.py"], check=True)
        time.sleep(10)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao executar : {e}")
        sys.exit(1)
    try:
        subprocess.run(["python3", "4_verificar_online.py"], check=True)
        time.sleep(15)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao executar : {e}")
        sys.exit(1)
    try:
        subprocess.run(["python3", "5_parallel_executar_nmap_docker.py"], check=True)
        time.sleep(30)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao executar  {e}")
        sys.exit(1)
    try:
        subprocess.run(["python3", "6_parallel_executar_nbtscan_docker.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Erro ao executar : {e}")
        sys.exit(1)
    
def main():
    if "OPENSEARCH_PASS" not in os.environ:
        print("[!] Variável de ambiente OPENSEARCH_PASS não definida.")
        print("    Exporte com: export OPENSEARCH_PASS='sua_senha'")
        sys.exit(1)

    executar_script()

    print("\n[✓] Todos os scripts foram executados com sucesso!")

if __name__ == "__main__":
    main()
