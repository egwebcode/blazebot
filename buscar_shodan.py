import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import socket
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

init(autoreset=True)
verbose = "-v" in sys.argv

print(Fore.CYAN + Style.BRIGHT + "\n=== EGWEBCODE BUSCAR SHODAN FREE - SCAN TURBINADO ===\n")
print(Fore.CYAN + "Pressione ENTER uma vez para encerrar...\n")

portas = [80, 8080, 8888, 443, 8443]
palavras_login = ["login", "admin", "senha", "password", "sign in", "access", "panel"]
lock = threading.Lock()
resultados = []
executando = True

def gerar_ips():
    for i in range(1, 4294967295):
        yield socket.inet_ntoa(i.to_bytes(4, 'big'))

session = requests.Session()

def escanear(ip_porta):
    if not executando:
        return
    ip, porta = ip_porta
    protocolos = ["https"] if porta in [443, 8443] else ["http", "https"]
    for protocolo in protocolos:
        url = f"{protocolo}://{ip}:{porta}"

        if verbose:
            with lock:
                print(Fore.WHITE + f"Buscando {url}...")

        try:
            resposta = session.get(url, timeout=3, verify=False)
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

def escutar_enter():
    global executando
    try:
        input()
        executando = False
    except:
        pass

def iniciar_scanner():
    with ThreadPoolExecutor(max_workers=200) as executor:
        ip_gen = gerar_ips()
        while executando:
            ip = next(ip_gen)
            for porta in portas:
                executor.submit(escanear, (ip, porta))

if __name__ == "__main__":
    try:
        threading.Thread(target=iniciar_scanner, daemon=True).start()
        escutar_enter()
        print(Fore.YELLOW + "\nSalvando resultados em resultados.txt...")
        with open("resultados.txt", "w") as f:
            for linha in resultados:
                f.write(linha + "\n")
        print(Fore.GREEN + Style.BRIGHT + "\n✅ Scanner finalizado com sucesso!")
    except KeyboardInterrupt:
        print(Fore.RED + "\nInterrompido manualmente.")
