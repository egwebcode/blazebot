#!/data/data/com.termux/files/usr/bin/bash

# Consulta inicial
read -p "🔍 Digite sua consulta (ex: webcam 7): " QUERY
PAGE=1

# Função para buscar os IPs
fetch_results() {
    URL="https://www.shodan.io/search?query=$1&page=$2"
    echo "⏳ Buscando resultados na página $2..."

    # Busca via curl e extrai IPs usando grep e sed
    curl -s "$URL" | grep -oP 'IP: \K[\d\.]+' | while read -r ip; do
        echo "🌐 IP encontrado: $ip"
    done
}

# Iniciar a busca
while true; do
    fetch_results "$QUERY" "$PAGE"
    
    # Pergunta se o usuário quer ir para a próxima página
    read -p "🔄 Deseja ir para a próxima página? (s/n): " choice
    if [[ "$choice" == "s" ]]; then
        PAGE=$((PAGE + 1))
    else
        echo "Pesquisa concluída."
        break
    fi
done
