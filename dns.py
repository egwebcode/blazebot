import subprocess
import time
import os
import threading
import requests

NOME_PAINEL = "EG WEBCODE DNS TESTE"
dns_servers = []
results = []

def limpar():
    os.system("clear")

def banner():
    print(f"""
\033[1;32m╔══════════════════════════════════════╗
║   🧪 {EG WEBCODE DNS MS TESTE} 🧪   ║
╚══════════════════════════════════════╝\033[0m
""")

def menu():
    banner()
    print("[1] COMEÇAR (com DNS padrão)")
    print("[2] ESCOLHER UM ARQUIVO .TXT")
    print("[3] USAR DNS LOCAL")
    print("[4] SAIR")
    return input("\n➤ Escolha uma opção: ")

def carregar_dns_basicos():
    return [
        '1.1.1.1', '8.8.8.8', '9.9.9.9',
        '208.67.222.222', '1.0.0.1', '8.8.4.4',
        '94.140.14.14', '8.26.56.26', '198.101.242.72',
        '185.228.168.9'
    ]

def carregar_de_arquivo(nome):
    try:
        with open(nome) as f:
            return [linha.strip() for linha in f if linha.strip()]
    except:
        print("\n[!] Arquivo inválido ou não encontrado.\n")
        return []

def dns_local_android():
    try:
        saida = subprocess.check_output("getprop | grep dns", shell=True).decode()
        encontrados = set()
        for linha in saida.strip().splitlines():
            if "." in linha:
                dns = linha.split(":")[1].strip().replace("[", "").replace("]", "")
                if dns and dns not in encontrados:
                    encontrados.add(dns)
        return list(encontrados)
    except:
        return []

def testar_dns(ip):
    inicio = time.time()
    try:
        subprocess.run(['dig', '@' + ip, 'google.com', '+timeout=1', '+tries=1', '+short'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        latencia = round((time.time() - inicio) * 1000)
        results.append((ip, latencia))
        print(f"✅ {ip} respondeu em {latencia}ms")
    except:
        print(f"❌ {ip} falhou ou demorou demais")

def get_ip_info():
    try:
        r = requests.get("https://ipinfo.io/json", timeout=5).json()
        return f"""
🌍 IP: {r.get('ip')}
🏢 Provedor: {r.get('org')}
📍 Local: {r.get('city')}, {r.get('region')} - {r.get('country')}
"""
    except:
        return "🌐 Sem conexão com a internet para mostrar IP."

def iniciar_teste(dns_list):
    results.clear()
    print(f"\n🔁 Testando {len(dns_list)} servidores DNS...\n")
    threads = []
    for ip in dns_list:
        t = threading.Thread(target=testar_dns, args=(ip,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    if results:
        results.sort(key=lambda x: x[1])
        print("\n🏆 TOP 5 DNS MAIS RÁPIDOS:\n")
        for ip, ms in results[:5]:
            print(f"🥇 {ip} - {ms}ms")
    else:
        print("\n⚠️ Nenhum DNS respondeu!")

    print("\n🔎 Informação de conexão:")
    print(get_ip_info())

# ======================== EXECUÇÃO ===========================

while True:
    limpar()
    opcao = menu()

    if opcao == '1':
        dns_servers = carregar_dns_basicos()
        limpar()
        banner()
        iniciar_teste(dns_servers)
        input("\n⚙️ Pressione ENTER para voltar ao menu...")

    elif opcao == '2':
        arquivo = input("\n📂 Digite o nome do arquivo .TXT com os DNS: ")
        dns_servers = carregar_de_arquivo(arquivo)
        if dns_servers:
            limpar()
            banner()
            iniciar_teste(dns_servers)
            input("\n⚙️ Pressione ENTER para voltar ao menu...")

    elif opcao == '3':
        dns_servers = dns_local_android()
        if dns_servers:
            limpar()
            banner()
            print("🧠 Usando DNS detectado localmente (getprop):")
            for ip in dns_servers:
                print(f"📡 {ip}")
            iniciar_teste(dns_servers)
        else:
            print("\n[!] Nenhum DNS local detectado!")
        input("\n⚙️ Pressione ENTER para voltar ao menu...")

    elif opcao == '4':
        print("\n👋 Saindo...\n")
        break

    else:
        print("\n[!] Opção inválida. Tente novamente.\n")
        time.sleep(1)
