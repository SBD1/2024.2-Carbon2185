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
    (uuid_generate_v4(), NULL, 5, 20, 100, 'Andarilho Corrompido', 
    'Um ex-operário transformado em predador urbano após anos de exposição à poluição tóxica. Seus olhos brilham em vermelho sob a máscara de gás improvisada, e ele ataca qualquer um que invada seu território com lâminas enferrujadas.'),

    (uuid_generate_v4(), NULL, 5, 20, 100, 'Drone de Supressão', 
    'Criado para manter a ordem, esse drone flutua silenciosamente entre os becos iluminados do Distrito B. Ele dispara pulsos elétricos para neutralizar qualquer suspeito de insubordinação, registrando cada evento para os servidores centrais do Regime.'),

    (uuid_generate_v4(), NULL, 5, 10, 120, 'Carrasco das Favelas', 
    'Um brutamontes contratado por gangues locais para impor o terror entre os desesperados. Vestindo pedaços de armadura improvisada, ele empunha um enorme martelo hidráulico capaz de esmagar concreto e ossos com facilidade.'),

    (uuid_generate_v4(), NULL, 5, 10, 120, 'Mutante das Minas', 
    'Um mineiro que passou tempo demais exposto à radiação e aos gases tóxicos. Sua pele esverdeada e olhos sem pupilas denunciam a mutação avançada. Ele ataca com unhas endurecidas como lâminas, tentando arrancar o antídoto de qualquer intruso.'),

    (uuid_generate_v4(), NULL, 5, 5, 100, 'Saqueador Nômade', 
    'Vagando entre os distritos, o Saqueador Nômade sobrevive pilhando suprimentos e eliminando qualquer um que represente uma ameaça. Sua máscara remendada esconde um rosto cheio de cicatrizes, e suas lâminas afiadas refletem a luz neon dos becos escuros.'),

    (uuid_generate_v4(), NULL, 5, 5, 100, 'Caçador de Recompensas', 
    'Equipado com sensores térmicos e um arsenal de armas customizadas, o Caçador de Recompensas rastreia alvos para o regime e para os criminosos ricos. Ele não tem lealdade, apenas um preço. Se seu nome estiver em sua lista, prepare-se para fugir... ou lutar pela vida.')
ON CONFLICT (nome) DO NOTHING;

-- Missoes
INSERT INTO Missao (id_missao, nome, descricao, dificuldade, objetivo, goal, recompensa) VALUES
    (uuid_generate_v4(), 'Saque diário', 'Derrote alguns Saqueadores Nômade.', 1, 'Destruir 5 Saqueador Nômade', 5, 50),
    (uuid_generate_v4(), 'O Caçador se Torna a Presa', 'Derrote alguns Caçadores de Recompensas.', 1, 'Eliminar 5 Caçador de Recompensas', 5, 50),
    (uuid_generate_v4(), 'Expurgo Urbano', 'Elimine os Andarilhos Corrompidos que espreitam nos becos abandonados.', 3, 'Derrotar 30 Andarilhos Corrompidos', 30, 1000),
    (uuid_generate_v4(), 'Caçada Radioativa', 'Neutralize os Mutantes das Minas antes que se espalhem pela cidade.', 4, 'Eliminar 30 Mutantes das Minas', 30, 1200),
    (uuid_generate_v4(), 'O Regime não Dorme', 'Enfrente os Drones de Supressão e impeça a vigilância implacável.', 5, 'Destruir 30 Drones de Supressão', 30, 1100),
    (uuid_generate_v4(), 'Justiça nas Sombras', 'Acabe com a rede de violência imposta pelos Carrascos das Favelas.', 5, 'Eliminar 30 Carrascos das Favelas', 30, 1500),
    (uuid_generate_v4(), 'Terror Cibernético', 'Zero.exe, um hacker AI autoconsciente, está tomando o controle de sistemas de defesa.', 6, 'Derrotar Zero.exe', 1, 5000),
    (uuid_generate_v4(), 'Caçada ao Tyrant', 'Tyrant, um cyber-ogro modificado, lidera os Steel Fangs em massacres brutais.', 6, 'Derrotar Tyrant', 1, 5200),
    (uuid_generate_v4(), 'O Guardião do Labirinto', 'A megacorp Shinsei Biotech criou um super-soldado, Orion, para proteger seus segredos.', 7, 'Derrotar Orion', 1, 7000),
    (uuid_generate_v4(), 'Rei dos Bairros Baixos', 'Viper, um ex-executivo transformado em rei do crime, governa o submundo com punho de ferro.', 8, 'Derrotar Viper', 1, 100000)
ON CONFLICT (nome) DO NOTHING;

-- Itens Comuns (5)
INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'arma', 'Pistola de Choque', 'Pistola que dispara pulsos elétricos', 100, 'Comum'),
(uuid_generate_v4(), 'arma', 'Faca Serrilhada', 'Lâmina com fio molecular para cortes precisos', 100, 'Comum'),
(uuid_generate_v4(), 'arma', 'Revólver Magnético', 'Arma que dispara projéteis ferromagnéticos', 100, 'Comum'),
(uuid_generate_v4(), 'arma', 'Espingarda Térmica', 'Dispara cartuchos de calor concentrado', 100, 'Comum'),
(uuid_generate_v4(), 'arma', 'Submetralhadora de Plasma', 'Versão básica para combate urbano', 100, 'Comum')
ON CONFLICT (nome) DO NOTHING;

-- Itens Raros (3)
INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'arma', 'Lança-Chamas Criogênico', 'Congela alvos com jatos de -200°C', 200, 'Raro'),
(uuid_generate_v4(), 'arma', 'Fuzil de Precisão Quântica', 'Mira através de paredes usando partículas entrelaçadas', 200, 'Raro'),
(uuid_generate_v4(), 'arma', 'Espada de Fótons', 'Lâmina de energia corta ligas metálicas', 200, 'Raro')
ON CONFLICT (nome) DO NOTHING;

-- Itens Lendários (1)
INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'arma', 'Canhão de Singularidade', 'Cria micro buracos negros que distorcem a realidade', 300, 'Lendário'),
(uuid_generate_v4(), 'arma', 'Raio Desintegrador', 'Aniquila matéria a nível molecular', 300, 'Lendário')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Arma (id_item, id_celula, municao, dano)
SELECT id_item, NULL, 
    CASE raridade
        WHEN 'Lendário' THEN 15
        WHEN 'Raro' THEN 10
        ELSE 5
    END,
    CASE raridade
        WHEN 'Lendário' THEN 15
        WHEN 'Raro' THEN 10
        ELSE 5
    END
FROM Item 
WHERE tipo = 'arma'
AND NOT EXISTS (SELECT 1 FROM Arma WHERE Arma.id_item = Item.id_item);


-- Armaduras Corrigidas
INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'armadura', 'Colete Nanotecnológico', 'Fibras autoregenerativas', 100, 'Comum'),
(uuid_generate_v4(), 'armadura', 'Capacete de Sensor Térmico', 'Detecta assinaturas de calor', 100, 'Comum'),
(uuid_generate_v4(), 'armadura', 'Grevas de Carbono', 'Proteção leve para pernas', 100, 'Comum'),
(uuid_generate_v4(), 'armadura', 'Manto de Camuflagem', 'Distorção visual básica', 100, 'Comum'),
(uuid_generate_v4(), 'armadura', 'Placas de Cerâmica', 'Blindagem anti-projéteis', 100, 'Comum')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'armadura', 'Exoesqueleto Hidráulico', 'Amplifica força em 300%', 200, 'Raro'),
(uuid_generate_v4(), 'armadura', 'Escudo de Energia', 'Campo de força portátil', 200, 'Raro'),
(uuid_generate_v4(), 'armadura', 'Traje de Absorção', 'Converte dano em energia', 200, 'Raro')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'armadura', 'Armadura de Nanobots', 'Líquido metálico adaptativo', 300, 'Lendário'),
(uuid_generate_v4(), 'armadura', 'Manto de Invisibilidade', 'Dobra a luz ao redor do usuário', 300, 'Lendário')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Armadura (id_item, id_celula, hp_bonus)
SELECT id_item, NULL, 
    CASE raridade
        WHEN 'Lendário' THEN 15
        WHEN 'Raro' THEN 10
        ELSE 5
    END
FROM Item 
WHERE tipo = 'armadura'
AND NOT EXISTS (SELECT 1 FROM Armadura WHERE Armadura.id_item = Item.id_item);

-- Implantes Corrigidos
INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'implantecibernetico', 'Olos Biônicos', 'Visão noturna e zoom 5x', 100, 'Comum'),
(uuid_generate_v4(), 'implantecibernetico', 'Pulmões de Filtro', 'Filtra toxinas do ar', 100, 'Comum'),
(uuid_generate_v4(), 'implantecibernetico', 'Membros de Titânio', 'Próteses básicas para força aumentada', 100, 'Comum'),
(uuid_generate_v4(), 'implantecibernetico', 'Interface Neural', 'Controle dispositivos com a mente', 100, 'Comum'),
(uuid_generate_v4(), 'implantecibernetico', 'Dermaplacas', 'Pele reforçada com ligas metálicas', 100, 'Comum')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'implantecibernetico', 'Garras Retráteis', 'Lâminas de adamantium embutidas', 200, 'Raro'),
(uuid_generate_v4(), 'implantecibernetico', 'Sistema de Adrenalina', 'Extrai o melhor do soldado', 200, 'Raro'),
(uuid_generate_v4(), 'implantecibernetico', 'Glândula de Toxinas', 'Produz venenos orgânicos letais', 200, 'Raro')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Item (id_item, tipo, nome, descricao, valor, raridade) VALUES 
(uuid_generate_v4(), 'implantecibernetico', 'Chip de IA', 'Consciência artificial auxiliar', 300, 'Lendário'),
(uuid_generate_v4(), 'implantecibernetico', 'Núcleo de Antimatéria', 'Capacidade de utilizar energia para atacar os inimigos', 300, 'Lendário')
ON CONFLICT (nome) DO NOTHING;

INSERT INTO ImplanteCibernetico (id_item, id_celula, custo_energia, dano)
SELECT id_item, NULL, 
    CASE raridade
        WHEN 'Lendário' THEN 10
        WHEN 'Raro' THEN 5
        ELSE 2
    END,
    CASE raridade
        WHEN 'Lendário' THEN 15
        WHEN 'Raro' THEN 10
        ELSE 5
    END
FROM Item 
WHERE tipo = 'implantecibernetico'
AND NOT EXISTS (SELECT 1 FROM ImplanteCibernetico WHERE ImplanteCibernetico.id_item = Item.id_item);

-- Instanciar inimigos em células específicas
INSERT INTO InstanciaInimigo (id_instancia_inimigo, id_inimigo, id_celula, hp_atual)
SELECT uuid_generate_v4(), i.id_inimigo, cm.id_celula, i.hp
FROM Inimigo i
CROSS JOIN CelulaMundo cm
WHERE cm.nome IN (
    'Núcleo Enferrujado', 'Torre Fantasma', 'Terminal Esquecido', 'O Abatedouro',
    'Câmara Central', 'Plataforma Zero', 'Planalto das Máquinas',
    'Mercado Sombrio', 'Torre Quebrada', 'Cratera 13',
    'Minas Negras', 'Cemitério de Aço', 'Aurora Envenenada'
)
ORDER BY random()
LIMIT 50
ON CONFLICT DO NOTHING;

"""
def dml(conn):
    cursor = conn.cursor()
    cursor.execute(INSERT_DATA_SQL)
    conn.commit()
    cursor.close()
