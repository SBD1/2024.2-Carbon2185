import os

cores = {
    'vermelho': '\033[31m',
    'verde': '\033[32m',
    'amarelo': '\033[33m',
    'azul': '\033[34m',
    'magenta': '\033[35m',
    'ciano': '\033[36m',
    'branco': '\033[37m',
    'reset': '\033[0m'  # Reset para a cor padrão
}

districtColor = {
    'A': cores['azul'],
    'B': cores['magenta'],
    'C': cores['verde'],
    'D': cores['branco'],
    'X': cores['vermelho']
}

def display_message(message: str, width: int = 40, underline_char: str = ""):
    # Remove espaços extras no final da mensagem
    cleaned_message = message.strip()
    
    # Calcula o espaçamento necessário para centralizar
    padding = (width - len(cleaned_message)) // 2

    # Centraliza a mensagem
    centered_message = f"{cleaned_message.center(width)}"
    print(centered_message)

    # Centraliza a linha abaixo da mensagem
    underline = underline_char
    centered_underline = f"{underline.center(width)}"
    print(centered_underline)


MAP_SIZE = 6

# Criação do mapa com distritos
def generate_map():
    mapa = []
    for i in range(MAP_SIZE):
        row = []
        for j in range(MAP_SIZE):
            district = define_district(i, j)
            row.append(f"{districtColor[district]}{district}")
        mapa.append(row)
    return mapa

# Define o distrito da célula
def define_district(x, y):
    if x < MAP_SIZE // 2 and y < MAP_SIZE // 2:
        return "A"
    elif x < MAP_SIZE // 2 and y >= MAP_SIZE // 2:
        return "B"
    elif x >= MAP_SIZE // 2 and y < MAP_SIZE // 2:
        return "C"
    else:
        return "D"

# Exibe o mapa com a posição do jogador
def display_map(mapa, player_pos):
    os.system("cls" if os.name == "nt" else "clear")  # Limpa o terminal
    for i in range(MAP_SIZE):
        row = ""
        for j in range(MAP_SIZE):
            if [i, j] == player_pos:
                row += f"{districtColor['X']}[X] "
            else:
                row += f"[{mapa[i][j]}] "
        print(row)
    print(f"\nUse {cores['amarelo']}W{cores['reset']} (cima), {cores['amarelo']}S{cores['reset']} (baixo), {cores['amarelo']}A{cores['reset']} (esquerda), {cores['amarelo']}D{cores['reset']} (direita) para mover. {cores['vermelho']}Voltar{cores['reset']} para sair.")
 
# Movimenta o personagem dentro do limite do mapa
def move_player(move, position):
    x, y = position
    if move == "w" and x > 0:
        x -= 1
    elif move == "s" and x < MAP_SIZE - 1:
        x += 1
    elif move == "a" and y > 0:
        y -= 1
    elif move == "d" and y < MAP_SIZE - 1:
        y += 1
    return [x, y]


