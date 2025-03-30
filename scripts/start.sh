#!/bin/bash

echo "[*] Limpando arquivos temporários da pasta /inoichi/temp..."
rm -rf /inoichi/temp/*

echo "[*] Subindo containers com Docker Compose..."
docker compose -f /inoichi/docker-compose.yml up -d

echo "[*] Aguardando 60 segundos para os serviços iniciarem..."
sleep 60

echo "[*] Criando índice reconhecimento_hosts no OpenSearch..."
/inoichi/scripts/cria_index_reconhecimento.sh

python3 printlogo.py
python3 executa_tudo.py
python3 loop_verifica_online_e_executa_scans.py
