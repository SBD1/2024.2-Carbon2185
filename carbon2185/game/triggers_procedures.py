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

-- COMERCIANTES CORRIGIDOS (SEM REPETIÇÃO DE ITENS)
-- Doc Carnificina (Distrito A)
DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
    item_record RECORD;
    instancia_id UUID;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Doc Carnificina') THEN
        -- Cria NPC
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (uuid_generate_v4(), 'npc') 
        RETURNING id_personagem INTO personagem_id;

        INSERT INTO NPC (id_personagem, tipo) 
        VALUES (personagem_id, 'comerciante');

        -- Localiza célula
        SELECT id_celula INTO celula_id 
        FROM CelulaMundo 
        WHERE nome = 'O Abatedouro';

        -- Cria Comerciante
        INSERT INTO Comerciante (
            id_comerciante, 
            id_personagem, 
            id_celula, 
            nome, 
            descricao
        ) VALUES (
            uuid_generate_v4(),
            personagem_id,
            celula_id,
            'Doc Carnificina',
            'Cirurgião especializado em armas e implantes cibernéticos de procedência duvidosa'
        )
        RETURNING id_comerciante INTO comerciante_id;

        -- Cria instâncias únicas para cada item
        FOR item_record IN 
            SELECT id_item 
            FROM Item 
            WHERE tipo != 'objeto_mapa'
        LOOP
            INSERT INTO InstanciaItem (id_instancia_item, id_item)
            VALUES (uuid_generate_v4(), item_record.id_item)
            RETURNING id_instancia_item INTO instancia_id;

            INSERT INTO Loja (id_comerciante, id_instancia_item)
            VALUES (comerciante_id, instancia_id);
        END LOOP;
    END IF;
END $$ LANGUAGE plpgsql;

-- Dr. Vex (Distrito B)
DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
    item_record RECORD;
    instancia_id UUID;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Dr. Vex - "O Escultor de Aço"') THEN
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (uuid_generate_v4(), 'npc') 
        RETURNING id_personagem INTO personagem_id;

        INSERT INTO NPC (id_personagem, tipo) 
        VALUES (personagem_id, 'comerciante');

        SELECT id_celula INTO celula_id 
        FROM CelulaMundo 
        WHERE nome = 'Bastião Sintético';

        INSERT INTO Comerciante (
            id_comerciante, 
            id_personagem, 
            id_celula, 
            nome, 
            descricao
        ) VALUES (
            uuid_generate_v4(),
            personagem_id,
            celula_id,
            'Dr. Vex - "O Escultor de Aço"',
            'Ex-cientista do regime que oferece armas e aprimoramentos cibernéticos experimentais'
        )
        RETURNING id_comerciante INTO comerciante_id;

        FOR item_record IN 
            SELECT id_item 
            FROM Item 
            WHERE tipo != 'objeto_mapa'
        LOOP
            INSERT INTO InstanciaItem (id_instancia_item, id_item)
            VALUES (uuid_generate_v4(), item_record.id_item)
            RETURNING id_instancia_item INTO instancia_id;

            INSERT INTO Loja (id_comerciante, id_instancia_item)
            VALUES (comerciante_id, instancia_id);
        END LOOP;
    END IF;
END $$ LANGUAGE plpgsql;

-- Relíquia (Distrito C)
DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
    item_record RECORD;
    instancia_id UUID;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Relíquia') THEN
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (uuid_generate_v4(), 'npc') 
        RETURNING id_personagem INTO personagem_id;

        INSERT INTO NPC (id_personagem, tipo) 
        VALUES (personagem_id, 'comerciante');

        SELECT id_celula INTO celula_id 
        FROM CelulaMundo 
        WHERE nome = 'Trilhos Mortos';

        INSERT INTO Comerciante (
            id_comerciante, 
            id_personagem, 
            id_celula, 
            nome, 
            descricao
        ) VALUES (
            uuid_generate_v4(),
            personagem_id,
            celula_id,
            'Relíquia',
            'Mercador de tecnologia obsoleta e protótipos roubados de corporações'
        )
        RETURNING id_comerciante INTO comerciante_id;

        FOR item_record IN 
            SELECT id_item 
            FROM Item 
            WHERE tipo != 'objeto_mapa'
        LOOP
            INSERT INTO InstanciaItem (id_instancia_item, id_item)
            VALUES (uuid_generate_v4(), item_record.id_item)
            RETURNING id_instancia_item INTO instancia_id;

            INSERT INTO Loja (id_comerciante, id_instancia_item)
            VALUES (comerciante_id, instancia_id);
        END LOOP;
    END IF;
END $$ LANGUAGE plpgsql;

-- Lídia (Distrito D)
DO $$
DECLARE 
    personagem_id UUID;
    comerciante_id UUID;
    celula_id UUID;
    item_record RECORD;
    instancia_id UUID;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Comerciante WHERE nome = 'Lídia "Mãos Leves"') THEN
        INSERT INTO Personagem (id_personagem, tipo) 
        VALUES (uuid_generate_v4(), 'npc') 
        RETURNING id_personagem INTO personagem_id;

        INSERT INTO NPC (id_personagem, tipo) 
        VALUES (personagem_id, 'comerciante');

        SELECT id_celula INTO celula_id 
        FROM CelulaMundo 
        WHERE nome = 'Os Suspiros';

        INSERT INTO Comerciante (
            id_comerciante, 
            id_personagem, 
            id_celula, 
            nome, 
            descricao
        ) VALUES (
            uuid_generate_v4(),
            personagem_id,
            celula_id,
            'Lídia "Mãos Leves"',
            'Cirurgiã renegada especialista em próteses biotecnológicas ilegais e armas tecnológicas'
        )
        RETURNING id_comerciante INTO comerciante_id;

        FOR item_record IN 
            SELECT id_item 
            FROM Item 
            WHERE tipo != 'objeto_mapa'
        LOOP
            INSERT INTO InstanciaItem (id_instancia_item, id_item)
            VALUES (uuid_generate_v4(), item_record.id_item)
            RETURNING id_instancia_item INTO instancia_id;

            INSERT INTO Loja (id_comerciante, id_instancia_item)
            VALUES (comerciante_id, instancia_id);
        END LOOP;
    END IF;
END $$ LANGUAGE plpgsql;

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

CREATE OR REPLACE FUNCTION respawn_inimigos() 
RETURNS VOID 
AS $$
BEGIN
    -- Insere os inimigos de volta nas células originais
    INSERT INTO InstanciaInimigo (id_instancia_inimigo, id_inimigo, id_celula, hp_atual)
    SELECT 
        sr.id_instancia,
        sr.id_inimigo,
        sr.id_celula_origem,
        i.hp
    FROM SalaRespawnInimigos sr
    JOIN Inimigo i ON sr.id_inimigo = i.id_inimigo;

    -- Limpa a sala de respawn
    DELETE FROM SalaRespawnInimigos;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE repor_municao(pc_id UUID)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE Arma a
    SET municao = CASE i.raridade
        WHEN 'Lendário' THEN 15
        WHEN 'Raro' THEN 10
        ELSE 5
    END
    FROM InstanciaItem ii
    JOIN Item i ON ii.id_item = i.id_item
    WHERE a.id_item = i.id_item
    AND ii.id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = pc_id);
    
    UPDATE PC
    SET wonglongs = wonglongs - 20
    WHERE id_personagem = pc_id;
END;
$$;


"""
def trigger_procedure(conn):
    cursor = conn.cursor()
    cursor.execute(TRIGGERS_PROCEDURES_SQL)
    conn.commit()
    cursor.close()
