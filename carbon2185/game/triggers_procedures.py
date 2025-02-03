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


"""
def trigger_procedure(conn):
    cursor = conn.cursor()
    cursor.execute(TRIGGERS_PROCEDURES_SQL)
    conn.commit()
    cursor.close()
