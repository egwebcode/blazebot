import time
import requests
import os
import random

# Blaze API
BLAZE_API = "https://blaze.com/api/roulette_games/recent"

# Cores e Emojis
COLORS = {
    "0": "⚪",
    "1": "🔴",
    "2": "⚫",
}

# Entradas válidas possíveis
ENTRADAS_VALIDAS = [("⚪", "🔴"), ("⚪", "⚫")]

# Limpa terminal
def limpar_tela():
    os.system("clear")

# Gera entrada aleatória
def gerar_entrada():
    return random.choice(ENTRADAS_VALIDAS)

# Busca o histórico mais recente
def get_historico_cores():
    try:
        response = requests.get(BLAZE_API)
        data = response.json()
        if isinstance(data, list):
            return [COLORS.get(str(jogo['color']), "?") for jogo in data][:15]
    except:
        pass
    return []

# Mostra painel
def exibir_painel(historico, entrada, entrada_id):
    limpar_tela()
    print("=" * 60)
    print("              🎰 BOT BLAZE DOUBLE - MONITOR")
    print("=" * 60)
    print(f"🕒 Últimos Resultados: {' '.join(historico)}")
    print("-" * 60)
    print(f"🎯 Entrada #{entrada_id}: {entrada[0]} + {entrada[1]}")
    print("-" * 60)
    print("⏳ Aguardando nova rodada...\n")

# Função principal
def main():
    historico_anterior = []
    entrada_id = 1
    entrada = gerar_entrada()

    while True:
        historico = get_historico_cores()
        if not historico or len(historico) < 2:
            print("⏳ Aguardando dados da Blaze...")
            time.sleep(2)
            continue

        # Detecta nova rodada
        if historico != historico_anterior:
            historico_anterior = historico
            exibir_painel(historico, entrada, entrada_id)

            # Gera nova entrada para próxima rodada
            entrada = gerar_entrada()
            entrada_id += 1

        time.sleep(1.5)

# Executa
if __name__ == "__main__":
    main()
