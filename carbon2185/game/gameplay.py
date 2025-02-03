from game.models import create_pc, create_npc, interact_with_npc
from game.utils import display_message, generate_map, display_map, move_player
from game.models import get_all_pcs, get_cell_id_by_position, get_player_position, update_player_cell
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
    display_message(f"\n{cores['magenta']}Bem-vindo ao Carbon2185!{cores['reset']}")
    while True:
        print(f"\n{cores['magenta']}Escolha uma opção:{cores['reset']}\n")
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
            print(f"{cores['magenta']}Sobre as classes{cores['reset']}")
            print("\n")
            print(f"Em Carbon2185, existem {cores['magenta']}três{cores['reset']} tipos de classes que você pode escolher e elas variam os atributos {cores['vermelho']}dano{cores['reset']}, {cores['verde']}pontos de vida{cores['reset']} e também a {cores['amarelo']}energia cibernética{cores['reset']} que possuem")
            print("\n")
            print(f"Os atributos são características fundamentais que definem o desempenho de um personagem em Carbon2185. O dano determina a quantidade de ferimentos que você pode causar aos inimigos, enquanto os pontos de vida (HP) indicam a resistência do seu personagem, ou seja, quanto ele pode aguentar de dano antes de ser derrotado. Já a energia cibernética é essencial para o uso de implantes cibernéticos, permitindo ao personagem acessar habilidades e poderes especiais, mas também sendo limitada, exigindo um bom gerenciamento durante as batalhas. Esses atributos moldam o estilo de combate e a sobrevivência de cada classe.")        
            print("\n")
            print(f"{cores['magenta']}As classes{cores['reset']}")
            print("\n")
            display_message(f"{cores['magenta']}Daimyo{cores['reset']}")    
            print(f"O Daimyo é um soldado poderoso e resistente, especializado em táticas de combate. Ele possui um ótimo aumento de bônus de HP (vida) de +10, dano +5 e por fim moderada quantidade de energia cibernética (+5), o que o torna um tanque eficaz para batalhas corpo a corpo.")
            print("\n")
            display_message(f"{cores['magenta']}Hacker{cores['reset']}")
            print(f"O Hacker é um especialista em tecnologia e ataques estratégicos, com uma grande quantidade de energia cibernética (+10), o que lhe permite utilizar uma variedade de implantes avançados. Seu bônus de dano é moderado (+5), e sua resistência (HP) é razoável (+5), permitindo-lhe ser eficaz tanto em combate quanto em táticas cibernéticas.")
            print("\n")
            display_message(f"{cores['magenta']}Scoundrel{cores['reset']}")
            print(f"O Scoundrel é ágil e letal, focado em ataques rápidos e furtivos. Com um grande bônus de dano (+10), ele é capaz de causar grandes ferimentos aos inimigos, mas possui uma resistência reduzida, com apenas +3 de HP. Sua energia cibernética é moderada (+5), permitindo o uso de alguns implantes cibernéticos, mas exige cautela durante as batalhas.")
            print("\n")
            print(f"{cores['magenta']}As facções{cores['reset']}")
            print("\n")
            print(f"Em um mundo cyberpunk dominado por megacorporações e governos decadentes, {cores['magenta']}duas grandes facções{cores['reset']} disputam o controle das ruas e dos distritos. Cada uma delas possui sua própria ideologia, território e métodos para alcançar o poder.")
            print("\n")
            display_message(f"{cores['magenta']}Yakuza{cores['reset']}")
            print("\n")
            print(f"A máfia japonesa, conhecida por sua honra e disciplina, opera sob a filosofia de “Lealdade acima de tudo”. Com uma hierarquia rígida e códigos de conduta inflexíveis, a Yakuza mantém um controle absoluto sobre seus territórios e protege aqueles que juram fidelidade. No entanto, traições são punidas com extrema severidade. A Yazuka possui total controle do {cores['magenta']}Distrito A - Ruínas do Noroeste{cores['reset']} e {cores['magenta']}Distrito D - Terra Devastada{cores['reset']}.")
            print("\n")
            display_message(f"{cores['magenta']}Triad{cores['reset']}")
            print("\n")
            print(f"Uma organização secreta chinesa que reina no submundo, seguindo o lema “O poder nasce da sombra”. A Triad é mestre em manipulação, extorsão e operações clandestinas, utilizando a tecnologia para expandir sua influência e controlar os mercados ilegais. A Triad ocupa atualmente a área do {cores['magenta']}Distrito B - O Olho do Regime{cores['reset']} e {cores['magenta']}Distrito C - O Abismo do Ferro{cores['reset']}.")
            print("\n")
            print(f"{cores['magenta']}Os Distritos{cores['reset']}")
            print("\n")
            display_message(f"{cores['magenta']}Distrito A - Ruínas do Noroeste{cores['reset']}")
            print("\n")
            print("Outrora um centro industrial próspero, o Distrito A agora é um cemitério de fábricas abandonadas e arranha-céus em colapso. A poluição tóxica impregna o ar, e os poucos sobreviventes vivem nas sombras, evitando os drones patrulheiros do governo. A resistência subterrânea usa os túneis antigos como esconderijo.")
            print("\n")
            display_message(f"{cores['magenta']}Distrito B - O Olho do Regime{cores['reset']}")
            print("\n")
            print("Fortemente vigiado, o Distrito B abriga a elite tecnocrata e a sede do alto conselho. Torres de vidro brilham sob a luz artificial, enquanto cidadãos monitorados obedecem às ordens das máquinas que regem suas vidas. Aqui, a tecnologia não é um luxo, mas um instrumento de controle absoluto.")
            print("\n")
            display_message(f"{cores['magenta']}Distrito C - O Abismo de Ferro{cores['reset']}")
            print("\n")
            print("Após décadas de desastres naturais e negligência do governo, o Distrito D afundou em um caos de favelas improvisadas e mercados negros. A energia elétrica é racionada, e os habitantes dependem de contrabandistas e engenhocas caseiras para sobreviver. Gangues de saqueadores dominam as ruínas, enquanto torres de extração exalam fumaça negra no horizonte.")
            print("\n")
            display_message(f"{cores['magenta']}Distrito D - Terra devastada{cores['reset']}")
            print("\n")
            print("Um experimento fracassado de terraformação deixou o solo do Distrito C envenenado. Seus habitantes, chamados de “Os Condenados”, são forçados a trabalhar nas minas subterrâneas em troca de doses de antídoto para a contaminação. O céu sobre o distrito brilha com uma aurora artificial, enquanto os gritos ecoam nos becos da cidade morta.")
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

    print(f"\n{cores['magenta']}Selecione um personagem para jogar:{cores['reset']}\n")
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

    # Criar um inventário para o personagem
    cursor.execute(""" 
        INSERT INTO Inventario (id_inventario, quantidade_itens, capacidade_maxima)
        VALUES (uuid_generate_v4(), 0, 10) RETURNING id_inventario;
    """)
    id_inventario = cursor.fetchone()[0]

    # Criar entrada na tabela PC com o inventário vinculado
    cursor.execute("""
        INSERT INTO PC (id_personagem, id_celula, id_faccao, id_classe, id_inventario, energia, wonglongs, dano, hp, hp_atual, nivel, xp, nome, descricao) 
        VALUES (%s, NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        id_personagem, id_faccao_escolhida, id_classe_escolhida, id_inventario, 
        energia_final, wonglongs, dano_final, hp_final, hp_final, nivel, xp, 
        nome_personagem, descricao_personagem
    ))

    cursor.execute("SELECT id_item FROM Arma ORDER BY id_item LIMIT 1;")
    id_arma = cursor.fetchone()[0]

    # Criar uma instância dessa arma e vinculá-la ao inventário do novo personagem
    cursor.execute("""
        INSERT INTO InstanciaItem (id_instancia_item, id_inventario, id_item)
        VALUES (uuid_generate_v4(), %s, %s);
    """, (id_inventario, id_arma))

    conn.commit()
    cursor.close()

    print(f"\nPersonagem {cores['amarelo']}'{nome_personagem}'{cores['reset']} criado com sucesso, com um inventário associado!")

def navigate_in_the_map(conn, pc):
    print(pc)
    player_position = get_player_position(conn, pc['id'])  # Obtém posição do banco
    game_map = generate_map()

    while True:
        display_map(game_map, player_position)
        command = input("Movimento: ").lower()
        
        if command == "q":
            break
        elif command in ["w", "a", "s", "d"]:
            new_position = move_player(command, player_position)
            new_cell_id = get_cell_id_by_position(conn, new_position[0], new_position[1])

            if new_cell_id:
                player_position = new_position  # Atualiza posição localmente
                update_player_cell(conn, pc['id'], new_cell_id)  # Atualiza no banco
            else:
                print("Movimento inválido! Não há célula nessa posição.")


def playing_with_character(conn, pc):
    
    #Menu principal do jogo quando um personagem é escolhido.

    display_message(f"\n{cores['magenta']}Bem-vindo ao jogo,{cores['reset']} {cores['amarelo']}{pc['nome']}{cores['reset']}{cores['magenta']}!{cores['reset']}")
    while True:
        print(f"\n{cores['magenta']}O que deseja fazer?{cores['reset']}\n")
        print(f"{cores['amarelo']}1.{cores['reset']} Informações do personagem")
        print(f"{cores['amarelo']}2.{cores['reset']} Inventário")
        print(f"{cores['amarelo']}3.{cores['reset']} Explorar")
        print(f"{cores['amarelo']}4.{cores['reset']} Missões disponíveis")
        print(f"{cores['amarelo']}5.{cores['reset']} Voltar\n")
        
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            print("\n")
            display_message(f"{cores['magenta']}Informações sobre {cores['amarelo']}{pc['nome']}{cores['reset']}:{cores['reset']}")
            print("\n")
            mostrar_informacoes_personagem(conn, pc['id'])
        elif escolha == "2":
            print("\n")
            display_message(f"{cores['magenta']}Inventário de {cores['amarelo']}{pc['nome']}{cores['reset']}{cores['reset']}")
            inventario(conn, pc['id'])
        elif escolha == "3":
            navigate_in_the_map(conn, pc)
        elif escolha == "4":
            display_message("Menu das missões devem partir daqui")
        elif escolha == "5":  # Agora a opção correta para sair do menu
            display_message(f"\n{cores['magenta']}Voltando ao menu principal...{cores['reset']}")
            break  # Agora sim, sair do menu do personagem
        else:
            display_message("Opção inválida. Tente novamente.") 

def mostrar_informacoes_personagem(conn, id_personagem):
    """Exibe detalhes do personagem, incluindo o nome da classe e da facção."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            PC.nome,
            PC.descricao,
            PC.nivel,
            PC.xp,
            PC.energia,
            PC.dano,
            PC.hp,
            PC.wonglongs,
            Classe.nome AS nome_classe,
            Faccao.nome AS nome_faccao
        FROM PC
        JOIN Classe ON PC.id_classe = Classe.id_classe
        JOIN Faccao ON PC.id_faccao = Faccao.id_faccao
        WHERE PC.id_personagem = %s
    """, (id_personagem,))
    info = cursor.fetchone()
    
    # Verifica se encontramos informações para o personagem
    if info is None:
        print("Personagem não encontrado.")
        cursor.close()
        return

    print(f"{cores['amarelo']}Nome:{cores['reset']} {info[0]}")
    print(f"{cores['amarelo']}Descrição:{cores['reset']} {info[1]}")
    print(f"{cores['amarelo']}Classe:{cores['reset']} {info[8]}")
    print(f"{cores['amarelo']}Facção:{cores['reset']} {info[9]}")
    print(f"{cores['amarelo']}Nível:{cores['reset']} {info[2]}")
    print(f"{cores['amarelo']}XP:{cores['reset']} {info[3]}")
    print(f"{cores['amarelo']}Energia:{cores['reset']} {info[4]}")
    print(f"{cores['amarelo']}Dano:{cores['reset']} {info[5]}")
    print(f"{cores['amarelo']}HP:{cores['reset']} {info[6]}")
    print(f"{cores['amarelo']}Wonglongs:{cores['reset']} {info[7]}")
    
    cursor.close()

    
def inventario(conn, id_personagem):
    """Gerencia o inventário do personagem informado, listando as instâncias de item associadas."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ii.id_instancia_item,
            COALESCE(a.nome, ar.nome, ic.nome) AS nome,
            COALESCE(a.descricao, ar.descricao, ic.descricao) AS descricao
        FROM InstanciaItem ii
        JOIN Item i ON ii.id_item = i.id_item
        LEFT JOIN Armadura a ON i.id_item = a.id_item
        LEFT JOIN Arma ar ON i.id_item = ar.id_item
        LEFT JOIN ImplanteCibernetico ic ON i.id_item = ic.id_item
        WHERE ii.id_inventario = (
            SELECT id_inventario FROM PC WHERE id_personagem = %s
        )
    """, (id_personagem,))
    itens = cursor.fetchall()
    
    if not itens:
        print(f"{cores['vermelho']}Seu inventário está vazio.{cores['reset']}")
        cursor.close()
        return

    print(f"\n{cores['verde']}Itens no Inventário:{cores['reset']}\n")
    for idx, (id_instancia, nome, desc) in enumerate(itens, start=1):
        print(f"{cores['verde']}{idx}.{cores['reset']} {nome} - {desc}")

    escolha = input(f"\n\n{cores['amarelo']}1.{cores['reset']} Descartar item\n\n{cores['amarelo']}2.{cores['reset']} Voltar\n\nEscolha: ")
    if escolha == "1":
        try:
            entrada = input(f"\nEscolha o número do item para descartar ou digite 'voltar' para sair: ").strip().lower()
            if entrada == "voltar":
                print(f"{cores['amarelo']}Voltando à listagem de itens...{cores['reset']}")
                inventario(conn, id_personagem)
            else:
                item_idx = int(entrada) - 1
                if 0 <= item_idx < len(itens):
                    confirm = input(f"Tem certeza que deseja descartar o item? ({cores['verde']}s{cores['reset']}/{cores['vermelho']}n{cores['reset']}): ").strip().lower()
                    if confirm == 's':
                        descartar_item(conn, itens[item_idx][0], id_personagem)
                    else:
                        print(f"{cores['amarelo']}\nDescartar item cancelado. Voltando à listagem de itens...{cores['reset']}")
                        inventario(conn, id_personagem)  # Retorna à listagem
                else:
                    print(f"{cores['vermelho']}Opção inválida!{cores['reset']}")
        except ValueError:
            print(f"{cores['vermelho']}Entrada inválida!{cores['reset']}")
    # Se a escolha for "2" ou qualquer outra opção, apenas retorna ao menu
    cursor.close()


# def usar_item(conn, id_instancia_item, id_personagem):
#    """Usa um item consumível, removendo a instância do inventário do personagem."""
#    cursor = conn.cursor()
#    cursor.execute
#    
#    ("""
#        DELETE FROM InstanciaItem 
#        WHERE id_instancia_item = %s 
#          AND id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
#    """, (id_instancia_item, id_personagem))
#    conn.commit()
#    print(f"{cores['verde']}Item usado!{cores['reset']}")
#    cursor.close()



def descartar_item(conn, id_instancia_item, id_personagem):
    """Descarta um item, removendo a instância do inventário do personagem."""
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM InstanciaItem 
        WHERE id_instancia_item = %s 
          AND id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
    """, (id_instancia_item, id_personagem))
    conn.commit()
    print(f"\n{cores['verde']}Item descartado!{cores['reset']}")
    cursor.close()

