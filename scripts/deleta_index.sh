#!/bin/bash

if [ -z "$OPENSEARCH_PASS" ]; then
  echo "[!] Erro: variável de ambiente OPENSEARCH_PASS não definida."
  echo "    Use: export OPENSEARCH_PASS='sua_senha_aqui'"
  exit 1
fi

echo "[!] ATENÇÃO: Isso irá DELETAR o índice 'reconhecimento_hosts'"
read -p "Tem certeza? (s/N): " CONFIRMA

if [[ "$CONFIRMA" != "s" && "$CONFIRMA" != "S" ]]; then
  echo "[-] Cancelado."
  exit 0
fi

curl -XDELETE --insecure -u admin:$OPENSEARCH_PASS https://localhost:9200/reconhecimento_hosts
