def carregar_ips(caminho_arquivo):
    with open(caminho_arquivo, "r") as f:
        return set(linha.strip() for linha in f if linha.strip())

def salvar_resultado(ips, caminho_saida):
    with open(caminho_saida, "w") as f:
        for ip in sorted(ips):
            f.write(ip + "\n")

def main():
    path_endpoint = "/inoichi/entrada/ips_endpoint.txt"
    path_firewall = "/inoichi/entrada/ips_firewall.txt"
    path_saida = "/inoichi/temp/resultado.txt"

    ips_endpoint = carregar_ips(path_endpoint)
    ips_firewall = carregar_ips(path_firewall)

    ips_sem_endpoint = ips_firewall - ips_endpoint
    salvar_resultado(ips_sem_endpoint, path_saida)

    print(f"✅ {len(ips_sem_endpoint)} IPs salvos em {path_saida}")

if __name__ == "__main__":
    main()
