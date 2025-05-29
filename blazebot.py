import time
import requests
import random

# Blaze API para histórico de roletas
BLAZE_API = "https://blaze.com/api/roulette_games/recent"

# Emojis
COLORS = {
    "0": "⚪",  # Branco
    "1": "🔴",  # Vermelho
    "2": "⚫",  # Preto
}

# Mapeamento de resultados (conforme cores)
def get_last_color():
    try:
        response = requests.get(BLAZE_API)
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            result = data[0]['color']
            return str(result)
    except Exception as e:
        print(f"Erro ao obter histórico da Blaze: {e}")
    return None

# Gera uma entrada válida (evita 🔴+⚫ e ⚫+🔴)
def gerar_entrada():
    entradas_validas = [("⚪", "🔴"), ("⚪", "⚫")]
    return random.choice(entradas_validas)

# Loop do bot
def main():
    print("BOT BLAZE ENTRADAS\n")
    entrada_atual = None

    while True:
        cor_atual = get_last_color()
        if cor_atual:
            emoji_cor = COLORS.get(cor_atual, "?")
            print(f"HISTÓRICO: {emoji_cor}")

            entrada = gerar_entrada()
            entrada_str = f"{entrada[0]}+{entrada[1]}"
            print(f"ENTRADA: {entrada_str}")

            # Verifica se a entrada bateu com o resultado atual
            if emoji_cor in entrada:
                print(f"✅ DEU BOM! Resultado: {emoji_cor}\n")
            else:
                print(f"❌ NÃO BATEU! Resultado: {emoji_cor}\n")
        else:
            print("Erro ao obter a última cor da Blaze. Tentando novamente...\n")

        time.sleep(15)  # Espera 15 segundos antes de consultar de novo

if __name__ == "__main__":
    main()
