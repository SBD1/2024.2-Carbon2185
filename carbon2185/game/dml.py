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
    'Um mineiro que passou tempo demais exposto à radiação e aos gases tóxicos. Sua pele esverdeada e olhos sem pupilas denunciam a mutação avançada. Ele ataca com unhas endurecidas como lâminas, tentando arrancar o antídoto de qualquer intruso.'),

    (uuid_generate_v4(), NULL, 10, 5, 100, 'Saqueador Nômade', 
    'Vagando entre os distritos, o Saqueador Nômade sobrevive pilhando suprimentos e eliminando qualquer um que represente uma ameaça. Sua máscara remendada esconde um rosto cheio de cicatrizes, e suas lâminas afiadas refletem a luz neon dos becos escuros.'),

    (uuid_generate_v4(), NULL, 10, 5, 100, 'Caçador de Recompensas', 
    'Equipado com sensores térmicos e um arsenal de armas customizadas, o Caçador de Recompensas rastreia alvos para o regime e para os criminosos ricos. Ele não tem lealdade, apenas um preço. Se seu nome estiver em sua lista, prepare-se para fugir... ou lutar pela vida.')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Missao (id_missao, nome, descricao, dificuldade, objetivo, goal) VALUES
    (uuid_generate_v4(), 'Silenciando as Máquinas', 'Desative os Drones de Supressão antes que alertem as autoridades.', 2, 'Destruir 40 Drones de Supressão', 40),
    (uuid_generate_v4(), 'Revolta nas Favelas', 'Derrote os Carrascos das Favelas que aterrorizam os moradores.', 2, 'Eliminar 40 Carrascos das Favelas', 40),
    (uuid_generate_v4(), 'Expurgo Urbano', 'Elimine os Andarilhos Corrompidos que espreitam nos becos abandonados.', 3, 'Derrotar 30 Andarilhos Corrompidos', 30),
    (uuid_generate_v4(), 'Caçada Radioativa', 'Neutralize os Mutantes das Minas antes que se espalhem pela cidade.', 4, 'Eliminar 30 Mutantes das Minas', 30),
    (uuid_generate_v4(), 'O Regime não Dorme', 'Enfrente os Drones de Supressão e impeça a vigilância implacável.', 5, 'Destruir 30 Drones de Supressão', 30),
    (uuid_generate_v4(), 'Justiça nas Sombras', 'Acabe com a rede de violência imposta pelos Carrascos das Favelas.', 5, 'Eliminar 30 Carrascos das Favelas', 30),
    (uuid_generate_v4(), 'Terror Cibernético', 'Zero.exe, um hacker AI autoconsciente, está tomando o controle de sistemas de defesa.', 6, 'Derrotar Zero.exe', 1),
    (uuid_generate_v4(), 'Caçada ao Tyrant', 'Tyrant, um cyber-ogro modificado, lidera os Steel Fangs em massacres brutais.', 6, 'Derrotar Tyrant', 1),
    (uuid_generate_v4(), 'O Guardião do Labirinto', 'A megacorp Shinsei Biotech criou um super-soldado, Orion, para proteger seus segredos.', 7, 'Derrotar Orion', 1),
    (uuid_generate_v4(), 'Rei dos Bairros Baixos', 'Viper, um ex-executivo transformado em rei do crime, governa o submundo com punho de ferro.', 8, 'Derrotar Viper', 1)
ON CONFLICT (nome) DO NOTHING;


"""
def dml(conn):
    cursor = conn.cursor()
    cursor.execute(INSERT_DATA_SQL)
    conn.commit()
    cursor.close()
