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

INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade)
SELECT uuid_generate_v4(), 'arma', 'Glock', 'Uma pistola básica', 100, 'comum'
WHERE NOT EXISTS (SELECT 1 FROM Item WHERE nome = 'Glock');

INSERT INTO Arma (id_item, id_celula, municao, dano)
SELECT id_item, NULL, 10, 5 
FROM Item WHERE nome = 'Glock'
AND NOT EXISTS (SELECT 1 FROM Arma WHERE id_item = (SELECT id_item FROM Item WHERE nome = 'Glock'));

INSERT INTO Inimigo (id_inimigo, id_personagem, dano, xp, hp, nome, descricao)
VALUES
    (uuid_generate_v4(), NULL, 20, 20, 100, 'Andarilho Corrompido', 
    'Um ex-operário transformado em predador urbano após anos de exposição à poluição tóxica. Seus olhos brilham em vermelho sob a máscara de gás improvisada, e ele ataca qualquer um que invada seu território com lâminas enferrujadas.'),

    (uuid_generate_v4(), NULL, 20, 20, 100, 'Drone de Supressão', 
    'Criado para manter a ordem, esse drone flutua silenciosamente entre os becos iluminados do Distrito B. Ele dispara pulsos elétricos para neutralizar qualquer suspeito de insubordinação, registrando cada evento para os servidores centrais do Regime.'),

    (uuid_generate_v4(), NULL, 15, 10, 120, 'Carrasco das Favelas', 
    'Um brutamontes contratado por gangues locais para impor o terror entre os desesperados. Vestindo pedaços de armadura improvisada, ele empunha um enorme martelo hidráulico capaz de esmagar concreto e ossos com facilidade.'),

    (uuid_generate_v4(), NULL, 15, 10, 120, 'Mutante das Minas', 
    'Um mineiro que passou tempo demais exposto à radiação e aos gases tóxicos. Sua pele esverdeada e olhos sem pupilas denunciam a mutação avançada. Ele ataca com unhas endurecidas como lâminas, tentando arrancar o antídoto de qualquer intruso.');

"""
def dml(conn):
    cursor = conn.cursor()
    cursor.execute(INSERT_DATA_SQL)
    conn.commit()
    cursor.close()
