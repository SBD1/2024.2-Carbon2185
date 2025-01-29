from game.models import create_pc, create_npc, interact_with_npc
from game.utils import display_message
from gameplay import inventario



def start_game(conn):
    """
    Inicia o jogo, apresentando as opções e gerenciando o fluxo principal.
    """
    display_message("Bem-vindo ao Carbon2185!")
    while True:
        print("\n Escolha uma opção:")
        print("1. Criar Personagem")
        print("2. Ver Missões")
        print("3. Interagir com NPC")
        print("4. Inventário")
        print("5. Sair")

        choice = input("Escolha: ")
        if choice == "1":
            create_character(conn)
        elif choice == "2":
            view_missions(conn)
        elif choice == "3":
            interact_with_npc(conn)
        elif choice == "4":
            id_personagem = input("Digite o ID do seu personagem: ")
            inventario(conn, id_personagem)
        elif choice == "5":
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

def inventario(conn, id_personagem):
    """
    Exibe o inventário do personagem e permite usar ou descartar itens.
    """
    cursor = conn.cursor()
    
    # Recupera o inventário do personagem
    cursor.execute("""
        SELECT i.id_item, a.nome, a.descricao, a.valor, a.raridade 
        FROM InstanciaItem ii
        JOIN Item i ON ii.id_item = i.id_item
        LEFT JOIN Armadura a ON i.id_item = a.id_item
        WHERE ii.id_inventario = (
            SELECT id_inventario FROM PC WHERE id_personagem = %s
        )
    """, (id_personagem,))
    
    items = cursor.fetchall()
    cursor.close()
    
    if not items:
        display_message("Seu inventário está vazio.")
        return
    
    print("\nItens no Inventário:")
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item[1]} - {item[2]} (Valor: {item[3]}, Raridade: {item[4]})")
    
    print("\nEscolha uma opção:")
    print("1. Usar item")
    print("2. Descartar item")
    print("3. Voltar")
    
    escolha = input("Escolha: ")
    
    if escolha == "1":
        item_idx = int(input("Escolha o número do item para usar: ")) - 1
        if 0 <= item_idx < len(items):
            usar_item(conn, items[item_idx][0], id_personagem)
        else:
            display_message("Escolha inválida.")
    elif escolha == "2":
        item_idx = int(input("Escolha o número do item para descartar: ")) - 1
        if 0 <= item_idx < len(items):
            descartar_item(conn, items[item_idx][0], id_personagem)
        else:
            display_message("Escolha inválida.")
    elif escolha == "3":
        return
    else:
        display_message("Opção inválida.")

def usar_item(conn, id_item, id_personagem):
    """ Lógica para usar um item. """
    display_message(f"Você usou o item {id_item}.")

def descartar_item(conn, id_item, id_personagem):
    """ Remove o item do inventário. """
    cursor = conn.cursor()
    cursor.execute("DELETE FROM InstanciaItem WHERE id_item = %s AND id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)", (id_item, id_personagem))
    conn.commit()
    cursor.close()
    display_message("Item descartado com sucesso.")