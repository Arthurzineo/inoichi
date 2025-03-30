#!/bin/bash

if [ -z "$OPENSEARCH_PASS" ]; then
  echo "[❌] A variável de ambiente OPENSEARCH_PASS não está definida."
  echo "Por favor, defina-a com: export OPENSEARCH_PASS='sua_senha'"
  exit 1
fi

rm -rf /inoichi/temp/*

echo "[*] Subindo containers com Docker Compose..."
docker compose -f /inoichi/docker-compose.yml up -d

echo "[*] Aguardando 60 segundos para os serviços iniciarem..."
sleep 60

/inoichi/scripts/cria_index_reconhecimento.sh

python3 printlogo.py
python3 executa_tudo.py
python3 loop_verifica_online_e_executa_scans.py
