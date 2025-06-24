#!/data/data/com.termux/files/usr/bin/bash

# Cores
green='\033[1;32m'
red='\033[1;31m'
blue='\033[1;34m'
yellow='\033[1;33m'
reset='\033[0m'

# Banner
BANNER() {
    clear
    echo -e "${blue}"
    echo "╔═════════════════════════════════════════════╗"
    echo "║        EG WEBCODE VPN REAL FUNCTIONAL       ║"
    echo "╠═════════════════════════════════════════════╣"
    echo "║   DNS, STUNNEL, TLS VPN com Verificação     ║"
    echo "╚═════════════════════════════════════════════╝"
    echo -e "${reset}"
}

# Verifica se o túnel está realmente ativo
CHECK_TUNNEL() {
    echo -e "${yellow}[+] Verificando túnel (tun0)...${reset}"
    if ip a | grep -q tun0; then
        echo -e "${green}[✔] Interface tun0 encontrada${reset}"
        echo -e "${yellow}[+] Testando ping via túnel...${reset}"
        if ping -I tun0 -c 2 1.1.1.1 >/dev/null 2>&1; then
            echo -e "${green}[✔] Túnel FUNCIONANDO com internet!${reset}"
        else
            echo -e "${red}[✘] tun0 sem internet. O túnel foi criado, mas não está roteando.${reset}"
        fi
    else
        echo -e "${red}[✘] Nenhum túnel ativo encontrado (tun0 ausente).${reset}"
    fi
    read -p "Pressione Enter para voltar ao menu..."
}

# Iniciar DNSTT
START_DNSTT() {
    BANNER
    echo -e "${green}[DNSTT CLIENT MODE]${reset}"
    read -p "🔹 Domínio DNS (ex: dns.exemplo.com): " DNS
    read -p "🔹 IP do servidor (ex: 123.123.123.123): " IP
    read -p "🔹 Porta do servidor DNS (padrão: 53): " PORT
    read -p "🔹 Caminho para chave pública (.pub): " PUB

    echo -e "\n${yellow}[+] Iniciando DNSTT com tunelamento via tun0...${reset}\n"
    ./dnstt-client -d tun0 --dns "$DNS" "$IP:$PORT" "$PUB" &
    sleep 2
    CHECK_TUNNEL
}

# Iniciar STUNNEL
START_STUNNEL() {
    BANNER
    echo -e "${green}[STUNNEL CUSTOM]${reset}"
    read -p "🔹 SNI (ex: m.youtube.com): " SNI
    read -p "🔹 IP do servidor (ex: 123.123.123.123): " IP
    read -p "🔹 Porta do servidor TLS (ex: 443): " PORT
    read -p "🔹 Porta local (ex: 8080): " LOCAL

    mkdir -p ~/stunnel
    cat > ~/stunnel/stunnel.conf <<EOF
client = yes
[sni]
accept = 127.0.0.1:$LOCAL
connect = $IP:$PORT
sni = $SNI
EOF

    echo -e "${yellow}[+] Iniciando Stunnel...${reset}"
    stunnel ~/stunnel/stunnel.conf &
    sleep 1
    echo -e "${green}[✔] STUNNEL ativo em 127.0.0.1:$LOCAL → $SNI:$PORT${reset}"
    read -p "Pressione Enter para voltar ao menu..."
}

# Encerrar conexões
STOP_ALL() {
    pkill dnstt-client
    pkill stunnel
    echo -e "${red}[✘] Todos os processos finalizados.${reset}"
    sleep 1
}

# Menu principal
while true; do
    BANNER
    echo -e "${green}Escolha uma opção:${reset}"
    echo -e "${blue}[1]${reset} Iniciar DNSTT (porta 53 UDP)"
    echo -e "${blue}[2]${reset} Iniciar STUNNEL (TLS/SNI)"
    echo -e "${blue}[3]${reset} Verificar se túnel está funcionando"
    echo -e "${blue}[4]${reset} Encerrar conexões"
    echo -e "${blue}[0]${reset} Sair"
    echo -ne "\n${yellow}EG> ${reset}"
    read opt

    case "$opt" in
        1) START_DNSTT ;;
        2) START_STUNNEL ;;
        3) CHECK_TUNNEL ;;
        4) STOP_ALL ;;
        0) STOP_ALL; echo -e "${blue}Saindo...${reset}"; exit ;;
        *) echo -e "${red}Opção inválida${reset}"; sleep 1 ;;
    esac
done
