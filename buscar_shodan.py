import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style, init
import threading
import socket
import time

init(autoreset=True)

print(Fore.CYAN + Style.BRIGHT + "\n=== EGWEBCODE BUSCAR SHODAN FREE - TURBO SCAN ===\n")

portas = [80, 8080, 8888, 443, 8443]
palavras_login = ["login", "admin", "senha", "password", "sign in", "access", "panel"]

lock = threading.Lock()  # Para evitar sobreposição de prints e escrita

def gerar_ips():
    for i in range(1, 4294967295):  # IPv4 completo
        ip = socket.inet_ntoa(i.to_bytes(4, 'big'))
        yield ip

def escanear(ip, porta):
    protocolos = ["http", "https"] if porta in [443, 8443] else ["http"]
    for protocolo in protocolos:
        url = f"{protocolo}://{ip}:{porta}"
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

                # Salva resultado
                with open("resultados.txt", "a") as f:
                    f.write(f"{url} - {status} - {titulo} - {servidor}\n")

        except requests.exceptions.RequestException:
            pass  # IP offline ou não responde

def iniciar_scanner():
    for ip in gerar_ips():
        for porta in portas:
            t = threading.Thread(target=escanear, args=(ip, porta))
            t.daemon = True
            t.start()
            time.sleep(0.01)  # controle de velocidade

if __name__ == "__main__":
    try:
        iniciar_scanner()
    except KeyboardInterrupt:
        print(Fore.RED + "\nScanner interrompido pelo usuário.")
