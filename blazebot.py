import time
import requests
import os
import random

# Blaze API
BLAZE_API = "https://blaze.com/api/roulette_games/recent"

# Cores e Emojis
COLORS = {
    "0": "⚪",  # Branco
    "1": "🔴",  # Vermelho
    "2": "⚫",  # Preto
}

# Gera uma entrada válida
def gerar_entrada():
    return random.choice([("⚪", "🔴"), ("⚪", "⚫")])

# Limpa tela (Linux/Termux)
def limpar_tela():
    os.system("clear")

# Busca o histórico de resultados
def get_historico_cores():
    try:
        response = requests.get(BLAZE_API)
        data = response.json()
        if isinstance(data, list):
            return [COLORS.get(str(jogo['color']), "?") for jogo in data][:15]  # Últimos 15
    except Exception as e:
        print(f"Erro ao obter histórico: {e}")
    return []

# Exibe painel informativo com estatísticas
def exibir_painel(historico, entrada, greens, losses, total):
    limpar_tela()
    print("=" * 50)
    print("          🎰 BOT BLAZE DOUBLE - MONITOR AO VIVO")
    print("=" * 50)
    print(f"🕒 Últimos Resultados: {' '.join(historico)}")
    print("-" * 50)

    # Estatísticas
    if total > 0:
        porcentagem = (greens / total) * 100
    else:
        porcentagem = 0.0

    print(f"🎯 Entrada atual: {entrada[0]} + {entrada[1]}")
    print(f"✅ GREENS: {greens}   ❌ LOSSES: {losses}   🎯 Assertividade: {porcentagem:.2f}%")
    print("-" * 50)
    print("⏳ Aguardando próximo resultado...\n")

# Função principal
def main():
    greens = 0
    losses = 0
    total = 0
    entrada = gerar_entrada()
    historico_anterior = []

    while True:
        historico = get_historico_cores()
        if not historico or len(historico) < 2:
            print("Aguardando dados válidos da Blaze...")
            time.sleep(2)
            continue

        # Atualiza painel se houver nova rodada
        if historico != historico_anterior:
            resultado = historico[0]

            if resultado in entrada:
                greens += 1
                status = "✅ GREEN!"
            else:
                losses += 1
                status = "❌ LOSS!"

            total += 1
            entrada = gerar_entrada()
            historico_anterior = historico

            exibir_painel(historico, entrada, greens, losses, total)
            print(f"🎲 Resultado: {resultado} → {status}")
            time.sleep(2)
        else:
            time.sleep(2)

# Executar
if __name__ == "__main__":
    main()
