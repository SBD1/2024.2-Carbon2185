from game.models import create_pc, create_npc, interact_with_npc
from game.utils import display_message
from gameplay import inventario



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
    energia = get_valid_input("Energia inicial: ", int)
    dano = get_valid_input("Dano inicial: ", int)
    hp = get_valid_input("HP inicial: ", int)

    # Criação do personagem no banco de dados
    create_pc(conn, nome, descricao, energia, dano, hp)
    display_message(f"Personagem {nome} criado com sucesso!")

def view_missions(conn):
    """
    Exibe as missões disponíveis no jogo.
    """
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_missao, nome, descricao FROM Missao")
            missions = cursor.fetchall()

            print("\nMissões Disponíveis:")
            for mission in missions:
                print(f"- {mission[1]}: {mission[2]} (ID: {mission[0]})")
    except Exception as e:
        display_message(f"Erro ao exibir missões: {e}")

def interact_with_npc(conn):
    """
    Gerencia a interação com um NPC.
    """
    print("\nInteração com NPC:")
    npc_id = get_valid_input("Digite o ID do NPC: ", int)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT nome, descricao FROM NPC WHERE id_personagem = %s", (npc_id,))
            npc = cursor.fetchone()

            if npc:
                display_message(f"Você encontrou {npc[0]}: {npc[1]}")
                npc_interaction(conn, npc_id)
            else:
                display_message("NPC não encontrado.")
    except Exception as e:
        display_message(f"Erro ao interagir com o NPC: {e}")

def npc_interaction(conn, npc_id):
    """
    Lida com a interação real com o NPC.
    """
    print("\nEscolha uma opção:")
    print("1. Falar com o NPC")
    print("2. Comprar itens")
    print("3. Voltar")
    
    escolha = input("Escolha: ")
    if escolha == "1":
        # Implementar a lógica de conversa com o NPC
        display_message("Você conversou com o NPC.")
    elif escolha == "2":
        # Lógica de compra de itens
        pass
    elif escolha == "3":
        return
    else:
        display_message("Opção inválida.")

def inventario(conn, id_personagem):
    """
    Exibe o inventário do personagem e permite usar ou descartar itens.
    """
    try:
        with conn.cursor() as cursor:
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

            if not items:
                display_message("Seu inventário está vazio.")
                return

            while True:
                print("\nItens no Inventário:")
                for idx, item in enumerate(items, 1):
                    print(f"{idx}. {item[1]} - {item[2]} (Valor: {item[3]}, Raridade: {item[4]})")

                print("\nEscolha uma opção:")
                print("1. Usar item")
                print("2. Descartar item")
                print("3. Voltar")

                escolha = input("Escolha: ")

                if escolha == "1":
                    item_idx = get_valid_input("Escolha o número do item para usar: ", int) - 1
                    if 0 <= item_idx < len(items):
                        usar_item(conn, items[item_idx][0], id_personagem)
                        reduzir_item_inventario(conn, items[item_idx][0], id_personagem)
                        break
                    else:
                        display_message("Escolha inválida. Tente novamente.")
                elif escolha == "2":
                    item_idx = get_valid_input("Escolha o número do item para descartar: ", int) - 1
                    if 0 <= item_idx < len(items):
                        descartar_item(conn, items[item_idx][0], id_personagem)
                        break
                    else:
                        display_message("Escolha inválida. Tente novamente.")
                elif escolha == "3":
                    break
                else:
                    display_message("Opção inválida. Tente novamente.")
    except Exception as e:
        display_message(f"Erro ao exibir inventário: {e}")

def get_valid_input(prompt, input_type):
    """
    Valida as entradas do usuário, garantindo que a entrada seja do tipo esperado.
    """
    while True:
        try:
            return input_type(input(prompt))
        except ValueError:
            print(f"Entrada inválida. Por favor, insira um valor válido do tipo {input_type.__name__}.")

def reduzir_item_inventario(conn, id_item, id_personagem):
    """ Reduz a quantidade do item no inventário em uma unidade ou remove se chegar a zero. """
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                DELETE FROM InstanciaItem 
                WHERE id_item = %s AND id_inventario = (
                    SELECT id_inventario FROM PC WHERE id_personagem = %s
                )
                LIMIT 1
            """, (id_item, id_personagem))
            conn.commit()
    except Exception as e:
        display_message(f"Erro ao reduzir item no inventário: {e}")

def descartar_item(conn, id_item, id_personagem):
    """ Remove o item do inventário. """
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM InstanciaItem WHERE id_item = %s AND id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)", (id_item, id_personagem))
            conn.commit()
            display_message("Item descartado com sucesso.")
    except Exception as e:
        display_message(f"Erro ao descartar item: {e}")

def comprar_item(conn, id_item, id_personagem):
    """ Adiciona um item comprado ao inventário do personagem. """
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_inventario FROM PC WHERE id_personagem = %s", (id_personagem,))
            id_inventario = cursor.fetchone()

            if id_inventario:
                cursor.execute("INSERT INTO InstanciaItem (id_inventario, id_item) VALUES (%s, %s)", (id_inventario[0], id_item))
                conn.commit()
                display_message("Item comprado e adicionado ao inventário!")
            else:
                display_message("Erro ao encontrar o inventário do personagem.")
    except Exception as e:
        display_message(f"Erro ao comprar item: {e}")

def loja(conn, id_comerciante, id_personagem, id_celula):
    """ Exibe a loja do comerciante e permite comprar itens apenas nas células 4 dos distritos. """
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_celula FROM PC WHERE id_personagem = %s", (id_personagem,))
            celula_personagem = cursor.fetchone()

            if not celula_personagem or celula_personagem[0] != id_celula:
                display_message("Você só pode acessar a loja na célula 4 de um distrito.")
                return

            cursor.execute("""
                SELECT i.id_item, a.nome, a.descricao, a.valor, a.raridade 
                FROM Loja l
                JOIN InstanciaItem ii ON l.id_instancia_item = ii.id_instancia_item
                JOIN Item i ON ii.id_item = i.id_item
                LEFT JOIN Armadura a ON i.id_item = a.id_item
                WHERE l.id_comerciante = %s
            """, (id_comerciante,))
            itens_loja = cursor.fetchall()

            if not itens_loja:
                display_message("A loja está vazia no momento.")
                return

            while True:
                print("\nItens disponíveis na loja:")
                for idx, item in enumerate(itens_loja, 1):
                    print(f"{idx}. {item[1]} - {item[2]} (Valor: {item[3]}, Raridade: {item[4]})")

                print("\nEscolha uma opção:")
                print("1. Comprar item")
                print("2. Voltar")

                escolha = input("Escolha: ")

                if escolha == "1":
                    item_idx = get_valid_input("Escolha o número do item para comprar: ", int) - 1
                    if 0 <= item_idx < len(itens_loja):
                        comprar_item(conn, itens_loja[item_idx][0], id_personagem)
                        break
                    else:
                        display_message("Escolha inválida. Tente novamente.")
                elif escolha == "2":
                    break
                else:
                    display_message("Opção inválida. Tente novamente.")
    except Exception as e:
        display_message(f"Erro ao acessar a loja: {e}")

