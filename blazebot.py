import time
import requests
import os
import random

# Blaze API
BLAZE_API = "https://blaze.com/api/roulette_games/recent"

# Cores e emojis
COLORS = {
    "0": "⚪",
    "1": "🔴",
    "2": "⚫",
}

# Entradas válidas
ENTRADAS_VALIDAS = [("⚪", "🔴"), ("⚪", "⚫")]

# Gera entrada aleatória
def gerar_entrada():
    return random.choice(ENTRADAS_VALIDAS)

# Limpa tela do terminal
def limpar_tela():
    os.system("clear")

# Obtém os 15 últimos resultados da Blaze
def get_historico_cores():
    try:
        response = requests.get(BLAZE_API)
        data = response.json()
        if isinstance(data, list):
            return [COLORS.get(str(jogo['color']), "?") for jogo in data][:15]
    except Exception as e:
        print(f"Erro ao obter histórico: {e}")
    return []

# Exibe painel de histórico + entrada
def exibir_painel(historico, entrada, entradas_total):
    limpar_tela()
    print("=" * 60)
    print("              🎰 BOT BLAZE DOUBLE - MONITOR")
    print("=" * 60)
    print(f"🕒 Últimos Resultados: {' '.join(historico)}")
    print("-" * 60)

    entrada_str = f"{entrada[0]} + {entrada[1]}"
    print(f"🎯 Entrada atual: {entrada_str} (entrada #{entradas_total})")
    print("-" * 60)
    print("⏳ Aguardando nova rodada...\n")

# Função principal
def main():
    historico_anterior = []
    entrada = gerar_entrada()
    tempo_ultima_entrada = time.time()
    entradas_total = 1

    while True:
        historico = get_historico_cores()
        if not historico or len(historico) < 2:
            print("⏳ Aguardando dados válidos da Blaze...")
            time.sleep(2)
            continue

        agora = time.time()

        # Nova entrada a cada 10s
        if agora - tempo_ultima_entrada >= 10:
            entrada = gerar_entrada()
            tempo_ultima_entrada = agora
            entradas_total += 1

        # Atualiza o painel se houve mudança no histórico
        if historico != historico_anterior:
            historico_anterior = historico
            exibir_painel(historico, entrada, entradas_total)

        time.sleep(2)

# Inicia
if __name__ == "__main__":
    main()
