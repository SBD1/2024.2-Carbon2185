from game.database import create_connection

INSERT_DATA_SQL = """

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


INSERT INTO Classe (id_classe, tipo, nome, descricao, hp_bonus, dano_bonus, energia_bonus)
SELECT uuid_generate_v4(), 'daimyo', 'Daimyo', 'Um soldado forte e resistente, especializado em táticas de combate.', 10, 5, 5
WHERE NOT EXISTS (SELECT 1 FROM Classe WHERE tipo = 'daimyo');

INSERT INTO Classe (id_classe, tipo, nome, descricao, hp_bonus, dano_bonus, energia_bonus)
SELECT uuid_generate_v4(), 'hacker', 'Hacker', 'Especialista em tecnologia e ataques estratégicos, possui muita energia', 5, 5, 10
WHERE NOT EXISTS (SELECT 1 FROM Classe WHERE tipo = 'hacker');

INSERT INTO Classe (id_classe, tipo, nome, descricao, hp_bonus, dano_bonus, energia_bonus)
SELECT uuid_generate_v4(), 'scoundrel', 'Scoundrel', 'Ágil e letal, focado em ataques rápidos, mas com baixa resistência.', 3, 10, 5
WHERE NOT EXISTS (SELECT 1 FROM Classe WHERE tipo = 'scoundrel');

INSERT INTO Faccao (id_faccao, tipo, nome, descricao, ideologia) 
SELECT uuid_generate_v4(), 'yakuza', 'Yakuza', 'máfia japonesa, conhecida por sua honra e disciplina.', 'Lealdade acima de tudo.'
WHERE NOT EXISTS (SELECT 1 FROM Faccao WHERE tipo = 'yakuza');

INSERT INTO Faccao (id_faccao, tipo, nome, descricao, ideologia) 
SELECT uuid_generate_v4(), 'triad', 'Triad', 'organização secreta chinesa, mestre do submundo.', 'O poder nasce da sombra.'
WHERE NOT EXISTS (SELECT 1 FROM Faccao WHERE tipo = 'triad');

INSERT INTO Item (id_item, tipo)
SELECT uuid_generate_v4(), 'equipamento'
WHERE NOT EXISTS (SELECT 1 FROM Item WHERE tipo = 'equipamento');

INSERT INTO Equipamento (id_item, tipo)
SELECT id_item, 'arma' FROM Item WHERE tipo = 'equipamento' 
AND NOT EXISTS (SELECT 1 FROM Equipamento WHERE tipo = 'arma');

INSERT INTO Arma (id_item, id_celula, nome, descricao, valor, raridade, municao, dano)
SELECT id_item, NULL, 'Glock', 'Uma pistola básica', 100, 'comum', 10, 5 
FROM Equipamento WHERE tipo = 'arma'
AND NOT EXISTS (SELECT 1 FROM Arma);


"""
def dml(conn):
    cursor = conn.cursor()
    cursor.execute(INSERT_DATA_SQL)
    conn.commit()
    cursor.close()
