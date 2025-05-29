import time
import requests
import os
import random

# Blaze API para obter histórico de roletas
BLAZE_API = "https://blaze.com/api/roulette_games/recent"

# Emojis
COLORS = {
    "0": "⚪",  # Branco
    "1": "🔴",  # Vermelho
    "2": "⚫",  # Preto
}

# Gera entrada válida (sem vermelho+preto ou preto+vermelho)
def gerar_entrada():
    entradas_validas = [("⚪", "🔴"), ("⚪", "⚫")]
    return random.choice(entradas_validas)

# Limpa a tela no Termux / Linux
def limpar_tela():
    os.system('clear')

# Obtém várias cores anteriores
def get_historico_cores():
    try:
        response = requests.get(BLAZE_API)
        data = response.json()
        if isinstance(data, list):
            return [COLORS.get(str(jogo['color']), "?") for jogo in data]
    except Exception as e:
        print(f"Erro ao obter histórico: {e}")
    return []

# Função principal do bot
def main():
    while True:
        limpar_tela()

        print("BOT BLAZE ENTRADAS\n")

        historico = get_historico_cores()
        if not historico:
            print("Erro ao obter dados da Blaze. Tentando novamente...")
            time.sleep(10)
            continue

        print(f"HISTÓRICOS:{''.join(historico)}")
        print("-" * 37)

        entrada = gerar_entrada()
        entrada_str = f"{entrada[0]}+{entrada[1]}"
        print(f"ENTRADA: {entrada_str}")
        print("AGUARDANDO RESULTADO...")

        time.sleep(15)  # Espera nova rodada

        nova_cor = get_historico_cores()
        if not nova_cor:
            print("Erro ao obter resultado. Tentando novamente...")
            time.sleep(10)
            continue

        resultado = nova_cor[0]
        if resultado in entrada:
            print("DEU GREEN ✅")
        else:
            print("DEU LOSS ❌")

        time.sleep(5)  # Tempo antes de limpar e reiniciar

# Executa
if __name__ == "__main__":
    main()
