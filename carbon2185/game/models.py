import random
import psycopg2

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
        # Lógica de combate aqui
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
    """
    Retorna uma lista de todos os personagens do banco de dados no PostgreSQL.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id_personagem, nome, descricao FROM PC")  # Ajuste os campos conforme necessário
    PC = cursor.fetchall()  # Obtém todos os personagens

    # Convertendo a lista de tuplas para uma lista de dicionários
    return [{"id": row[0], "nome": row[1]} for row in PC]


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
                nome, descricao, dificuldade, objetivo, progresso = row
                print(f"{cores['magenta']}Missão:{cores['reset']} {nome}")
                print(f"{cores['amarelo']}Descrição:{cores['reset']} {descricao}")
                print(f"{cores['amarelo']}Dificuldade:{cores['reset']} {dificuldade}")
                print(f"{cores['amarelo']}Objetivo:{cores['reset']} {objetivo}")
                print(f"{cores['amarelo']}Progresso:{cores['reset']} {progresso}")
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
            print("Personagem deletado com sucesso.")
    except Exception as e:
        conn.rollback()
        print("Erro ao deletar personagem:", e)