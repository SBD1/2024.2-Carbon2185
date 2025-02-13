import random
import psycopg2 
import time

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

def create_pc(conn, name, description):
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Inventario (quantidade_itens, capacidade_maxima) 
        VALUES (0, 20) 
        RETURNING id_inventario
    """)
    id_inventario = cursor.fetchone()[0]
    
    cursor.execute(
        """
        INSERT INTO Personagem (tipo)
        VALUES ('pc')
        RETURNING id_personagem
        """
    )
    id_personagem = cursor.fetchone()[0]
    conn.commit()

    cursor.execute(
        """
        INSERT INTO PC (id_personagem, energia, wonglongs, dano, hp, hp_atual, nivel, xp, nome, descricao)
        VALUES (%s, 10, 100, 20, 100, 100, 1, 0, %s, %s)
        """,
        (id_personagem, name, description)
    )
    conn.commit()
    cursor.close()


def interact_with_npc(conn, npc_id, pc_id):
    cursor = conn.cursor()
    cursor.execute("SELECT tipo FROM NPC WHERE id_personagem = %s", (npc_id,))
    npc_type = cursor.fetchone()[0]
    
    if npc_type == 'comerciante':
        cursor.execute("SELECT id_comerciante FROM Comerciante WHERE id_personagem = %s", (npc_id,))
        merchant_id = cursor.fetchone()[0]
        interact_with_merchant(conn, merchant_id, pc_id)
    elif npc_type == 'inimigo':
        print(f"{cores['vermelho']}Prepare-se para lutar!{cores['reset']}")
    cursor.close()

def create_npc(conn, npc_type, id_celula=None):
    """
    Cria um NPC no banco de dados, podendo ser um comerciante ou um inimigo.

    Args:
        conn: Conexão com o banco de dados (psycopg2 connection object).
        npc_type: Tipo do NPC ('comerciante' ou 'inimigo').
        id_celula: (Opcional) ID da célula no mundo onde o NPC estará localizado.
    """
    try:
        with conn.cursor() as cursor:
            # Criar NPC base
            cursor.execute("""
                INSERT INTO NPC (id_personagem, tipo)
                VALUES (DEFAULT, %s)
                RETURNING id_personagem;
            """, (npc_type,))
            id_personagem = cursor.fetchone()[0]

            if npc_type == "comerciante":
                # Gerar dados aleatórios para o comerciante
                nome = f"Comerciante {random.randint(1, 100)}"
                descricao = "Vendedor de itens raros"
                cursor.execute("""
                    INSERT INTO Comerciante (id_personagem, id_celula, nome, descricao)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id_comerciante;
                """, (id_personagem, id_celula, nome, descricao))
                id_comerciante = cursor.fetchone()[0]
                print(f"Comerciante criado com sucesso! ID: {id_comerciante}, Nome: {nome}")

            elif npc_type == "inimigo":
                # Gerar dados aleatórios para o inimigo
                nome = f"Inimigo {random.randint(1, 100)}"
                descricao = "Criatura hostil"
                dano = random.randint(5, 20)
                xp = random.randint(10, 50)
                hp = random.randint(50, 100)
                hp_atual = hp
                cursor.execute("""
                    INSERT INTO Inimigo (id_personagem, id_celula, dano, xp, hp, hp_atual, nome, descricao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id_inimigo;
                """, (id_personagem, id_celula, dano, xp, hp, hp_atual, nome, descricao))
                id_inimigo = cursor.fetchone()[0]
                print(f"Inimigo criado com sucesso! ID: {id_inimigo}, Nome: {nome}, Dano: {dano}, XP: {xp}, HP: {hp}")

            else:
                raise ValueError("Tipo de NPC inválido. Use 'comerciante' ou 'inimigo'.")

            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar NPC: {e}")
        
def progredir_missao(conn, id_personagem, id_missao):
    cursor = conn.cursor()
    
    cursor.execute(
        """
        SELECT progresso 
        FROM ProgressoMissao 
        WHERE id_personagem = %s AND id_missao = %s;
        """,
        (id_personagem, id_missao)
    )
    progresso = cursor.fetchone()[0]

    cursor.execute(
        """
        UPDATE ProgressoMissao 
        SET progresso = %s 
        WHERE id_personagem = %s AND id_missao = %s;
        """,
        (progresso+1, id_personagem, id_missao)
    )
    conn.commit()
    cursor.close()

def loja(conn, id_comerciante, id_personagem, id_celula):
    """Lógica da loja."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT i.id_item, a.nome, a.valor 
        FROM Loja l
        JOIN InstanciaItem ii ON l.id_instancia_item = ii.id_instancia_item
        JOIN Item i ON ii.id_item = i.id_item
        LEFT JOIN Armadura a ON i.id_item = a.id_item
        WHERE l.id_comerciante = %s
    """, (id_comerciante,))
    itens = cursor.fetchall()
    
    print(f"\n{'🏪'*5} LOJA {'🏪'*5}")
    for idx, (id_item, nome, valor) in enumerate(itens, 1):
        print(f"{idx}. {nome} - {valor} wonglongs")
    
    escolha = input("\n1. Comprar\n2. Sair\nEscolha: ")
    if escolha == "1":
        item_idx = int(input("Escolha o item: ")) - 1
        id_item = itens[item_idx][0]
        cursor.execute("SELECT wonglongs FROM PC WHERE id_personagem = %s", (id_personagem,))
        wonglongs = cursor.fetchone()[0]
        
        if wonglongs >= itens[item_idx][2]:
            cursor.execute("UPDATE PC SET wonglongs = wonglongs - %s WHERE id_personagem = %s", 
                          (itens[item_idx][2], id_personagem))
            cursor.execute("""
                INSERT INTO InstanciaItem (id_inventario, id_item)
                VALUES ((SELECT id_inventario FROM PC WHERE id_personagem = %s), %s)
            """, (id_personagem, id_item))
            conn.commit()
            print(f"{'✅'*3} Compra realizada! {'✅'*3}")
        else:
            print(f"{cores['vermelho']}Saldo insuficiente!{cores['reset']}")
    cursor.close()

def get_all_pcs(conn):
    """Retorna uma lista de todos os personagens com todos os atributos necessários."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            id_personagem,
            nome,
            descricao,
            energia,
            wonglongs,
            dano,
            hp,
            hp_atual,
            nivel,
            xp
        FROM PC
    """)
    pcs = cursor.fetchall()
    
    # Convertendo para lista de dicionários
    return [{
        'id': row[0],
        'nome': row[1],
        'descricao': row[2],
        'energia': row[3],
        'wonglongs': row[4],
        'dano': row[5],
        'hp': row[6],
        'hp_atual': row[7],
        'nivel': row[8],
        'xp': row[9]
    } for row in pcs]

# Função para buscar a posição inicial do personagem no banco
def get_player_position(conn, pc_id):
    with conn.cursor() as cur:
        # Consulta corrigida para pegar a posição através da tabela PC
        cur.execute("""
            SELECT cm.eixoX, cm.eixoY 
            FROM CelulaMundo cm
            JOIN PC pc ON cm.id_celula = pc.id_celula
            WHERE pc.id_personagem = %s;
        """, (pc_id,))
        pos = cur.fetchone()
        return list(pos) if pos else [0, 0]  # Fallback seguro

# Função para buscar a célula correspondente no banco
def get_cell_id_by_position(conn, x, y):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id_celula FROM CelulaMundo WHERE eixoX = %s AND eixoY = %s;
        """, (x, y))
        result = cur.fetchone()
        return result[0] if result else None

# Função para atualizar a célula do personagem no banco
def update_player_cell(conn, pc_id, new_cell_id):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE PC SET id_celula = %s WHERE id_personagem = %s;
        """, (new_cell_id, pc_id))
        conn.commit()

# models.py
def get_cell_info(conn, cell_id):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT 
                cm.nome AS cell_name,
                cm.descricao AS cell_desc,
                d.nome AS district_name,
                d.descricao AS district_desc,
                cm.eixoX,
                cm.eixoY
            FROM CelulaMundo cm
            JOIN Distrito d ON cm.id_distrito = d.id_distrito
            WHERE cm.id_celula = %s;
        """, (cell_id,))
        result = cur.fetchone()
        if result:
            return {
                'cell_name': result[0],
                'cell_desc': result[1],
                'district_name': result[2],
                'district_desc': result[3],
                'eixoX': result[4],
                'eixoY': result[5]
            }
        return None

def listar_missoes_progresso(conn, id_personagem):
    try:
        cursor = conn.cursor()
        cursor.callproc('listar_missoes_progresso', (id_personagem,))
        resultados = cursor.fetchall()

        if resultados:
            for row in resultados:
                nome, descricao, dificuldade, objetivo, progresso, recompensa = row
                print(f"{cores['magenta']}Missão:{cores['reset']} {nome}")
                print(f"{cores['amarelo']}Descrição:{cores['reset']} {descricao}")
                print(f"{cores['amarelo']}Dificuldade:{cores['reset']} {dificuldade}")
                print(f"{cores['amarelo']}Objetivo:{cores['reset']} {objetivo}")
                print(f"{cores['amarelo']}Progresso:{cores['reset']} {progresso}")
                print(f"{cores['amarelo']}Recompensa:{cores['reset']} {recompensa} ₩")
                print("\n")

        cursor.close()

    except Exception as e:
        print(f"{cores['vermelho']}Ocorreu um erro:{cores['reset']} {e}")

def progride_missao(conn, id_personagem, id_missao):
    try:
        cursor = conn.cursor()
        cursor.callproc('progredir_missao', (id_personagem, id_missao))
        conn.commit()
        cursor.close()

    except Exception as e:
        print(f"{cores['vermelho']}Ocorreu um erro:{cores['reset']} {e}")

def deletar_personagem(conn, id_personagem):
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM PC WHERE id_personagem = %s", (id_personagem,))
            conn.commit()
            print("\n")
            print(f"{cores['magenta']}Você perdeu, seu personagem foi deletado!{cores['reset']}")
            print("\n")
    except Exception as e:
        conn.rollback()
        print("Erro ao deletar personagem:", e)

import random

import random

import random

import random

def get_inimigos_na_celula(conn, cell_id):
    cursor = conn.cursor()
    
    # 1. Obter as coordenadas GLOBAIS (eixoX, eixoY) da célula
    cursor.execute("""
        SELECT 
            cm.eixoX,
            cm.eixoY,
            cm.local_x,
            cm.local_y,
            d.nome
        FROM CelulaMundo cm
        JOIN Distrito d ON cm.id_distrito = d.id_distrito
        WHERE cm.id_celula = %s;
    """, (cell_id,))
    resultado = cursor.fetchone()
    
    if not resultado:
        cursor.close()
        return []
    
    eixoX, eixoY, local_x, local_y, distrito_nome = resultado
    
    # 2. Verificar se é safezone
    cursor.execute("""
        SELECT (local_x * 3 + local_y + 1) 
        FROM CelulaMundo 
        WHERE id_celula = %s
    """, (cell_id,))
    cell_number = cursor.fetchone()[0]
    
    if cell_number == 4:
        return []  # Safezone

    # 3. Verificar 5% de chance de spawn do boss do distrito
    if random.random() <= 0.03:
        boss_district_mapping = {
            "Distrito A - Ruínas do Noroeste": "Zero.exe",
            "Distrito B - O Olho do Regime": "Tyrant",
            "Distrito C - O Abismo de Ferro": "Orion",
            "Distrito D - Terra devastada": "Viper"
        }
        
        boss_name = boss_district_mapping.get(distrito_nome)
        
        if boss_name:
            # Buscar instância do boss na célula atual
            cursor.execute("""
                SELECT 
                    ii.id_instancia_inimigo,
                    i.nome,
                    i.descricao,
                    ii.hp_atual,
                    i.dano,
                    i.xp,
                    i.hp
                FROM InstanciaInimigo ii
                JOIN Inimigo i ON ii.id_inimigo = i.id_inimigo
                WHERE i.nome = %s
                AND ii.id_celula = %s
            """, (boss_name, cell_id))
            
            boss = cursor.fetchone()
            
            if boss:
                cursor.close()
                return [{
                    'id': boss[0],
                    'nome': boss[1],
                    'hp_atual': boss[3],
                    'dano': boss[4],
                    'xp': boss[5],
                    'hp_max': boss[6],
                    'descricao': boss[2]
                }]

    # 4. Lógica original para inimigos normais
    restricoes = {
        "andarilho corrompido": "Distrito A - Ruínas do Noroeste",
        "drone de supressão": "Distrito B - O Olho do Regime",
        "carrasco da favela": "Distrito C - O Abismo de Ferro",
        "mutante das minas": "Distrito D - Terra devastada"
    }
    
    cursor.execute("""
        SELECT 
            ii.id_instancia_inimigo,
            i.nome,
            i.descricao,
            ii.hp_atual,
            i.dano,
            i.xp,
            i.hp
        FROM InstanciaInimigo ii
        JOIN Inimigo i ON ii.id_inimigo = i.id_inimigo
        WHERE ii.id_celula = %s
    """, (cell_id,))
    inimigos = cursor.fetchall()
    cursor.close()
    
    # 5. Separar os inimigos em restritos e globais
    inimigos_restritos = []
    inimigos_globais = []
    for row in inimigos:
        instancia_id, enemy_name, descricao, hp_atual, dano, xp, hp_max = row
        enemy_name_lower = enemy_name.strip().lower()
        
        if enemy_name_lower in restricoes:
            if distrito_nome == restricoes[enemy_name_lower]:
                inimigos_restritos.append({
                    'id': instancia_id,
                    'nome': enemy_name,
                    'hp_atual': hp_atual,
                    'dano': dano,
                    'xp': xp,
                    'hp_max': hp_max,
                    'descricao': descricao
                })
        else:
            inimigos_globais.append({
                'id': instancia_id,
                'nome': enemy_name,
                'hp_atual': hp_atual,
                'dano': dano,
                'xp': xp,
                'hp_max': hp_max,
                'descricao': descricao
            })

    # 6. Seleção ponderada de inimigos normais
    inimigos_selecionados = []
    vagas = 2
    while vagas > 0 and (inimigos_restritos or inimigos_globais):
        if inimigos_restritos and inimigos_globais:
            if random.random() < 0.75:
                escolhido = random.choice(inimigos_restritos)
                inimigos_restritos.remove(escolhido)
            else:
                escolhido = random.choice(inimigos_globais)
                inimigos_globais.remove(escolhido)
        elif inimigos_restritos:
            escolhido = random.choice(inimigos_restritos)
            inimigos_restritos.remove(escolhido)
        elif inimigos_globais:
            escolhido = random.choice(inimigos_globais)
            inimigos_globais.remove(escolhido)
        inimigos_selecionados.append(escolhido)
        vagas -= 1

    return inimigos_selecionados



def atualizar_hp_inimigo(conn, instancia_id, novo_hp):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE InstanciaInimigo
        SET hp_atual = %s
        WHERE id_instancia_inimigo = %s
    """, (novo_hp, instancia_id))
    conn.commit()
    cursor.close()

def remover_inimigo(conn, instancia_id):
    """Move o inimigo para a sala de respawn ao invés de deletar"""
    cursor = conn.cursor()
    try:
        # 1. Pega os dados do inimigo
        cursor.execute("""
            SELECT id_inimigo, id_celula 
            FROM InstanciaInimigo 
            WHERE id_instancia_inimigo = %s
        """, (instancia_id,))
        id_inimigo, id_celula = cursor.fetchone()

        # 2. Insere na sala de respawn
        cursor.execute("""
            INSERT INTO SalaRespawnInimigos 
                (id_instancia, id_inimigo, id_celula_origem)
            VALUES (%s, %s, %s)
        """, (instancia_id, id_inimigo, id_celula))

        # 3. Remove da tabela principal
        cursor.execute("""
            DELETE FROM InstanciaInimigo 
            WHERE id_instancia_inimigo = %s
        """, (instancia_id,))
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao mover inimigo: {e}")
    finally:
        cursor.close()

def atualizar_hp_jogador(conn, pc_id, novo_hp):
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE PC
        SET hp_atual = %s
        WHERE id_personagem = %s
    """, (novo_hp, pc_id))
    conn.commit()
    cursor.close()

def adicionar_recompensa(conn, pc_id, xp, wonglongs, inimigo_nome):
    cursor = conn.cursor()
    try:       

        # 1. Atualiza XP e Wonglongs do jogador
        cursor.execute("""
            UPDATE PC
            SET 
                xp = xp + %s,
                wonglongs = wonglongs + %s
            WHERE id_personagem = %s
            RETURNING xp, nivel, hp, energia
        """, (xp, wonglongs, pc_id))
        novo_xp, nivel_atual, hp_max, energia = cursor.fetchone()

        # 2. Verifica se houve level up (a cada 100 xp)
        niveis_ganhos = novo_xp // 100
        if niveis_ganhos > 0:
            novo_nivel = nivel_atual + niveis_ganhos
            novo_hp = hp_max + (10 * niveis_ganhos)      # +10 HP por nível ganho
            nova_energia = energia + (10 * novo_nivel)     # Energia base +10 por nível

            cursor.execute("""
                UPDATE PC
                SET 
                    nivel = %s,
                    hp = %s,
                    hp_atual = %s,
                    energia = %s, 
                    xp = xp %% 100  
                WHERE id_personagem = %s
            """, (novo_nivel, novo_hp, novo_hp, nova_energia, pc_id))
            conn.commit()

            # Exibe mensagem de level up
            print(f"\n{cores['magenta']}=== LEVEL UP! ==={cores['reset']}")
            print(f"{cores['verde']}Novo nível: {cores['amarelo']}{novo_nivel}{cores['reset']}")
            print(f"{cores['verde']}HP máximo aumentou para: {cores['amarelo']}{novo_hp}{cores['reset']}")
            print(f"\n{cores['verde']}Energia aumentada para: {cores['amarelo']}{nova_energia}{cores['reset']}")
            time.sleep(5)
        else:
            conn.commit()

        # 3. Atualiza o progresso das missões
        # A consulta agora retorna 3 colunas (id_missao, objetivo e goal) para que o desempacotamento funcione corretamente
        cursor.execute("""
            SELECT id_missao, objetivo, goal
            FROM Missao 
            WHERE objetivo ILIKE %s
        """, (f'%{inimigo_nome}%',))
        missoes = cursor.fetchall()

        for id_missao, objetivo, goal in missoes:
            cursor.execute("""
                UPDATE ProgressoMissao
                SET progresso = progresso + 1
                WHERE id_missao = %s AND id_personagem = %s
            """, (id_missao, pc_id))
                    
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"Erro ao atualizar recompensas: {e}")
    finally:
        cursor.close()

def is_safezone(conn, cell_id):
    """Verifica se a célula é uma safezone (célula 4 do distrito)"""
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT (local_x * 3 + local_y + 1) 
            FROM CelulaMundo 
            WHERE id_celula = %s
        """, (cell_id,))
        result = cursor.fetchone()
        return result and result[0] == 4

def inicializar_inimigos(conn):
    """Garante que inimigos normais estejam instanciados nas células não-safezone"""
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM InstanciaInimigo")
        if cursor.fetchone()[0] == 0:
            # Query corrigida e modificada para excluir bosses
            cursor.execute("""
                INSERT INTO InstanciaInimigo (id_instancia_inimigo, id_inimigo, id_celula, hp_atual)
                SELECT
                    uuid_generate_v4(),
                    i.id_inimigo,
                    cm.id_celula,
                    i.hp
                FROM Inimigo i
                CROSS JOIN CelulaMundo cm
                WHERE 
                    (cm.local_x * 3 + cm.local_y + 1) != 4  -- Condição de safezone corrigida
                    AND i.nome NOT IN (
                        'Zero.exe', 'Tyrant', 'Orion', 'Viper'  -- Exclui bosses
                    )
                    AND cm.id_celula NOT IN (
                        SELECT id_celula FROM Comerciante  -- Exclui células com comerciantes
                    )
            """)
            conn.commit()
            print(f"Inimigos normais inicializados: {cursor.rowcount} instâncias criadas")
            
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inicializar inimigos normais: {str(e)}")
    finally:
        cursor.close()

def inicializar_bosses(conn):
    """Inserir 1 boss em TODAS as células não-safezone do distrito correspondente"""
    boss_district_map = {
        'Zero.exe': 'Distrito A - Ruínas do Noroeste',
        'Tyrant': 'Distrito B - O Olho do Regime',
        'Orion': 'Distrito C - O Abismo de Ferro',
        'Viper': 'Distrito D - Terra devastada'
    }

    cursor = conn.cursor()
    
    try:
        for boss_name, district_name in boss_district_map.items():
            # 1. Obter ID e HP do boss
            cursor.execute("""
                SELECT id_inimigo, hp 
                FROM Inimigo 
                WHERE nome = %s 
                LIMIT 1
            """, (boss_name,))
            boss_data = cursor.fetchone()
            
            if not boss_data:
                print(f"Boss {boss_name} não encontrado!")
                continue
                
            boss_id, boss_hp = boss_data
            
            # 2. Buscar TODAS as células não-safezone do distrito
            cursor.execute("""
                SELECT cm.id_celula 
                FROM CelulaMundo cm
                JOIN Distrito d ON cm.id_distrito = d.id_distrito
                WHERE 
                    d.nome = %s AND
                    (cm.local_x * 3 + cm.local_y + 1) != 4
            """, (district_name,))
            
            celulas = cursor.fetchall()
            
            if not celulas:
                print(f"Nenhuma célula válida em {district_name}")
                continue
                
            # 3. Inserir em todas as células
            inseridos = 0
            for celula in celulas:
                cell_id = celula[0]
                try:
                    cursor.execute("""
                        INSERT INTO InstanciaInimigo 
                            (id_instancia_inimigo, id_inimigo, id_celula, hp_atual)
                        VALUES 
                            (uuid_generate_v4(), %s, %s, %s)
                        ON CONFLICT (id_inimigo, id_celula) DO NOTHING
                    """, (boss_id, cell_id, boss_hp))
                    if cursor.rowcount > 0:
                        inseridos += 1
                except Exception as e:
                    print(f"Erro na célula {cell_id}: {str(e)}")
                    continue
        conn.commit()
        
    except Exception as e:
        conn.rollback()
        print(f"Erro: {str(e)}")
    finally:
        cursor.close()

def respawn_inimigos(conn):
    """Retorna todos os inimigos da sala de respawn para suas células originais"""
    cursor = conn.cursor()
    try:
        # 1. Move os inimigos de volta
        cursor.execute("""
            INSERT INTO InstanciaInimigo (id_instancia_inimigo, id_inimigo, id_celula, hp_atual)
            SELECT 
                sr.id_instancia,
                sr.id_inimigo,
                sr.id_celula_origem,
                i.hp
            FROM SalaRespawnInimigos sr
            JOIN Inimigo i ON sr.id_inimigo = i.id_inimigo
        """)

        # 2. Limpa a sala de respawn
        cursor.execute("DELETE FROM SalaRespawnInimigos")
        
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro no respawn: {e}")
    finally:
        cursor.close()

def get_armas_inventario(conn, pc_id):
    """Retorna todas as armas no inventário do jogador com seus dados"""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            ii.id_instancia_item,
            i.nome,
            a.dano,
            a.municao,
            i.raridade
        FROM InstanciaItem ii
        JOIN Item i ON ii.id_item = i.id_item
        JOIN Arma a ON i.id_item = a.id_item
        WHERE ii.id_inventario = (
            SELECT id_inventario FROM PC WHERE id_personagem = %s
        )
    """, (pc_id,))
    
    armas = [{
        'id': row[0],
        'nome': row[1],
        'dano': row[2],
        'municao': row[3],
        'raridade': row[4]
    } for row in cursor.fetchall()]
    
    cursor.close()
    return armas