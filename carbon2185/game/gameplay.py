from game.models import create_pc, create_npc, interact_with_npc
from game.utils import display_message
from game.models import get_all_pcs 
from game.models import listar_missoes_progresso
from game.database import create_connection

# Códigos de cores ANSI
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

def start_game(conn):
    """ 
    Inicia o jogo, apresentando as opções e gerenciando o fluxo principal.
    """
    display_message(f"{cores['magenta']}Bem-vindo ao Carbon2185!{cores['reset']}")
    while True:
        print("\nEscolha uma opção:\n")
        print(f"{cores['amarelo']}1.{cores['reset']} Selecionar Personagem")
        print(f"{cores['amarelo']}2.{cores['reset']} Criar Personagem")
        print(f"{cores['amarelo']}3.{cores['reset']} Sobre o jogo")
        print(f"{cores['amarelo']}4.{cores['reset']} Sair\n")

        choice = input("Digite o número da sua escolha: ")
        if choice == "1":
            personagem = select_character(conn)
            if personagem:  # Se um personagem for escolhido, inicia o jogo e sai do menu principal
                playing_with_character(conn, personagem)
                break  # Sai do loop principal
        elif choice == "2":
            create_character(conn)
        elif choice == "3":
            print("\n")
            print(f"{cores['magenta']}Sobre o Carbon2185{cores['reset']}")
            print("\n")
            print(f"Carbon 2185 é um RPG cyberpunk focado em contar histórias em um futuro distópico sombrio.")
            print("\n")
            print(f"{cores['magenta']}Como jogar?{cores['reset']}")
            print("\n")
            print(f"A primeira coisa que você, jogador, deve fazer ao iniciar o Carbon 2185 é criar seu personagem, escolhendo um nome e dando uma breve descrição sobre ele. Em seguida, escolha a facção na qual deseja representar e por fim, decida-se sobre sua classe, a qual impactará diretamente a sua gameplay.")
            print("\n")
        elif choice == "4":
            print("\n")
            display_message(f"{cores['magenta']}Saindo do jogo. Até a próxima!{cores['reset']}")
            break
        else:
            display_message(f"{cores['vermelho']}Opção inválida. Tente novamente.{cores['reset']}")


def select_character(conn):
    """
    Lista os personagens existentes no banco de dados e permite ao jogador selecionar um.
    """
    personagens = get_all_pcs(conn)  # Obtém todos os personagens do banco de dados

    if not personagens:
       print(f"{cores['vermelho']}Nenhum personagem encontrado. Crie um primeiro!{cores['reset']}")
       return

    print("\nSelecione um personagem para jogar:\n")
    for i, personagem in enumerate(personagens, start=1):
        print(f"{cores['amarelo']}{i}.{cores['reset']} {personagem['nome']}\n")

    while True:
        try:
            escolha = int(input("Escolha o número do personagem: ")) - 1
            if 0 <= escolha < len(personagens):
                personagem_escolhido = personagens[escolha]
                playing_with_character(conn, personagem_escolhido)  # Chama o menu do jogo com o personagem escolhido
                break
            else:
                print(f"{cores['vermelho']}\nEscolha inválida.\n{cores['reset']}")
        except ValueError:
            print(f"{cores['vermelho']}\nDigite um número válido.\n{cores['reset']}")


def create_character(conn):
    cursor = conn.cursor()

    display_message(f"{cores['magenta']}\nCriação de personagem:{cores['reset']}\n")
    # Informações básicas do personagem
    nome_personagem = input("Digite o nome do seu personagem: ")
    descricao_personagem = input("\nDigite uma breve descrição do seu personagem: ")

    # Escolha da facção
    print("\nEscolha sua facção:\n")
    cursor.execute("SELECT id_faccao, nome, descricao, ideologia FROM Faccao")
    faccoes = cursor.fetchall()

    if not faccoes:
        print(f"{cores['vermelho']}Nenhuma facção disponível no banco de dados!{cores['reset']}")
        return

    for idx, faccao in enumerate(faccoes, start=1):
        id_faccao, nome, descricao, ideologia = faccao
        print(f"{cores['amarelo']}{idx}.{cores['reset']} {cores['vermelho']}[{nome}]{cores['reset']} É a {descricao} Ideologia: {cores['magenta']}{ideologia}{cores['reset']}\n")

    while True:
        try:
            escolha_faccao = int(input("Digite o número da facção escolhida: "))
            if 1 <= escolha_faccao <= len(faccoes):
                id_faccao_escolhida = faccoes[escolha_faccao - 1][0]
                break
            else:
                print(f"{cores['vermelho']}Opção inválida! Escolha um número dentro da lista.{cores['reset']}")
        except ValueError:
            print(f"{cores['vermelho']}Entrada inválida! Digite um número válido.{cores['reset']}")

    # Escolha da classe
    print("\nEscolha sua classe:\n")
    cursor.execute("SELECT id_classe, nome, descricao, hp_bonus, dano_bonus, energia_bonus FROM Classe")
    classes = cursor.fetchall()

    if not classes:
        print(f"{cores['vermelho']}Nenhuma classe encontrada no banco de dados!{cores['reset']}")
        return

    for idx, (id_classe, nome, descricao, hp_bonus, dano_bonus, energia_bonus) in enumerate(classes, start=1):
        print(f"{cores['amarelo']}{idx}.{cores['reset']} {cores['magenta']}[{nome}]{cores['reset']} - {descricao}")
        print(f"     (HP: {cores['verde']}+{hp_bonus:<1}{cores['reset']}, "f"Dano: {cores['vermelho']}+{dano_bonus:<1}{cores['reset']}, "f"Energia: {cores['amarelo']}+{energia_bonus:<1}{cores['reset']})\n")


    while True:
        try:
            escolha_classe = int(input("Digite o número da classe escolhida: "))
            if 1 <= escolha_classe <= len(classes):
                id_classe_escolhida, _, _, hp_bonus, dano_bonus, energia_bonus = classes[escolha_classe - 1]
                break
            else:
                print(f"{cores['vermelho']}Opção inválida! Escolha um número dentro da lista.{cores['reset']}")
        except ValueError:
            print(f"{cores['vermelho']}Entrada inválida! Digite um número válido.{cores['reset']}")

    # Definição dos atributos básicos
    hp_base = 100
    dano_base = 20
    energia_base = 20
    nivel = 1
    xp = 0
    wonglongs = 100

    # Aplicação dos bônus da classe escolhida
    hp_final = hp_base + hp_bonus
    dano_final = dano_base + dano_bonus
    energia_final = energia_base + energia_bonus

    # Criar entrada na tabela Personagem
    cursor.execute(""" 
        INSERT INTO Personagem (id_personagem, tipo)
        VALUES (uuid_generate_v4(), 'pc') RETURNING id_personagem;
    """)
    id_personagem = cursor.fetchone()[0]

    # Criar entrada na tabela PC com os atributos já somados
    cursor.execute("""
        INSERT INTO PC ( id_personagem, id_celula, id_faccao, id_classe, id_inventario, energia, wonglongs, dano, hp, hp_atual, nivel, xp, nome, descricao) 
        VALUES (%s, NULL, %s, %s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        id_personagem, id_faccao_escolhida, id_classe_escolhida, energia_final, wonglongs, dano_final, hp_final, hp_final, nivel, xp, nome_personagem, descricao_personagem
    ))

    conn.commit()
    cursor.close()

    print(f"\nPersonagem {cores['amarelo']}'{nome_personagem}'{cores['reset']} criado com sucesso!")


def playing_with_character(conn, pc):
    
    #Menu principal do jogo quando um personagem é escolhido.
    global id_player
    display_message(f" {cores['magenta']}Bem-vindo ao jogo,{cores['reset']} {cores['amarelo']}{pc['nome']}{cores['reset']}{cores['magenta']}!{cores['reset']}")
    while True:
        print("\nO que deseja fazer?\n")
        print(f"{cores['amarelo']}1.{cores['reset']} Informações do personagem")
        print(f"{cores['amarelo']}2.{cores['reset']} Inventário")
        print(f"{cores['amarelo']}3.{cores['reset']} Explorar")
        print(f"{cores['amarelo']}4.{cores['reset']} Missões disponíveis")
        print(f"{cores['amarelo']}5.{cores['reset']} Voltar\n")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            print("\n")
            display_message(f"{cores['magenta']}Informações sobre {pc['nome']}:{cores['reset']}")
            print("\n")
            mostrar_informacoes_personagem(conn, pc['id'])
        elif escolha == "2":
            display_message("Mecânica do inventário precisar se implentada aqui")
        elif escolha == "3":
            display_message("Exploração deve partir daqui")
        elif escolha == "4":
            display_message("Menu das missões devem partir daqui")
            listar_missoes_progresso(conn, pc['id'])
        elif escolha == "5":  # Agora a opção correta para sair do menu
            display_message(f"Voltando ao menu principal...")
            break  # Agora sim, sair do menu do personagem
        else:
            display_message("Opção inválida. Tente novamente.") 


def mostrar_informacoes_personagem(conn, id_personagem):
    """Exibe detalhes do personagem."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nome, descricao, nivel, xp, energia, dano, hp, wonglongs 
        FROM PC WHERE id_personagem = %s
    """, (id_personagem,))
    info = cursor.fetchone()
    print(f"{cores['amarelo']}Nome:{cores['reset']} {info[0]}")
    print(f"{cores['amarelo']}Descrição:{cores['reset']} {info[1]}")
    print(f"{cores['amarelo']}Nível:{cores['reset']} {info[2]}")
    print(f"{cores['amarelo']}XP:{cores['reset']} {info[3]}")
    print(f"{cores['amarelo']}Energia:{cores['reset']} {info[4]}")
    print(f"{cores['amarelo']}Dano:{cores['reset']} {info[5]}")
    print(f"{cores['amarelo']}HP:{cores['reset']} {info[6]}")
    print(f"{cores['amarelo']}Wonglongs:{cores['reset']} {info[7]}")
    cursor.close()

def inventario(conn, id_personagem):
    """Gerencia o inventário."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id_item, a.nome, a.descricao 
        FROM InstanciaItem ii
        JOIN Item i ON ii.id_item = i.id_item
        LEFT JOIN Armadura a ON i.id_item = a.id_item
        WHERE ii.id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
    """, (id_personagem,))
    itens = cursor.fetchall()
    
    if not itens:
        print(f"{cores['amarelo']}Seu inventário está vazio.{cores['reset']}")
        return

    print(f"\n{cores['verde']}Itens no Inventário:{cores['reset']}")
    for idx, (id_item, nome, desc) in enumerate(itens, 1):
        print(f"{idx}. {nome} - {desc}")

    escolha = input("\n1. Usar item\n2. Descartar\n3. Voltar\nEscolha: ")
    if escolha == "1":
        item_idx = int(input("Escolha o item: ")) - 1
        usar_item(conn, itens[item_idx][0], id_personagem)
    elif escolha == "2":
        item_idx = int(input("Escolha o item: ")) - 1
        descartar_item(conn, itens[item_idx][0], id_personagem)
    cursor.close()

def usar_item(conn, id_item, id_personagem):
    """Usa um item consumível."""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM InstanciaItem 
        WHERE id_item = %s 
        AND id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
        LIMIT 1
    """, (id_item, id_personagem))
    conn.commit()
    print(f"{cores['verde']}Item usado!{cores['reset']}")
    cursor.close()

def descartar_item(conn, id_item, id_personagem):
    """Descarta um item."""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM InstanciaItem 
        WHERE id_item = %s 
        AND id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
    """, (id_item, id_personagem))
    conn.commit()
    print(f"{cores['verde']}Item descartado!{cores['reset']}")
    cursor.close()
