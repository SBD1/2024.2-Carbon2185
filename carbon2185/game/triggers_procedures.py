from game.database import create_connection

TRIGGERS_PROCEDURES_SQL = """

CREATE OR REPLACE FUNCTION criar_progresso_missao()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO ProgressoMissao (id_missao, id_personagem, progresso)
    SELECT m.id_missao, NEW.id_personagem, 0
    FROM Missao m;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_criar_progresso_missao') THEN
        CREATE TRIGGER trigger_criar_progresso_missao
        AFTER INSERT ON PC
        FOR EACH ROW
        EXECUTE FUNCTION criar_progresso_missao();
    END IF;
END $$;

CREATE OR REPLACE FUNCTION progredir_missao(id_personagem UUID, id_missao UUID)
RETURNS void AS $$
DECLARE
    progress INT;
BEGIN
    SELECT progresso 
    INTO progress
    FROM ProgressoMissao 
    WHERE id_personagem = id_personagem AND id_missao = id_missao;

    UPDATE ProgressoMissao 
    SET progresso = progress + 1
    WHERE id_personagem = id_personagem AND id_missao = id_missao;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION listar_missoes_progresso(id_personagem UUID)
RETURNS TABLE (
    nome VARCHAR(100),
    descricao VARCHAR(100),
    dificuldade INT,
    objetivo VARCHAR(100),
    progresso INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT m.nome, m.descricao, m.dificuldade, m.objetivo, p.progresso
    FROM Missao m
    JOIN ProgressoMissao p ON m.id_missao = p.id_missao
    WHERE p.id_personagem = $1;
END;
$$ LANGUAGE plpgsql;

DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
BEGIN
    -- Verificar se o comerciante já existe pelo nome
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Doc Carnificina') THEN
        SELECT id_celula INTO celula_id FROM CelulaMundo WHERE nome = 'O Abatedouro' LIMIT 1;
        
        -- Gerar novos UUIDs
        personagem_id := uuid_generate_v4();
        comerciante_id := uuid_generate_v4();
        
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (personagem_id, 'npc')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO NPC (id_personagem, tipo)
        VALUES (personagem_id, 'comerciante')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO Comerciante (id_comerciante, id_personagem, id_celula, nome, descricao)
        VALUES (
            comerciante_id,
            personagem_id,
            celula_id,
            'Doc Carnificina',
            'Cirurgião especializado em implantes cibernéticos de procedência duvidosa'
        )
        ON CONFLICT (nome) DO NOTHING;
    END IF;
END $$;

-- Comerciante para Bastião Sintético (Distrito B)
DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Dr. Vex - "O Escultor de Aço"') THEN
        SELECT id_celula INTO celula_id FROM CelulaMundo WHERE nome = 'Bastião Sintético' LIMIT 1;
        
        personagem_id := uuid_generate_v4();
        comerciante_id := uuid_generate_v4();
        
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (personagem_id, 'npc')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO NPC (id_personagem, tipo)
        VALUES (personagem_id, 'comerciante')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO Comerciante (id_comerciante, id_personagem, id_celula, nome, descricao)
        VALUES (
            comerciante_id,
            personagem_id,
            celula_id,
            'Dr. Vex - "O Escultor de Aço"',
            'Ex-cientista do regime que oferece armas e aprimoramentos cibernéticos experimentais'
        )
        ON CONFLICT (nome) DO NOTHING;
    END IF;
END $$;

-- Comerciante para Trilhos Mortos (Distrito C)
DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Relíquia') THEN
        SELECT id_celula INTO celula_id FROM CelulaMundo WHERE nome = 'Trilhos Mortos' LIMIT 1;
        
        personagem_id := uuid_generate_v4();
        comerciante_id := uuid_generate_v4();
        
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (personagem_id, 'npc')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO NPC (id_personagem, tipo)
        VALUES (personagem_id, 'comerciante')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO Comerciante (id_comerciante, id_personagem, id_celula, nome, descricao)
        VALUES (
            comerciante_id,
            personagem_id,
            celula_id,
            'Relíquia',
            'Mercador de tecnologia obsoleta e protótipos roubados de corporações'
        )
        ON CONFLICT (nome) DO NOTHING;
    END IF;
END $$;

-- Comerciante para Os Suspiros (Distrito D)
DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Lídia "Mãos Leves"') THEN
        SELECT id_celula INTO celula_id FROM CelulaMundo WHERE nome = 'Os Suspiros' LIMIT 1;
        
        personagem_id := uuid_generate_v4();
        comerciante_id := uuid_generate_v4();
        
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (personagem_id, 'npc')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO NPC (id_personagem, tipo)
        VALUES (personagem_id, 'comerciante')
        ON CONFLICT (id_personagem) DO NOTHING;
        
        INSERT INTO Comerciante (id_comerciante, id_personagem, id_celula, nome, descricao)
        VALUES (
            comerciante_id,
            personagem_id,
            celula_id,
            'Lídia "Mãos Leves"',
            'Cirurgiã renegada especialista em próteses biotecnológicas ilegais e armas tecnológicas'
        )
        ON CONFLICT (nome) DO NOTHING;
    END IF;
END $$;

"""
def trigger_procedure(conn):
    cursor = conn.cursor()
    cursor.execute(TRIGGERS_PROCEDURES_SQL)
    conn.commit()
    cursor.close()
