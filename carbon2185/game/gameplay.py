from game.models import create_pc, create_npc, interact_with_npc
from game.utils import display_message

def start_game(conn):
    """
    Inicia o jogo, apresentando as opções e gerenciando o fluxo principal.
    """
    display_message("Bem-vindo ao Carbon2185!")
    while True:
        print("\nEscolha uma opção:")
        print("1. Criar Personagem")
        print("2. Ver Missões")
        print("3. Interagir com NPC")
        print("4. Sair")

        choice = input("Escolha: ")
        if choice == "1":
            create_character(conn)
        elif choice == "2":
            view_missions(conn)
        elif choice == "3":
            interact_with_npc(conn)
        elif choice == "4":
            display_message("Saindo do jogo. Até a próxima!")
            break
        else:
            display_message("Opção inválida. Tente novamente.")

def create_character(conn):
    """
    Gerencia a criação de um personagem.
    """
    print("\nCriação de Personagem:")
    nome = input("Digite o nome do personagem: ")
    descricao = input("Descreva seu personagem: ")
    energia = int(input("Energia inicial: "))
    dano = int(input("Dano inicial: "))
    hp = int(input("HP inicial: "))

    # Criação do personagem no banco de dados
    create_pc(conn, nome, descricao, energia, dano, hp)
    display_message(f"Personagem {nome} criado com sucesso!")

def view_missions(conn):
    """
    Exibe as missões disponíveis no jogo.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id_missao, nome, descricao FROM Missao")
    missions = cursor.fetchall()

    print("\nMissões Disponíveis:")
    for mission in missions:
        print(f"- {mission[1]}: {mission[2]} (ID: {mission[0]})")

    cursor.close()

def interact_with_npc(conn):
    """
    Gerencia a interação com um NPC.
    """
    print("\nInteração com NPC:")
    npc_id = int(input("Digite o ID do NPC: "))

    # Interação com o NPC no banco de dados
    cursor = conn.cursor()
    cursor.execute("SELECT nome, descricao FROM NPC WHERE id_personagem = %s", (npc_id,))
    npc = cursor.fetchone()

    if npc:
        display_message(f"Você encontrou {npc[0]}: {npc[1]}")
        # Logica de interação com o NPC
        interact_with_npc(conn, npc_id)
    else:
        display_message("NPC não encontrado.")

    cursor.close()
