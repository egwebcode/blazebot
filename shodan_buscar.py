import shodan
import sys

def buscar_shodan(api_key, query):
    try:
        # Conecta à API do Shodan com a chave fornecida
        api = shodan.Shodan(api_key)
        print(f"Buscando por: {query}")
        
        # Realiza a pesquisa no Shodan
        results = api.search(query)
        
        print(f"\nResultados encontrados: {results['total']}")
        print("------------------------------")

        # Itera sobre os resultados e imprime as informações relevantes
        for result in results['matches']:
            ip = result['ip_str']
            porta = result['port']
            url = f"https://{ip}:{porta}"
            info = f"IP: {ip} | Porta: {porta} | URL: {url}"

            # Adiciona mais informações sobre o dispositivo
            if 'hostnames' in result:
                info += f" | Hostnames: {', '.join(result['hostnames'])}"
            if 'location' in result:
                location = result['location']
                info += f" | Localização: {location.get('city', 'Desconhecido')}, {location.get('country_name', 'Desconhecido')}"
            
            print(info)
            print("------------------------------")
    except shodan.APIError as e:
        print(f"Erro ao acessar a API do Shodan: {e}")

def main():
    print("Bem-vindo ao script de busca no Shodan!")
    
    # Solicita a chave da API manualmente
    api_key = input("Digite sua chave da API do Shodan: ").strip()
    if not api_key:
        print("Chave de API inválida.")
        sys.exit(1)

    # Solicita o termo de pesquisa manualmente
    query = input("Digite o que deseja buscar no Shodan (exemplo: webcam 7): ").strip()
    if not query:
        print("Pesquisa inválida.")
        sys.exit(1)

    buscar_shodan(api_key, query)

if __name__ == "__main__":
    main()
