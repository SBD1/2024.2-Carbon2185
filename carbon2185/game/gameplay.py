from game.models import create_pc, create_npc, interact_with_npc
from game.utils import display_message, generate_map, display_map, move_player
from game.models import get_all_pcs, get_cell_id_by_position, get_player_position, update_player_cell, get_cell_info, listar_missoes_progresso, deletar_personagem, get_inimigos_na_celula, atualizar_hp_inimigo, atualizar_hp_jogador, random, adicionar_recompensa, remover_inimigo, is_safezone
from game.database import create_connection
from game.utils import get_cell_label, display_map, generate_map, move_player
import os 
import time

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
            print("Todos os distritos possuem nove regiões e cada uma conta uma história diferente. Descubra por si mesmo ao explorar o mundo de Carbon2185")
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
            print("\n")
            display_message(f"{cores['vermelho']}Opção inválida. Tente novamente.{cores['reset']}")


def select_character(conn):
    personagens = get_all_pcs(conn)
    
    if not personagens:
        print(f"\n{cores['vermelho']}Nenhum personagem disponível.{cores['reset']}")
        return None
    
    while True:

        print(f"\n{cores['magenta']}Selecione um personagem (ou digite 'voltar' para retornar):{cores['reset']}")
        print("\n")
        for idx, pc in enumerate(personagens, 1):
            print(f"{cores['amarelo']}{idx}.{cores['reset']} {pc['nome']} (HP: {pc['hp_atual']}/{pc['hp']}) (Nível: {pc['nivel']})")
        
        escolha = input("\nEscolha: ").strip().lower()
        
        if escolha == 'voltar':
            return None
        
        try:
            escolha_int = int(escolha)
        except ValueError:
            print(f"{cores['vermelho']}Input inválido. Escolha um número válido.{cores['reset']}")
            continue
        
        if 1 <= escolha_int <= len(personagens):
            return personagens[escolha_int - 1]
        else:
            print(f"{cores['vermelho']}Opção inválida. Tente novamente.{cores['reset']}")

def create_character(conn):
    cursor = conn.cursor()

    display_message(f"{cores['magenta']}\nCriação de personagem:{cores['reset']}\n")

    # 1. Coletar informações básicas primeiro
    nome_personagem = input("Digite o nome do seu personagem: ")
    descricao_personagem = input("\nDigite uma breve descrição do seu personagem: ")

    # 2. Criar Personagem e Inventário ANTES de outras operações
    cursor.execute(""" 
        INSERT INTO Personagem (id_personagem, tipo)
        VALUES (uuid_generate_v4(), 'pc') RETURNING id_personagem;
    """)
    id_personagem = cursor.fetchone()[0]

    cursor.execute(""" 
        INSERT INTO Inventario (id_inventario, quantidade_itens, capacidade_maxima)
        VALUES (uuid_generate_v4(), 0, 10) RETURNING id_inventario;
    """)
    id_inventario = cursor.fetchone()[0]

    # 3. Escolha da facção
    print("\nEscolha sua facção:\n")
    cursor.execute("SELECT id_faccao, nome, descricao, ideologia FROM Faccao")
    faccoes = cursor.fetchall()

    if not faccoes:
        print(f"{cores['vermelho']}Nenhuma facção disponível!{cores['reset']}")
        return

    for idx, faccao in enumerate(faccoes, start=1):
        id_faccao, nome, descricao, ideologia = faccao
        print(f"{cores['amarelo']}{idx}.{cores['reset']} {cores['vermelho']}[{nome}]{cores['reset']} É uma {descricao} Ideologia: {cores['magenta']}{ideologia}{cores['reset']}")

    while True:
        try:
            escolha = int(input("\nEscolha: ")) - 1
            id_faccao_escolhida = faccoes[escolha][0]
            break
        except (IndexError, ValueError):
            print(f"{cores['vermelho']}Escolha inválida!{cores['reset']}")

    # 4. Escolha da classe
    print("\nEscolha sua classe:\n")
    cursor.execute("SELECT id_classe, nome, descricao, hp_bonus, dano_bonus, energia_bonus FROM Classe")
    classes = cursor.fetchall()

    for idx, classe in enumerate(classes, start=1):
        id_classe, nome, descricao, hp_bonus, dano_bonus, energia_bonus = classe
        print(f"{cores['amarelo']}{idx}.{cores['reset']} {cores['magenta']}[{nome}]{cores['reset']} {descricao} (HP: {cores['verde']}+{hp_bonus}{cores['reset']}, Dano: {cores['vermelho']}+{dano_bonus}{cores['reset']}, Energia: {cores['amarelo']}+{energia_bonus}{cores['reset']})")

    while True:
        try:
            escolha = int(input("\nEscolha: ")) - 1
            id_classe_escolhida, _, _, hp_bonus, dano_bonus, energia_bonus = classes[escolha]
            break
        except (IndexError, ValueError):
            print(f"{cores['vermelho']}Escolha inválida!{cores['reset']}")

    # 5. Calcular atributos
    hp_final = 100 + hp_bonus
    dano_final = 20 + dano_bonus
    energia_final = 20 + energia_bonus

    # 6. Pegar célula inicial
    cursor.execute("SELECT id_celula FROM CelulaMundo WHERE eixoX = 0 AND eixoY = 0;")
    celula_inicial = cursor.fetchone()[0]

    # 7. Inserir PC
    cursor.execute("""
    INSERT INTO PC (
        id_personagem, id_celula, id_faccao, id_classe, id_inventario,
        energia, wonglongs, dano, hp, hp_atual, nivel, xp, nome, descricao
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", (
    id_personagem, celula_inicial, id_faccao_escolhida, id_classe_escolhida, id_inventario,
    energia_final, 100, dano_final, hp_final, hp_final, 1, 0, nome_personagem, descricao_personagem
))
    # 8. Adicionar arma inicial (Glock)
    cursor.execute("""
        SELECT i.id_item 
        FROM Item i 
        JOIN Arma a ON i.id_item = a.id_item 
        WHERE i.nome = 'Glock'
    """)
    arma_glock = cursor.fetchone()

    if arma_glock:
        id_arma = arma_glock[0]
        # Adicionar instância da arma no inventário
        cursor.execute("""
            INSERT INTO InstanciaItem (id_instancia_item, id_inventario, id_item)
            VALUES (uuid_generate_v4(), %s, %s)
        """, (id_inventario, id_arma))
        
        # Atualizar quantidade de itens no inventário
        cursor.execute("""
            UPDATE Inventario 
            SET quantidade_itens = quantidade_itens + 1 
            WHERE id_inventario = %s
        """, (id_inventario,))
    else:
        print(f"{cores['vermelho']}Erro: Arma inicial não encontrada!{cores['reset']}")
    conn.commit()
    cursor.close()
    print(f"\nPersonagem {cores['amarelo']}{nome_personagem}{cores['reset']} criado com sucesso!")

# gameplay.py
import time

def navigate_in_the_map(conn, pc):
    game_map = generate_map()
    player_position = get_player_position(conn, pc['id'])
    
    while True:
        display_map(game_map, player_position)
        command = input(f"{cores['amarelo']}Movimento:{cores['reset']} ").lower()

        if command == "voltar":
            final_cell_id = get_cell_id_by_position(conn, *player_position)
            update_player_cell(conn, pc['id'], final_cell_id)
            break
            
        elif command in ["w", "a", "s", "d"]:
            new_position = move_player(command, player_position)
            new_cell_id = get_cell_id_by_position(conn, *new_position)
            
            if new_cell_id:
                print("\n")
                print(f"\n{cores['magenta']}Viajando por Carbon2185...{cores['reset']}")
                time.sleep(3)
                player_position = new_position
                update_player_cell(conn, pc['id'], new_cell_id)
                
                # Verifica se é safezone
                if is_safezone(conn, new_cell_id):
                    print(f"\n{cores['verde']}Este é uma safezone devido à movimentação do mercado clandestino!")
                    print(f"{cores['verde']}Os contrabandistas possuem um acordo de cessar-fogo.{cores['reset']}")
                    time.sleep(3)
                else:
                    # Lógica de combate apenas se não for safezone
                    inimigos = get_inimigos_na_celula(conn, new_cell_id)
                    
                    if inimigos:
                        if random.random() < 0.5:  # 50% de chance de combate
                            os.system("cls" if os.name == "nt" else "clear")
                            resultado = handle_combat(conn, pc, inimigos)
                            if not resultado:
                                deletar_personagem(conn, pc['id'])
                                print("\n")
                                print(f"{cores['vermelho']}=== GAME OVER! ==={cores['reset']}")
                                start_game(conn)
                                break
                        else:
                            print("\n")
                            print(f"\n{cores['ciano']}Você teve sorte! Nenhum inimigo apareceu.{cores['reset']}")
                            time.sleep(2)

                # Restante do código para verificar comerciante e mostrar info da célula
                merchant = check_merchant(conn, new_cell_id)
                if merchant:
                    os.system("cls" if os.name == "nt" else "clear")
                    print(f"\n{cores['ciano']}=== {merchant['nome']} ==={cores['reset']}")
                    print(f"{cores['branco']}{merchant['descricao']}{cores['reset']}\n")
                    choice = input(f"{cores['amarelo']}Deseja interagir? (s/n): {cores['reset']}").lower()
                    if choice == 's':
                        interact_with_merchant(conn, merchant['id_comerciante'], pc['id'])
                        input(f"\n{cores['verde']}Pressione Enter para voltar ao mapa...{cores['reset']}")
                
                cell_info = get_cell_info(conn, new_cell_id)
                display_cell_info(cell_info)
                
            else:
                print(f"{cores['vermelho']}Movimento inválido!{cores['reset']}")
                time.sleep(1)

# Adicione esta nova função
def display_cell_info(cell_info):
    os.system("cls" if os.name == "nt" else "clear")  # Limpa antes de mostrar info
    if cell_info:
        cell_label = get_cell_label(cell_info['eixoX'], cell_info['eixoY'])
        print(f"\n{cores['magenta']}{cell_info['district_name']} - {cell_info['district_desc']}{cores['reset']}")
        print("\n")
        display_message(f"{cores['verde']}Região {cell_label} - {cell_info['cell_name']}:{cores['reset']}")
        print(f"{cores['branco']}{cell_info['cell_desc']}{cores['reset']}\n")
        print("\n")
        input(f"{cores['amarelo']}Pressione Enter para navegar novamente...{cores['reset']}")  # Pausa até confirmação

def playing_with_character(conn, pc):
    
    #Menu principal do jogo quando um personagem é escolhido.
    print("\n")
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
            print("\n")
            display_message(f"Missões disponíveis para {pc['nome']}")
            listar_missoes_progresso(conn, pc['id'])
        elif escolha == "5":  # Agora a opção correta para sair do menu
            print("\n")
            display_message(f"\n{cores['magenta']}Voltando ao menu principal...{cores['reset']}")
            start_game(conn)
            break
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
    cursor = conn.cursor()
    
    # Primeiro pegar a capacidade do inventário
    cursor.execute("""
        SELECT inv.quantidade_itens, inv.capacidade_maxima 
        FROM Inventario inv
        JOIN PC ON PC.id_inventario = inv.id_inventario
        WHERE PC.id_personagem = %s
    """, (id_personagem,))
    quantidade, capacidade = cursor.fetchone()
    
    # Restante do código mantido
    cursor.execute("""
        SELECT 
            ii.id_instancia_item,
            i.nome,
            i.descricao
        FROM InstanciaItem ii
        JOIN Item i ON ii.id_item = i.id_item
        WHERE ii.id_inventario = (
            SELECT id_inventario FROM PC WHERE id_personagem = %s
        )
    """, (id_personagem,))
    itens = cursor.fetchall()
    
    print(f"\n{cores['verde']}Itens no Inventário ({quantidade}/{capacidade}):{cores['reset']}\n")  # Alterado aqui
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

def descartar_item(conn, id_instancia_item, id_personagem):
    cursor = conn.cursor()
    try:
        # Deletar o item
        cursor.execute("""
            DELETE FROM InstanciaItem 
            WHERE id_instancia_item = %s 
            AND id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
        """, (id_instancia_item, id_personagem))
        
        # Atualizar a quantidade no inventário
        cursor.execute("""
            UPDATE Inventario
            SET quantidade_itens = quantidade_itens - 1
            WHERE id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
        """, (id_personagem,))
        
        conn.commit()
        print(f"\n{cores['verde']}Item descartado!{cores['reset']}")
    except Exception as e:
        conn.rollback()
        print(f"{cores['vermelho']}Erro ao descartar item: {e}{cores['reset']}")
    finally:
        cursor.close()

def interact_with_merchant(conn, merchant_id, pc_id):
    cursor = conn.cursor()
    try:
        # Consulta melhorada com informações de atributos
        cursor.execute("""
            SELECT 
                i.nome,
                i.descricao,
                i.valor,
                ii.id_instancia_item,
                i.tipo,
                COALESCE(a.dano, ar.hp_bonus, ic.dano) AS atributo_principal,
                COALESCE(a.municao, ic.custo_energia, 0) AS atributo_secundario
            FROM Loja l
            JOIN InstanciaItem ii ON l.id_instancia_item = ii.id_instancia_item
            JOIN Item i ON ii.id_item = i.id_item
            LEFT JOIN Arma a ON i.id_item = a.id_item
            LEFT JOIN Armadura ar ON i.id_item = ar.id_item
            LEFT JOIN ImplanteCibernetico ic ON i.id_item = ic.id_item
            WHERE l.id_comerciante = %s
        """, (merchant_id,))
        
        items = cursor.fetchall()

        if not items:
            print(f"\n{cores['amarelo']}A loja está em renovação, volte mais tarde!{cores['reset']}")
            return

        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print(f"{cores['ciano']}=== LOJA ==={cores['reset']}")
            
            # Mostra saldo
            cursor.execute("SELECT wonglongs FROM PC WHERE id_personagem = %s", (pc_id,))
            wonglongs = cursor.fetchone()[0]
            print(f"{cores['verde']}Saldo Disponível: {wonglongs} Wonglongs{cores['reset']}\n")

            # Lista detalhada de itens
            for idx, item in enumerate(items, 1):
                tipo = item[4]
                detalhes = ""
                
                if tipo == 'arma':
                    detalhes = f"Dano: {item[5]} | Munição: {item[6]}"
                elif tipo == 'armadura':
                    detalhes = f"HP Bonus: {item[5]}"
                elif tipo == 'implantecibernetico':
                    detalhes = f"Dano: {item[5]} | Custo Energia: {item[6]}"
                
                print(f"{cores['amarelo']}{idx}.{cores['reset']} {item[0]} ({tipo})")
                print(f"   {item[1]}")
                print(f"   {detalhes}")
                print(f"   {cores['verde']}Preço: {item[2]} Wonglongs{cores['reset']}\n")

            print(f"{cores['amarelo']}0. Voltar ao Mapa{cores['reset']}")
            escolha = input("\nEscolha um item: ")

            if escolha == "0":
                break

            try:
                idx = int(escolha) - 1
                if 0 <= idx < len(items):
                    item_escolhido = items[idx]
                    
                    # Verifica saldo
                    if wonglongs >= item_escolhido[2]:
                        # Atualiza inventário
                        cursor.execute("""
                            UPDATE InstanciaItem
                            SET id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = %s)
                            WHERE id_instancia_item = %s
                        """, (pc_id, item_escolhido[3]))
                        
                        # Atualiza Wonglongs
                        cursor.execute("""
                            UPDATE PC
                            SET wonglongs = wonglongs - %s
                            WHERE id_personagem = %s
                        """, (item_escolhido[2], pc_id))
                        
                        cursor.execute("""
                            UPDATE Inventario
                            SET quantidade_itens = quantidade_itens + 1
                            WHERE id_inventario = (
                                SELECT id_inventario FROM PC WHERE id_personagem = %s
                            )
                        """, (pc_id,))
                        
                        conn.commit()
                        print(f"\n{cores['verde']}Compra realizada! {item_escolhido[0]} adicionado ao inventário.{cores['reset']}")
                    else:
                        print(f"\n{cores['vermelho']}Saldo insuficiente!{cores['reset']}")
                    
                    input(f"\n{cores['amarelo']}Pressione Enter para continuar...{cores['reset']}")
                else:
                    print(f"\n{cores['vermelho']}Índice inválido!{cores['reset']}")
                    time.sleep(1)
            except ValueError:
                print(f"\n{cores['vermelho']}Digite um número válido!{cores['reset']}")
                time.sleep(1)
                
    except Exception as e:
        print(f"\n{cores['vermelho']}Erro na transação: {str(e)}{cores['reset']}")
        conn.rollback()
    finally:
        cursor.close()

def check_merchant(conn, cell_id):
    """Verifica se há um comerciante na célula atual e retorna um dicionário"""
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id_comerciante, nome, descricao 
            FROM Comerciante 
            WHERE id_celula = %s
        """, (cell_id,))
        result = cursor.fetchone()
        
        if result:
            return {
                'id_comerciante': result[0],  # Primeira coluna: id_comerciante
                'nome': result[1],           # Segunda coluna: nome
                'descricao': result[2]       # Terceira coluna: descricao
            }
        return None
    finally:
        cursor.close()

def handle_combat(conn, pc, inimigos):
    while inimigos:
        current_enemy = inimigos[0]
        
        print(f"\n{cores['vermelho']}=== COMBATE ==={cores['reset']}")
        print("\n")
        print(f"{cores['amarelo']}Inimigo:{cores['reset']} {cores['magenta']}{current_enemy['nome']}.{cores['reset']}")
        print(f"{cores['amarelo']}Descrição:{cores['reset']} {cores['magenta']}{current_enemy['descricao']}{cores['reset']}")
        print("\n")
        print(f"{cores['amarelo']}HP do inimigo: {cores['reset']}{cores['amarelo']}{cores['vermelho']}{current_enemy['hp_atual']}/{current_enemy['hp_max']}{cores['reset']}{cores['reset']}")
        print("\n")
        print(f"{cores['amarelo']}Seu HP: {cores['reset']}{cores['verde']}{pc['hp_atual']}{cores['reset']}\n")
        print("\n")
        escolha = input(f"{cores['amarelo']}1.{cores['reset']} Atacar\n{cores['amarelo']}2.{cores['reset']} Fugir\n\nEscolha: ")

        if escolha == "1":
            # Jogador ataca
            dano_jogador = pc['dano']
            current_enemy['hp_atual'] = max(0, current_enemy['hp_atual'] - dano_jogador)
            atualizar_hp_inimigo(conn, current_enemy['id'], current_enemy['hp_atual'])
            
            print(f"\n{cores['verde']}Você causou {dano_jogador} de dano!{cores['reset']}")
            print("\n")
            
            if current_enemy['hp_atual'] <= 0:
                print(f"{cores['verde']}Inimigo derrotado!{cores['reset']}")
                adicionar_recompensa(conn, pc['id'], current_enemy['xp'], current_enemy['xp']//2)
                remover_inimigo(conn, current_enemy['id'])
                inimigos.pop(0)
                continue

            # Inimigo contra-ataca
            dano_inimigo = current_enemy['dano']
            novo_hp = max(0, pc['hp_atual'] - dano_inimigo)
            atualizar_hp_jogador(conn, pc['id'], novo_hp)
            
            print(f"{cores['vermelho']}O inimigo contra-atacou causando {dano_inimigo} de dano!{cores['reset']}")
            
            if novo_hp <= 0:
                print("\n")
                print(f"{cores['vermelho']}Você foi derrotado!{cores['reset']}")
                input("Pressione Enter para continuar...")
                return False
                
                
        elif escolha == "2":
            if random.random() < 0.5:  # 50% de chance de fugir
                print("\n")
                print(f"{cores['ciano']}Fuga bem sucedida!{cores['reset']}")
                return True
            else:
                print("\n")
                print(f"{cores['vermelho']}Falha na fuga!{cores['reset']}")
                # Inimigo ataca quando a fuga falha
                dano_inimigo = current_enemy['dano']
                novo_hp = max(0, pc['hp_atual'] - dano_inimigo)
                atualizar_hp_jogador(conn, pc['id'], novo_hp)
                
                print(f"{cores['vermelho']}O inimigo atacou causando {dano_inimigo} de dano!{cores['reset']}")
                
                if novo_hp <= 0:
                    print("\n")
                    print(f"{cores['vermelho']}Você foi derrotado!{cores['reset']}")
                    input("Pressione Enter para voltar ao menu principal...")
                    return False

        else:
            print("Opção inválida!")

        # Atualiza status do PC
        cursor = conn.cursor()
        cursor.execute("SELECT hp_atual FROM PC WHERE id_personagem = %s", (pc['id'],))
        pc['hp_atual'] = cursor.fetchone()[0]
        cursor.close()

    print(f"{cores['verde']}Todos os inimigos foram derrotados!{cores['reset']}")
    input("Pressione Enter para continuar...")
    return True

