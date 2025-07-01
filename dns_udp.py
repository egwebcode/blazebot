#!/data/data/com.termux/files/usr/bin/bash

clear
echo -e "\e[1;36m====== DNS UDP 53 - SCANNER LATÊNCIA ======\e[0m"
echo -e "Escolha o modo de entrada:"
echo -e "1) Inserir servidores DNS manualmente"
echo -e "2) Usar lista de IPs via arquivo .txt"

read -p $'\nDigite sua opção (1 ou 2): ' modo

dns_temp="dns_input_temp.txt"
> "$dns_temp"  # Limpa arquivo temporário

if [[ "$modo" == "1" ]]; then
    echo -e "\nDigite os IPs dos servidores DNS (um por vez)."
    echo "Digite 'fim' para encerrar a entrada."
    while true; do
        read -p "IP: " ip
        [[ "$ip" == "fim" ]] && break
        echo "$ip" >> "$dns_temp"
    done
elif [[ "$modo" == "2" ]]; then
    read -p $'\nDigite o nome do arquivo .txt com os IPs DNS: ' arquivo
    if [[ ! -f "$arquivo" ]]; then
        echo -e "\e[1;31mArquivo não encontrado!\e[0m"
        exit 1
    fi
    cp "$arquivo" "$dns_temp"
else
    echo -e "\e[1;31mOpção inválida!\e[0m"
    exit 1
fi

echo -e "\n\e[1;33mIniciando verificação...\e[0m"

output="resultados_dns_$(date +%H%M%S).txt"
> "$output"

testar_dns() {
    servidor=$1
    tempo_inicial=$(date +%s%3N)

    echo "" | timeout 1s nc -w1 -u "$servidor" 53 &>/dev/null
    status=$?

    tempo_final=$(date +%s%3N)
    tempo_total=$((tempo_final - tempo_inicial))

    if [[ $status -eq 0 ]]; then
        echo -e "✅ $servidor - ${tempo_total}ms"
        echo "$tempo_total $servidor" >> "$output"
    else
        echo -e "❌ $servidor - sem resposta"
    fi
}

total=$(wc -l < "$dns_temp")
contador=1

while IFS= read -r ip; do
    ip=$(echo "$ip" | tr -d '\r')
    if [[ -n "$ip" ]]; then
        echo -e "\n\e[1;36m[$contador/$total] Testando $ip...\e[0m"
        testar_dns "$ip"
        contador=$((contador+1))
    fi
done < "$dns_temp"

echo -e "\n\e[1;32mServidores com resposta (ordenados por latência):\e[0m"
sort -n "$output" | awk '{print "✅ " $2 " - " $1 "ms"}' | tee ordenados_$output

echo -e "\n\e[1;34mResultado salvo em: ordenados_$output\e[0m"
