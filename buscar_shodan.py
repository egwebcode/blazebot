import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import threading
import socket
import time
import sys

init(autoreset=True)

verbose = "-v" in sys.argv

print(Fore.CYAN + Style.BRIGHT + "\n=== EGWEBCODE BUSCAR SHODAN FREE - PAINEL AO VIVO ===\n")
print(Fore.CYAN + "Pressione ENTER uma vez para encerrar...\n")

portas = [80, 8080, 8888, 443, 8443]
palavras_login = ["login", "admin", "senha", "password", "sign in", "access", "panel"]
lock = threading.Lock()
resultados = []
executando = True

def gerar_ips():
    for i in range(1, 4294967295):
        ip = socket.inet_ntoa(i.to_bytes(4, 'big'))
        yield ip

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
                print(Fore.GREEN + f"[200 OK] {url}")
                print(Fore.YELLOW + f"Status: {status}")
                print(Fore.MAGENTA + f"Título: {titulo}")
                print(Fore.BLUE + f"Servidor: {servidor}")
                if achou_login:
                    print(Fore.RED + "[ALERTA] Página de login detectada!")
                print(Fore.CYAN + "------------------------------")

                resultados.append(f"{url} - {status} - {titulo} - {servidor}")

        except requests.exceptions.RequestException:
            if verbose:
                with lock:
                    print(Fore.RED + f"[ERRO] {url} não respondeu.")
                    print(Fore.CYAN + "------------------------------")

def escutar_enter_uma_vez():
    global executando
    try:
        input()
        executando = False
    except:
        pass

def iniciar_scanner():
    ip_gen = gerar_ips()
    while executando:
        ip = next(ip_gen)
        for porta in portas:
            t = threading.Thread(target=escanear, args=(ip, porta))
            t.daemon = True
            t.start()
            time.sleep(0.01)

if __name__ == "__main__":
    try:
        scanner_thread = threading.Thread(target=iniciar_scanner)
        scanner_thread.start()

        escutar_enter_uma_vez()

        print(Fore.YELLOW + "\nSalvando resultados em resultados.txt...")
        with open("resultados.txt", "w") as f:
            for linha in resultados:
                f.write(linha + "\n")

        print(Fore.GREEN + Style.BRIGHT + "\n✅ Scanner finalizado com sucesso!")

    except KeyboardInterrupt:
        print(Fore.RED + "\nInterrompido manualmente.")
