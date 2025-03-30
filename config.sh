#!/bin/bash

# ======================
# 🐧 Atualização do Sistema
# ======================
echo "[🆙] Atualizando sistema e pacotes..."
sudo apt update && sudo apt upgrade -y

# ======================
# 🐳 Instalação do Docker e Docker Compose
# ======================
echo "[📦] Instalando dependências do Docker..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

echo "[🔑] Adicionando chave GPG do Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "[📋] Adicionando repositório do Docker à lista de fontes..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "[🔄] Atualizando repositórios e instalando Docker..."
sudo apt update
sudo apt install -y docker-ce

echo "[🧩] Instalando Docker Compose v2.27.1..."
mkdir -p ~/.docker/cli-plugins/
curl -SL https://github.com/docker/compose/releases/download/v2.27.1/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose
chmod +x ~/.docker/cli-plugins/docker-compose

# ======================
# 🔐 Permissões: Dados e Certificados
# ======================
echo "[📂] Ajustando permissões da pasta opensearch-data..."
sudo chown -R 1000:1000 ./opensearch-data
sudo chmod -R 700 ./opensearch-data

echo "[🔒] 1. Aplicando permissão de leitura (r--) para todo o conteúdo de /inoichi..."
chmod -R a+r /inoichi

echo "[🔧] 2. Aplicando permissão total (rwx) para todo o conteúdo de /inoichi/scripts..."
chmod -R a+rwx /inoichi/scripts

echo "[🔐] 2.5 Dando permissão de execução para /inoichi/certs/certificados.sh..."
sudo chmod -R a+r certs
sudo chmod a+rx certs
chmod +x /inoichi/certs/certificados.sh

echo "[🚀] Executando o script de geração de certificados..."
/inoichi/certs/certificados.sh

echo "[🔧] Ajustando propriedades e permissões dos certificados..."
sudo chown -R 1000:1000 certs
sudo chmod -R u+r certs
sudo chmod u+rx certs

echo "[📜] 3. Garantindo permissão de leitura e acesso à pasta /inoichi/certs..."
chmod a+rx /inoichi/certs

echo "[📁] 4. Aplicando permissão de leitura (r--) para todo o conteúdo dentro de /inoichi/certs..."
chmod -R a+r /inoichi/certs

# ======================
# 🛠️ Build da Imagem Docker
# ======================
echo "[🔨] 5. Buildando imagem Docker personalizada com nome 'kali-recon' a partir de /inoichi/docker..."
docker build -t kali-recon /inoichi/docker

echo "[✅] Todas as permissões foram ajustadas e a imagem Docker 'kali-recon' foi criada com sucesso!"
