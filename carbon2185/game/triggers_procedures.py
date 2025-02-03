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

"""
def trigger_procedure(conn):
    cursor = conn.cursor()
    cursor.execute(TRIGGERS_PROCEDURES_SQL)
    conn.commit()
    cursor.close()
