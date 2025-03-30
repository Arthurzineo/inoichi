import time
import os
import subprocess

# Tempo entre ciclos (em segundos)
INTERVALO_LOOP = 60

def main():
    while True:
        print("\n[🔁] Iniciando novo ciclo de verificação e scan...")

        print("[1] Executando verificação de online (verificar_online.py)...")
        subprocess.run(["python3", "4_verificar_online.py"])

        print("[2] Executando parallel do Nmap (5_parallel_executar_nmap_docker.py)...")
        subprocess.run(["python3", "5_parallel_executar_nmap_docker.py"])

        print("[3] Executando parallel do nbtscan (6_parallel_executar_nbtscan_docker.py)...")
        subprocess.run(["python3", "6_parallel_executar_nbtscan_docker.py"])

        print(f"[⏳] Aguardando {INTERVALO_LOOP} segundos para o próximo ciclo...\n")
        time.sleep(INTERVALO_LOOP)

if __name__ == "__main__":
    main()
