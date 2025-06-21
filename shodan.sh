#!/data/data/com.termux/files/usr/bin/bash

# Definir cores para o painel colorido
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
WHITE='\033[0;97m'
RESET='\033[0m'

# Função para exibir o título inicial
function show_banner() {
    clear
    echo -e "${CYAN}========================================================="
    echo -e "${WHITE}          Shodan.io Professional Search Tool           "
    echo -e "${WHITE}                 By EGWEBCODE - SHODAN.IO               "
    echo -e "${CYAN}========================================================="
    echo -e "${YELLOW}Bem-vindo ao painel profissional de pesquisa Shodan!"
    echo -e "${CYAN}========================================================="
}

# Função para pedir e validar a chave da API
function get_api_key() {
    while true; do
        echo -e "${CYAN}🔑 Por favor, insira sua chave da API do Shodan:"
        read -s API_KEY
        if [[ -z "$API_KEY" ]]; then
            echo -e "${RED}A chave da API não pode estar vazia. Tente novamente.${RESET}"
        else
            echo -e "${GREEN}Chave da API recebida com sucesso!${RESET}"
            break
        fi
    done
}

# Função para buscar resultados com a API do Shodan
function fetch_results() {
    URL="https://api.shodan.io/shodan/host/search?key=$API_KEY&query=$1&page=$2"
    echo -e "${CYAN}⏳ Buscando resultados na página $2..."
    
    curl -s "$URL" | jq -r '.matches[] | "
