import socket
import random
import time

def construir_query_dns(hostname):
    ID = random.randint(0, 65535)
    FLAGS = 0x0100  # padrão para consulta padrão recursiva
    QDCOUNT = 1
    header = ID.to_bytes(2, 'big') + FLAGS.to_bytes(2, 'big') + QDCOUNT.to_bytes(2, 'big') + b'\x00\x00\x00\x00'
    qname = b''.join(len(part).to_bytes(1, 'big') + part.encode() for part in hostname.split('.')) + b'\x00'
    qtype = (1).to_bytes(2, 'big')  # tipo A
    qclass = (1).to_bytes(2, 'big')  # classe IN
    return header + qname + qtype + qclass

def testar_dns_udp(ip, dominio='google.com', timeout=3):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)
    query = construir_query_dns(dominio)
    try:
        start = time.time()
        sock.sendto(query, (ip, 53))
        resposta, _ = sock.recvfrom(512)
        elapsed = round((time.time() - start) * 1000)
        if resposta:
            print(f"✅ {ip} respondeu via UDP em {elapsed}ms")
            return True
    except socket.timeout:
        print(f"❌ {ip} NÃO respondeu (timeout)")
    except Exception as e:
        print(f"❌ {ip} erro: {e}")
    finally:
        sock.close()
    return False

if __name__ == "__main__":
    test_dns = "1.1.1.1"
    print(f"Testando DNS UDP: {test_dns}")
    testar_dns_udp(test_dns)
