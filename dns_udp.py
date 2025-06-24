import socket, random, time, threading, os, subprocess

NOME_PAINEL = "EG WEBCODE DNS UDP TUNNEL TESTE"
dns_list = []
resultados = []

def limpar():
    os.system("clear")

def banner():
    print(f"""\033[1;32m
╔══════════════════════════════════════════╗
║   📡 {EG WEBCODE DNS UDP}   ║
╚══════════════════════════════════════════╝\033[0m
""")

def menu():
    banner()
    print("[1] TESTAR DNS BÁSICOS CONHECIDOS")
    print("[2] ESCOLHER UM ARQUIVO .TXT")
    print("[3] TESTAR DNS LOCAL (getprop)")
    print("[4] SAIR")
    return input("\n➤ Escolha uma opção: ")

def construir_query_dns(hostname):
    ID = random.randint(0, 65535)
    FLAGS = 0x0100
    QDCOUNT = 1
    header = ID.to_bytes(2, 'big') + FLAGS.to_bytes(2, 'big') + \
             QDCOUNT.to_bytes(2, 'big') + b'\x00\x00\x00\x00'
    qname = b''.join((len(x).to_bytes(1, 'big') + x.encode() for x in hostname.split('.'))) + b'\x00'
    qtype = (1).to_bytes(2, 'big')
    qclass = (1).to_bytes(2, 'big')
    return header + qname + qtype + qclass

def testar_dns_udp(ip, dominio='google.com', timeout=2):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(timeout)
        consulta = construir_query_dns(dominio)
        inicio = time.time()
        sock.sendto(consulta, (ip, 53))
        resposta, _ = sock.recvfrom(512)
        duracao = round((time.time() - inicio) * 1000)
        if resposta:
            print(f"✅ {ip} respondeu via UDP em {duracao}ms")
            resultados.append((ip, duracao))
    except socket.timeout:
        print(f"❌ {ip} NÃO respondeu (timeout)")
    except Exception as e:
        print(f"❌ {ip} erro: {e}")
    finally:
        sock.close()

def carregar_dns_basicos():
    return [
        '1.1.1.1', '8.8.8.8', '9.9.9.9',
        '208.67.222.222', '1.0.0.1', '8.8.4.4',
        '185.228.168.9', '94.140.14.14'
    ]

def carregar_arquivo(nome):
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

def iniciar_teste_udp(lista):
    resultados.clear()
    print(f"\n🔁 Testando {len(lista)} DNS via UDP...\n")
    threads = []
    for ip in lista:
        t = threading.Thread(target=testar_dns_udp, args=(ip,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    if resultados:
        print("\n🏆 TOP DNS FUNCIONAIS (UDP):\n")
        resultados.sort(key=lambda x: x[1])
        for ip, ms in resultados[:5]:
            print(f"🥇 {ip} - {ms}ms")
    else:
        print("\n⚠️ Nenhum DNS respondeu via UDP.")

# ============ EXECUÇÃO ============

while True:
    limpar()
    opcao = menu()

    if opcao == '1':
        dns_list = carregar_dns_basicos()
        limpar()
        banner()
        iniciar_teste_udp(dns_list)
        input("\n⚙️ Pressione ENTER para voltar ao menu...")

    elif opcao == '2':
        arquivo = input("\n📂 Digite o nome do arquivo .TXT com os DNS: ")
        dns_list = carregar_arquivo(arquivo)
        if dns_list:
            limpar()
            banner()
            iniciar_teste_udp(dns_list)
        input("\n⚙️ Pressione ENTER para voltar ao menu...")

    elif opcao == '3':
        dns_list = dns_local_android()
        if dns_list:
            limpar()
            banner()
            print("🔎 DNS detectado via getprop:")
            for ip in dns_list:
                print(f"📡 {ip}")
            iniciar_teste_udp(dns_list)
        else:
            print("\n[!] Nenhum DNS local detectado.")
        input("\n⚙️ Pressione ENTER para voltar ao menu...")

    elif opcao == '4':
        print("\n👋 Saindo...\n")
        break

    else:
        print("\n[!] Opção inválida. Tente novamente.")
        time.sleep(1)
