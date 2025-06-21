import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import threading
import socket
import time
import sys
import select

# Inicializa o terminal colorido
init(autoreset=True)

# Verifica se o modo verbose foi ativado com -v
verbose = "-v" in sys.argv

print(Fore.CYAN + Style.BRIGHT + "\n=== EGWEBCODE BUSCAR SHODAN FREE - ULTIMATE VERSION ===\n")

# Configurações
portas = [80, 8080, 8888, 443, 8443]
palavras_login = ["login", "admin", "senha", "password", "sign in", "access", "panel"]
lock = threading.Lock()
resultados = []

# Gera IPs sequenciais válidos
def gerar_ips():
    for i in range(1, 4294967295):
        ip = socket.inet_ntoa(i.to_bytes(4, 'big'))
        yield ip

# Função para escanear
def escanear(ip, porta):
    protocolos = ["https"] if porta in [443, 8443] else ["http", "https"]
    for protocolo in protocolos:
        url = f"{protocolo}://{ip}:{porta}"

        if verbose:
            with lock:
                print(Fore.WHITE + f"Buscando {url}...")

        try:
            resposta = requests.get(url, timeout=3, verify=False)
            status = resposta.status_code
            headers = resposta.headers
            soup = BeautifulSoup(resposta.text, "html.parser")
            titulo = soup.title.string.strip() if soup.title else "Sem título"
            conteudo = resposta.text.lower()
            achou_login = any(p in conteudo for p in palavras_login)
            servidor = headers.get("Server", "Desconhecido")

            with lock:
                print(Fore.GREEN + f"[ONLINE] {url}")
                print(Fore.YELLOW + f"Status: {status}")
                print(Fore.MAGENTA + f"Título: {titulo}")
                print(Fore.BLUE + f"Servidor: {servidor}")
                if achou_login:
                    print(Fore.RED + "[ALERTA] Página de login detectada!")
                print(Fore.CYAN + "------------------------------")

                resultado = f"{url} - {status} - {titulo} - {servidor}"
                resultados.append(resultado)

        except requests.exceptions.RequestException:
            pass

# Listener para detectar ENTER + ENTER
def esperar_dois_enters():
    enter_count = 0
    print(Fore.CYAN + "Pressione ENTER duas vezes para encerrar...")
    while True:
        if select.select([sys.stdin], [], [], 0.1)[0]:
            input()
            enter_count += 1
            if enter_count >= 2:
                break
        else:
            enter_count = 0

# Início do scanner
def iniciar_scanner():
    ip_generator = gerar_ips()
    while True:
        ip = next(ip_generator)
        for porta in portas:
            t = threading.Thread(target=escanear, args=(ip, porta))
            t.daemon = True
            t.start()
            time.sleep(0.01)

# Execução principal
if __name__ == "__main__":
    try:
        # Roda o scanner em thread
        thread_scanner = threading.Thread(target=iniciar_scanner)
        thread_scanner.daemon = True
        thread_scanner.start()

        # Espera ENTER + ENTER
        esperar_dois_enters()

        # Salva os resultados encontrados
        print(Fore.YELLOW + "\nSalvando resultados em 'resultados.txt'...\n")
        with open("resultados.txt", "w") as f:
            for linha in resultados:
                f.write(linha + "\n")

        print(Fore.GREEN + Style.BRIGHT + "\n✅ Scanner finalizado com sucesso!\n")

    except KeyboardInterrupt:
        print(Fore.RED + "\nInterrompido manualmente.")
