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
# utils.py

def display_map(mapa, player_pos):
    os.system("cls" if os.name == "nt" else "clear")
    for i in range(MAP_SIZE):
        row = ""
        for j in range(MAP_SIZE):
            cell = mapa[i][j]
            if [i, j] == player_pos:
                row += f"{districtColor['X']}[X]{cores['reset']} "
            else:
                row += f"[{cell}] "
        print(row)
    print(f"\nInsira {cores['amarelo']}W, A, S ou D{cores['reset']} para se mover. {cores['vermelho']}Voltar{cores['reset']} para sair.")

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

def get_cell_label(x, y):
    district = define_district(x, y)
    if district == 'A':
        initial_x, initial_y = 0, 0
    elif district == 'B':
        initial_x, initial_y = 0, 3
    elif district == 'C':
        initial_x, initial_y = 3, 0
    else:  # D
        initial_x, initial_y = 3, 3
    
    local_x = x - initial_x
    local_y = y - initial_y
    cell_number = (local_x * 3) + local_y + 1
    return f"{district}{cell_number}"

def generate_map():
    mapa = []
    for i in range(MAP_SIZE):
        row = []
        for j in range(MAP_SIZE):
            cell_label = get_cell_label(i, j)
            district = define_district(i, j)
            row.append(f"{districtColor[district]}{cell_label}{cores['reset']}")
        mapa.append(row)
    return mapa

