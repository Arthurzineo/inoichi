#!/bin/bash

apt install docker.io
apt install docker-compose

echo "[🔒] 1. Aplicando permissão de leitura (r--) para todo o conteúdo de /inoichi..."
chmod -R a+r /inoichi

echo "[🔧] 2. Aplicando permissão total (rwx) para todo o conteúdo de /inoichi/scripts..."
chmod -R a+rwx /inoichi/scripts

echo "[🔐] 2.5 Dando permissão de execução para /inoichi/certs/certificados.sh..."
chmod +x /inoichi/certs/certificados.sh

echo "[🚀] Executando o script de geração de certificados..."
/inoichi/certs/certificados.sh

echo "[📜] 3. Garantindo permissão de leitura e acesso à pasta /inoichi/certs..."
chmod a+rx /inoichi/certs

echo "[📁] 4. Aplicando permissão de leitura (r--) para todo o conteúdo dentro de /inoichi/certs..."
chmod -R a+r /inoichi/certs

echo "[🔨] 5. Buildando imagem Docker personalizada com nome 'kali-recon' a partir de /inoichi/docker..."
docker build -t kali-recon /inoichi/docker

echo "[✅] Todas as permissões foram ajustadas e a imagem Docker 'kali-recon' foi criada com sucesso!"
