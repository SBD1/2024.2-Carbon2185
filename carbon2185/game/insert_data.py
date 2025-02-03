import psycopg2

def insert_initial_data(conn):
    cur = conn.cursor()
    
    # Lista de distritos a serem criados
    distritos = [
        {"nome": "Distrito A", "descricao": "Distrito ao noroeste da cidade"},
        {"nome": "Distrito B", "descricao": "Distrito ao nordeste da cidade"},
        {"nome": "Distrito C", "descricao": "Distrito ao sudoeste da cidade"},
        {"nome": "Distrito D", "descricao": "Distrito ao sudeste da cidade"}
    ]
    
    # Definição da grade de cada distrito
    largura_distrito = 3  # Células por linha
    altura_distrito = 3   # Células por coluna
    
    # Coordenadas iniciais
    eixoX_inicial = 0
    eixoY_inicial = 0
    
    for distrito in distritos:
        nome_distrito = distrito["nome"]
        descricao_distrito = distrito["descricao"]

        # Insere o distrito, se não existir
        cur.execute("""
            INSERT INTO Distrito (id_distrito, nome, descricao) 
            VALUES (uuid_generate_v4(), %s, %s)
            ON CONFLICT (nome) DO NOTHING
            RETURNING id_distrito;
        """, (nome_distrito, descricao_distrito))
        
        # Se o distrito foi inserido, recupera o ID
        result = cur.fetchone()
        if result:
            id_distrito = result[0]
        else:
            # Se o distrito já existia, obtém o id existente
            cur.execute("SELECT id_distrito FROM Distrito WHERE nome = %s;", (nome_distrito,))
            id_distrito = cur.fetchone()[0]
        
        # Insere as células do distrito, se não existir
        for i in range(altura_distrito):
            for j in range(largura_distrito):
                eixoX = eixoX_inicial + i
                eixoY = eixoY_inicial + j
                nome_celula = f"Célula {chr(65 + distritos.index(distrito))}-{i * largura_distrito + j + 1}"  # Ex: "Célula A-1"
                descricao_celula = f"Parte do {nome_distrito}"

                # Insere a célula, se não existir (com base no id_distrito, eixoX, eixoY)
                cur.execute("""
                    INSERT INTO CelulaMundo (id_distrito, eixoX, eixoY, nome, descricao)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id_distrito, eixoX, eixoY) DO NOTHING;
                """, (id_distrito, eixoX, eixoY, nome_celula, descricao_celula))

        # Atualiza eixoY para que o próximo distrito continue ao lado
        eixoY_inicial += largura_distrito

    conn.commit()
    cur.close()

