#!/data/data/com.termux/files/usr/bin/bash

# Troque pela sua chave da API do Shodan
API_KEY="SUA_API_KEY_AQUI"

read -p "🔍 Digite sua consulta (ex: webcam 7): " QUERY

# Formata a query
ENCODED_QUERY=$(echo "$QUERY" | sed 's/ /%20/g')

echo "⏳ Buscando dados no Shodan..."

curl -s "https://api.shodan.io/shodan/host/search?key=$API_KEY&query=$ENCODED_QUERY" | jq -c '.matches[]' | while read -r host; do
  ip=$(echo "$host" | jq -r '.ip_str')
  port=$(echo "$host" | jq -r '.port')
  org=$(echo "$host" | jq -r '.org // "N/A"')
  country=$(echo "$host" | jq -r '.location.country_name // "N/A"')
  city=$(echo "$host" | jq -r '.location.city // "N/A"')
  hostnames=$(echo "$host" | jq -r '.hostnames | join(", ") // "N/A"')

  echo "🌐 IP: $ip"
  echo "📍 Localização: $city, $country"
  echo "🏢 Organização: $org"
  echo "🔌 Porta: $port"
  echo "🔗 Hostnames: $hostnames"
  echo "---------------------------"
done
