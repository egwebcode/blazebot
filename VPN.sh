#!/data/data/com.termux/files/usr/bin/bash

# Color & style
blue='\033[1;34m'
green='\033[1;32m'
red='\033[1;31m'
yellow='\033[1;33m'
reset='\033[0m'

BANNER() {
clear
echo -e "${blue}"
echo "╔═══════════════════════════════════════════╗"
echo "║         EG WEBCODE VPN CUSTOM             ║"
echo "╠═══════════════════════════════════════════╣"
echo "║  Redirecionamento via DNSTT ou STUNNEL    ║"
echo "║  Totalmente customizável e expansível     ║"
echo "╚═══════════════════════════════════════════╝"
echo -e "${reset}"
}

# Instalar dependências se necessário
INSTALL_DEPENDENCIES() {
    echo -e "${yellow}[+] Instalando dependências...${reset}"
    pkg update -y
    pkg install -y curl wget proot stunnel dnsutils unzip
    [ ! -f ./dnstt-client ] && {
        echo -e "${yellow}[+] Baixando dnstt-client...${reset}"
        curl -L -o dnstt.zip https://github.com/yrutschle/dnstt/releases/latest/download/dnstt-client-linux.zip
        unzip dnstt.zip
        chmod +x dnstt-client
    }
}

# DNSTT CLIENT
START_DNSTT() {
    BANNER
    echo -e "${green}[DNSTT]${reset} Informe os dados:"
    read -p "🔹 Host DNS (ex: dns.egcode.com): " DNS
    read -p "🔹 Porta do servidor (ex: 53): " PORT
    read -p "🔹 IP real do servidor (ex: 123.123.123.123): " IP
    read -p "🔹 Caminho para chave pública .pub: " PUBKEY

    echo -e "\n${yellow}[+] Iniciando conexão via dnstt-client...${reset}\n"
    ./dnstt-client -d tun0 --dns "$DNS" "$IP:$PORT" "$PUBKEY" &
    sleep 2
    echo -e "${green}[✔] DNSTT rodando em tun0${reset}"
    read -p "Pressione Enter para voltar ao menu..."
}

# STUNNEL
START_STUNNEL() {
    BANNER
    echo -e "${green}[STUNNEL]${reset} Informe os dados:"
    read -p "🔹 Host SNI (ex: m.youtube.com): " SNI
    read -p "🔹 IP do servidor TLS (ex: 123.123.123.123): " IP
    read -p "🔹 Porta TLS (ex: 443): " PORT
    read -p "🔹 Porta local (ex: 8080): " LOCAL

    mkdir -p ~/stunnel
    cat > ~/stunnel/stunnel.conf <<EOF
client = yes
[sni]
accept = 127.0.0.1:$LOCAL
connect = $IP:$PORT
sni = $SNI
EOF

    stunnel ~/stunnel/stunnel.conf &
    sleep 2
    echo -e "${green}[✔] STUNNEL escutando em 127.0.0.1:$LOCAL${reset}"
    read -p "Pressione Enter para voltar ao menu..."
}

# Mata os processos
STOP_ALL() {
    pkill stunnel
    pkill dnstt-client
    echo -e "${red}[✘] Conexões encerradas.${reset}"
    sleep 1
}

# MENU PRINCIPAL
while true; do
    BANNER
    echo -e "${green}Escolha uma opção:${reset}"
    echo -e "${blue}[1]${reset} Iniciar conexão DNSTT"
    echo -e "${blue}[2]${reset} Iniciar conexão STUNNEL (SNI)"
    echo -e "${blue}[3]${reset} Parar todas conexões"
    echo -e "${blue}[4]${reset} Instalar dependências"
    echo -e "${blue}[0]${reset} Sair"
    echo -ne "\n${yellow}EG> ${reset}"
    read opt

    case "$opt" in
        1) START_DNSTT ;;
        2) START_STUNNEL ;;
        3) STOP_ALL ;;
        4) INSTALL_DEPENDENCIES ;;
        0) STOP_ALL; echo -e "${blue}Saindo...${reset}"; exit ;;
        *) echo -e "${red}Opção inválida${reset}"; sleep 1 ;;
    esac
done
