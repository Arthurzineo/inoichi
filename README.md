# 🐉 INOICHI - Reconhecimento de Hosts com OpenSearch

Projeto de automação para reconhecimento de ativos em rede, com coleta, visualização e gestão centralizada de resultados usando o OpenSearch + OpenSearch Dashboards. Ideal para profissionais de cibersegurança e sysadmins que desejam automatizar seus processos de footprinting e discovery.

---
Claro! Aqui está um exemplo de tópico que pode ir no seu `README.md` ou apresentação do projeto:

---

## 🎯 Propósito / O que esperamos resolver

Em médias e grandes empresas, o controle e a visibilidade sobre os ativos de TI — especialmente estações de trabalho e servidores — é um grande desafio. Um dos principais problemas enfrentados pelas equipes de segurança é identificar, de forma precisa e constante, quais computadores estão **sem um endpoint de proteção ativo** (como antivírus ou EDR).  

Essas falhas podem acontecer por diversos motivos, como:

- **Erro na instalação do endpoint**  
- **Máquinas recém-formatadas ou adicionadas ao ambiente**  
- **Desinstalação não autorizada ou acidental**  
- **Exceções que não foram devidamente catalogadas ou documentadas**

Em ambientes com **milhares de computadores**, essa verificação se torna praticamente impossível de ser feita manualmente todos os dias. Isso abre brechas sérias de segurança, podendo permitir que uma máquina comprometida passe despercebida por tempo suficiente para causar vazamentos ou movimentações laterais em redes corporativas.

Este projeto tem como propósito **automatizar o reconhecimento, análise e rastreamento desses hosts**, permitindo que a equipe de segurança:

- Detecte rapidamente computadores possivelmente desprotegidos  
- Classifique exceções de forma controlada e documentada  
- Mantenha um painel de visibilidade atualizado e histórico de alterações  
- Ganhe tempo e confiabilidade no processo de verificação diária de cobertura de endpoints

Nosso objetivo é **reduzir o tempo entre o surgimento de uma falha e sua detecção**, melhorando o tempo de resposta e fortalecendo a postura de segurança da organização.

---

Quer que eu formate isso num `.txt` também junto com os outros arquivos?

## 🚀 Funcionalidades

- ⚙️ Execução automatizada de scanners (nmap, nbtscan)
- 📦 Deploy com Docker Compose
- 🔐 Segurança com HTTPS (certificados TLS próprios)
- 🛡️ OpenSearch com autenticação e painel de visualização
- 🧠 Detecção e marcação de exceções via CSV
- 📊 Dashboard customizado no OpenSearch Dashboards
- 🐚 Scripts em Python e Shell para automação completa
---


## 🔧 Requisitos

Ubuntu Server com python instalado, e git.

---

## ⚡ Como usar

1. **Clone o repositório:**

Clone usando o usuario ROOT estando no /
(Atualmente o projeto usa algumas coisas com caminho absoluto.)

```bash
cd /
```

```bash
git clone https://github.com/seuusuario/inoichi.git
cd inoichi
```

2. **Defina a variável de ambiente com a senha do OpenSearch:**

```bash
export OPENSEARCH_PASS="sua_senha_forte"
```

3. **Execute o script de Configuração:**

```bash
chmod +x config.sh
./config.sh
```

> Este script:
> - Da update no sistema
> - Instala o parallel
> - instala docker + docker compose e todas as dependencias
> - Cria os certificados para o TLS do https auto assinado do banco (prencher com os dados solicitados)
> - Libera as permições de leituras e escrita nos arquivos
> - Cria a imagem kali-recon para ser usada nos containers no programa

---

4. **Prencha as listas de IPS:**
   Coloque os IPS nessa lista no formato 1 ip por linha.
```bash
/inoichi/entrada/ips_firewall.txt
/inoichi/entrada/ips_endpoint.txt
```

5. **Execute o script de inicialização:**

```bash
cd /inoichi/scripts/
./start.sh
```

> Este script:
> - Limpa arquivos temporários
> - Sobe os containers do docker compose
> - Aguarda a inicialização
> - Cria o índice `reconhecimento_hosts`
> - Exibe o logo
> - Inicia os scripts principais ( inicial + looping )

---



## 📥 Adicionar IPs como exceção

Você pode usar um CSV com IP e comentário para marcar exceções diretamente no índice:

```csv
192.168.1.1,IP do roteador principal
```

Execute:

```bash
python3 /inoichi/scripts/excecoes_csv.py caminho/para/excecoes.csv
```
Você pode usar um IP unico e comentário para marcar exceções diretamente no índice:
Execute:

```bash
python3 /inoichi/scripts/adicionar_excecao.py ip "comentario entre aspas"
```
Você pode deletar ip (isso remove a exceção):
```bash
python3 /inoichi/scripts/remover_ip.py ip 
```

Você pode deletar deletar o index todo para zerar o banco:
```bash
./deleta_index.sh  
```
para criar o index do zero é só executar novamente o start.sh ou se preferir criar ele antes é apenas executar o:
```bash
./cria_index_reconhecimento.sh  
```

---

## 📡 Visualização

Acesse o painel em:  
🔗 `https://localhost:5601`

Login padrão:
- Usuário: `admin`
- Senha: definida pela variável de ambiente `OPENSEARCH_PASS`

---

## 📞 Como habilitar o telegram?
para habiltiar o telegram é necessario modificar 2 arquivos
```bash
/inoichi/scripts/3_registrar_no_opensearch.py 
/inoichi/scripts/4_verificar_online.py 
```
e alterar:
- TOKEN = "0"  # coloque seu token aqui
- CHAT_ID = "0"  # coloque seu chat_id aqui
Porem antes tem que ser criado o bot no telegram recomento Botfather o token vai ser o tokengerado pelo BOT e o CHAT_ID o ID do seu CHAT
---

> 💡 **Curiosidade**: O nome **Inoichi** é inspirado no personagem do universo Naruto, conhecido por suas habilidades de coleta e transmissão de informações — algo que reflete bem a proposta do projeto!
