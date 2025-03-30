#!/bin/bash

# Verifica se a variável de ambiente está definida
if [ -z "$OPENSEARCH_PASS" ]; then
  echo "[!] Erro: variável de ambiente OPENSEARCH_PASS não definida."
  echo "    Use: export OPENSEARCH_PASS='sua_senha_aqui'"
  exit 1
fi

echo "[+] Criando índice RECONHECIMENTO_HOSTS"
echo

curl -XPUT --insecure --user admin:$OPENSEARCH_PASS https://localhost:9200/reconhecimento_hosts \
  -H "Content-Type: application/json" -d @- <<EOF
{
  "mappings": {
    "properties": {
      "@timestamp":         { "type": "date" },
      "ip":                 { "type": "ip" },
      "data_escaneamento":  { "type": "date" },
      "status_online":      { "type": "boolean" },
      "excecao":            { "type": "boolean" },
      "comentario":         { "type": "text" },
      "host_ja_scan":       { "type": "boolean" },
      "erro":               { "type": "text" },

      "nmap_resultado": {
        "properties": {
          "os": { "type": "text" },
          "cpe": { "type": "keyword" }
        }
      },

      "nbtscan_resultado": {
        "properties": {
          "hostname": { "type": "keyword" },
          "mac":      { "type": "keyword" }
        }
      }
    }
  }
}
EOF
