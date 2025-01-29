import random
from gameplay import loja  # Importando loja no topo para evitar problemas de importação.

def create_pc(conn, name, description, energia, dano, hp):
    cursor = conn.cursor()
    
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
        INSERT INTO PC (id_personagem, energia, dano, hp, hp_atual, nivel, xp, nome, descricao)
        VALUES (%s, %s, %s, %s, %s, 1, 0, %s, %s)
        """,
        (id_personagem, energia, dano, hp, hp, name, description)
    )
    conn.commit()
    cursor.close()

def interact_with_npc(conn, npc_id, id_personagem):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT tipo, id_personagem FROM NPC WHERE id_personagem = %s", (npc_id,)
    )
    npc_info = cursor.fetchone()

    if not npc_info:
        print("NPC não encontrado.")
        cursor.close()
        return

    npc_type, id_comerciante = npc_info
    
    if npc_type == 'comerciante':
        print("Este NPC é um comerciante. Você pode comprar itens aqui.")
        cursor.execute("SELECT id_celula FROM Comerciante WHERE id_personagem = %s", (npc_id,))
        id_celula = cursor.fetchone()
        if id_celula:
            loja(conn, id_comerciante, id_personagem, id_celula[0])
        else:
            print("Erro ao localizar a célula do comerciante.")
    elif npc_type == 'inimigo':
        print("Este NPC é um inimigo! Prepare-se para lutar.")
    else:
        print("Nenhuma interação disponível com este NPC.")

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