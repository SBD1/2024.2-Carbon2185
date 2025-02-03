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
    progresso INT,
    recompensa INT
) AS $$
BEGIN
    RETURN QUERY
    SELECT m.nome, m.descricao, m.dificuldade, m.objetivo, p.progresso, m.recompensa
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

CREATE OR REPLACE PROCEDURE Equipar_armadura(
    p_id_personagem UUID,
    p_id_armadura UUID
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO ArmaduraEquipada(id_personagem, id_armadura)
    VALUES (p_id_personagem, p_id_armadura)
    ON CONFLICT (id_personagem) DO NOTHING;
END;
$$;


CREATE OR REPLACE FUNCTION Remover_Armadura(p_id_personagem UUID)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM ArmaduraEquipada
    WHERE id_personagem = p_id_personagem;
END;
$$;



CREATE OR REPLACE FUNCTION Aumentar_hp_por_armadura()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE PC
    SET hp = PC.hp + (SELECT hp_bonus FROM Armadura WHERE id_item = NEW.id_armadura)
    WHERE id_personagem = NEW.id_personagem;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS Trigger_hp_Aumentar_por_armadura ON ArmaduraEquipada;

CREATE TRIGGER Trigger_hp_Aumentar_por_armadura
AFTER INSERT ON ArmaduraEquipada
FOR EACH ROW
EXECUTE FUNCTION Aumentar_hp_por_armadura();



CREATE OR REPLACE FUNCTION Diminuir_hp_por_armadura()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE PC
    SET hp = PC.hp - (SELECT hp_bonus FROM Armadura WHERE id_item = OLD.id_armadura)
    WHERE id_personagem = OLD.id_personagem;
    
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS Trigger_Diminuir_hp_por_armadura ON ArmaduraEquipada;

CREATE TRIGGER Trigger_Diminuir_hp_por_armadura
BEFORE DELETE ON ArmaduraEquipada
FOR EACH ROW
EXECUTE FUNCTION Diminuir_hp_por_armadura();


-- trigger concluir missao e recompensar player
CREATE OR REPLACE FUNCTION concluir_missao()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.progresso >= (SELECT goal FROM Missao WHERE id_missao = NEW.id_missao) THEN
        UPDATE ProgressoMissao
        SET progresso = 0
        WHERE id_missao = NEW.id_missao AND id_personagem = NEW.id_personagem;

        UPDATE PC
        SET wonglongs = wonglongs + (SELECT recompensa FROM Missao WHERE id_missao = NEW.id_missao)
        WHERE id_personagem = NEW.id_personagem;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_concluir_missao ON ProgressoMissao;

CREATE TRIGGER trigger_concluir_missao
AFTER UPDATE ON ProgressoMissao
FOR EACH ROW
EXECUTE FUNCTION concluir_missao();

"""
def trigger_procedure(conn):
    cursor = conn.cursor()
    cursor.execute(TRIGGERS_PROCEDURES_SQL)
    conn.commit()
    cursor.close()
