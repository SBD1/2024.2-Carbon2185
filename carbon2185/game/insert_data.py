def insert_initial_data(conn):
    cur = conn.cursor()

    # Lista de distritos com suas regiões
    distritos = [
        {
            "nome": "Distrito A - Ruínas do Noroeste",
            "descricao": "Outrora um centro industrial próspero, o Distrito A agora é um cemitério de fábricas abandonadas e arranha-céus em colapso...",
            "eixoXInicial": 0,
            "eixoYInicial": 0,
            "regioes": [
                {"nome": "Núcleo Enferrujado", "descricao": "O coração do distrito, onde antigas fábricas colapsadas formam um labirinto de aço retorcido. Refúgio de nômades urbanos e caçadores de peças."},
                {"nome": "Torre Fantasma", "descricao": "Um arranha-céu inclinado que serve de base para transmissões piratas da resistência. Seus elevadores quebrados escondem armadilhas para invasores."},
                {"nome": "Terminal Esquecido", "descricao": "Estação de trem subterrânea abandonada, lar de comerciantes clandestinos e mutantes caçadores de sucata."},
                {"nome": "O Abatedouro", "descricao": "Antigo frigorífico transformado em covil de traficantes de órgãos cibernéticos. Peças humanas e robóticas têm o mesmo valor."},
                {"nome": "Passagem dos Espectros", "descricao": "Túneis ferroviários bloqueados, usados pela resistência para movimentação secreta."},
                {"nome": "Chaminé dos Lamentos", "descricao": "Duto industrial que exala vapores tóxicos. Quem sobe até o topo desaparece no nevoeiro."},
                {"nome": "Os Alagados", "descricao": "Áreas industriais submersas em água contaminada. Comunidades sobrevivem em plataformas flutuantes."},
                {"nome": "A Ferrugem", "descricao": "Depósito de máquinas desativadas, território de drones descontrolados e saqueadores."},
                {"nome": "Refúgio das Sombras", "descricao": "Bunker subterrâneo secreto onde líderes rebeldes planejam ataques."}
            ]
        },
        {
            "nome": "Distrito B - O Olho do Regime",
            "descricao": "Fortemente vigiado, o Distrito B abriga a elite tecnocrata e a sede do alto conselho...",
            "eixoXInicial": 0,
            "eixoYInicial": 3,
            "regioes": [
                {"nome": "Câmara Central", "descricao": "Sede do Alto Conselho, onde decisões são tomadas sem interferência humana."},
                {"nome": "Plataforma Zero", "descricao": "Ponto de chegada dos trens a vácuo, com inspeções rigorosas de cidadãos."},
                {"nome": "Planalto das Máquinas", "descricao": "Complexo de IA que regula todas as atividades do distrito."},
                {"nome": "Bastião Sintético", "descricao": "Centro de pesquisa de aprimoramentos cibernéticos para 'otimização' humana."},
                {"nome": "Praça da Ordem", "descricao": "Espaço público com hologramas de propaganda do regime 24h. Rebeliões são punidas instantaneamente."},
                {"nome": "Zona Holográfica", "descricao": "Área de realidade virtual controlada pelo governo para ilusões escapistas."},
                {"nome": "Torre do Julgamento", "descricao": "Tribunal automatizado com execuções transmitidas ao vivo para todos os distritos."},
                {"nome": "Caminho da Submissão", "descricao": "Corredor de prédios de luxo exclusivo para leais ao regime. Traidores são removidos."},
                {"nome": "Porto Digital", "descricao": "Centro de armazenamento de dados protegido por barreiras quânticas. Alvo da resistência."}
            ]
        },
        {
            "nome": "Distrito C - O Abismo de Ferro",
            "descricao": "Após décadas de desastres naturais e negligência do governo...",
            "eixoXInicial": 3,
            "eixoYInicial": 0,
            "regioes": [
                {"nome": "Mercado Sombrio", "descricao": "Coração do submundo onde tudo pode ser comprado: armas, energia roubada, identidades falsas."},
                {"nome": "Torre Quebrada", "descricao": "Esqueleto de prédio inacabado controlado por gangues de tráfico ilegal."},
                {"nome": "Cratera 13", "descricao": "Buraco gigantesco onde sobreviventes vivem sob luzes enferrujadas."},
                {"nome": "Trilhos Mortos", "descricao": "Ferrovia abandonada usada para transporte ilegal de tecnologia."},
                {"nome": "Colmeia de Aço", "descricao": "Habitações empilhadas de contêineres onde famílias dividem cubículos."},
                {"nome": "A Fundição", "descricao": "Fábrica clandestina com trabalhadores à beira do colapso."},
                {"nome": "Refúgio das Engrenagens", "descricao": "Esconderijo de engenheiros renegados criando dispositivos anti-regime."},
                {"nome": "Labirinto das Sombras", "descricao": "Complexo subterrâneo perigoso onde poucos retornam."},
                {"nome": "Última Faísca", "descricao": "Gerador de energia roubado, vital para comunidades rebeldes."}
            ]
        },
        {
            "nome": "Distrito D - Terra Devastada",
            "descricao": "Um experimento fracassado de terraformação deixou o solo envenenado...",
            "eixoXInicial": 3,
            "eixoYInicial": 3,
            "regioes": [
                {"nome": "Minas Negras", "descricao": "Cavernas onde condenados extraem minerais tóxicos por doses de antídoto."},
                {"nome": "Cemitério de Aço", "descricao": "Campo de veículos destruídos desmontados por habitantes famintos."},
                {"nome": "Aurora Envenenada", "descricao": "Centro com luzes artificiais que lembram o fracasso da terraformação."},
                {"nome": "Os Suspiros", "descricao": "Ruínas de hospital, covil de contrabandistas de próteses ilegais."},
                {"nome": "Bairro dos Esquecidos", "descricao": "Prédios fantasmas onde vozes sussurram à noite."},
                {"nome": "Docas Secas", "descricao": "Zona industrial abandonada, esconderijo de foras da lei."},
                {"nome": "Fenda Radioativa", "descricao": "Rachadura no solo com gases letais e corpos petrificados."},
                {"nome": "Refúgio dos Condenados", "descricao": "Comunidade oculta trocando favores por proteção."},
                {"nome": "Catedral Sombria", "descricao": "Templo esquecido, santuário para cultos secretos anti-regime."}
            ]
        }
    ]

    for distrito in distritos:
        nome_distrito = distrito["nome"]
        descricao_distrito = distrito["descricao"]
        eixoX_inicial = distrito["eixoXInicial"]
        eixoY_inicial = distrito["eixoYInicial"]
        regioes = distrito["regioes"]

        # Insere o distrito (mesma lógica de antes)
        cur.execute("""
            INSERT INTO Distrito (id_distrito, nome, descricao) 
            VALUES (uuid_generate_v4(), %s, %s) 
            ON CONFLICT (nome) DO NOTHING
            RETURNING id_distrito;
        """, (nome_distrito, descricao_distrito))
        
        result = cur.fetchone()
        if result:
            id_distrito = result[0]
        else:
            cur.execute("SELECT id_distrito FROM Distrito WHERE nome = %s;", (nome_distrito,))
            id_distrito = cur.fetchone()[0]

        # Insere as regiões como células
        for index, regiao in enumerate(regioes):
            i = index // 3  # 0,0,0,1,1,1,2,2,2
            j = index % 3   # 0,1,2,0,1,2,0,1,2
            eixoX = eixoX_inicial + i
            eixoY = eixoY_inicial + j

            cur.execute("""
                INSERT INTO CelulaMundo (id_distrito, eixoX, eixoY, nome, descricao)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id_distrito, eixoX, eixoY) DO NOTHING;
            """, (id_distrito, eixoX, eixoY, regiao["nome"], regiao["descricao"]))

    conn.commit()
    cur.close()