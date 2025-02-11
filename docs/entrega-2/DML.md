# <center>Entrega do Trabalho 2 - SQL</center>

## **DML**

A DML (Data Manipulation Language), ao contrário da DDL, foca na manipulação e alteração dos dados dentro de um banco de dados. Ela permite que os usuários insiram, atualizem e excluam dados em tabelas de forma eficiente. A DML é composta por comandos que alteram o conteúdo dos dados armazenados, mas sem modificar a estrutura das tabelas ou do banco de dados em si.

### INSERT

```sql

BEGIN TRANSACTION;

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
SELECT uuid_generate_v4(), 'arma', 'Glock', 'Uma pistola básica', 100, 'Comum'
WHERE NOT EXISTS (SELECT 1 FROM Item WHERE nome = 'Glock');

INSERT INTO Arma (id_item, id_celula, municao, dano)
SELECT id_item, NULL, 5, 5 
FROM Item WHERE nome = 'Glock'
AND NOT EXISTS (SELECT 1 FROM Arma WHERE id_item = (SELECT id_item FROM Item WHERE nome = 'Glock'));

INSERT INTO Inimigo (id_inimigo, id_personagem, dano, xp, hp, nome, descricao)
VALUES
    (uuid_generate_v4(), NULL, 5, 10, 100, 'Andarilho Corrompido', 
    'Um ex-operário transformado em predador urbano após anos de exposição à poluição tóxica. Seus olhos brilham em vermelho sob a máscara de gás improvisada, e ele ataca qualquer um que invada seu território com lâminas enferrujadas.'),

    (uuid_generate_v4(), NULL, 5, 10, 100, 'Drone de Supressão', 
    'Criado para manter a ordem, esse drone flutua silenciosamente entre os becos iluminados do Distrito B. Ele dispara pulsos elétricos para neutralizar qualquer suspeito de insubordinação, registrando cada evento para os servidores centrais do Regime.'),

    (uuid_generate_v4(), NULL, 5, 10, 120, 'Carrasco das Favelas', 
    'Um brutamontes contratado por gangues locais para impor o terror entre os desesperados. Vestindo pedaços de armadura improvisada, ele empunha um enorme martelo hidráulico capaz de esmagar concreto e ossos com facilidade.'),

    (uuid_generate_v4(), NULL, 5, 10, 120, 'Mutante das Minas', 
    'Um mineiro que passou tempo demais exposto à radiação e aos gases tóxicos. Sua pele esverdeada e olhos sem pupilas denunciam a mutação avançada. Ele ataca com unhas endurecidas como lâminas, tentando arrancar o antídoto de qualquer intruso.'),

    (uuid_generate_v4(), NULL, 5, 10, 100, 'Saqueador Nômade', 
    'Vagando entre os distritos, o Saqueador Nômade sobrevive pilhando suprimentos e eliminando qualquer um que represente uma ameaça. Sua máscara remendada esconde um rosto cheio de cicatrizes, e suas lâminas afiadas refletem a luz neon dos becos escuros.'),

    (uuid_generate_v4(), NULL, 5, 10, 100, 'Caçador de Recompensas', 
    'Equipado com sensores térmicos e um arsenal de armas customizadas, o Caçador de Recompensas rastreia alvos para o regime e para os criminosos ricos. Ele não tem lealdade, apenas um preço. Se seu nome estiver em sua lista, prepare-se para fugir... ou lutar pela vida.')
    
ON CONFLICT (nome) DO NOTHING;

INSERT INTO Inimigo (id_inimigo, id_personagem, dano, xp, hp, nome, descricao)
VALUES
    (uuid_generate_v4(), NULL, 20, 100, 400, 'Zero.exe', 'Um hacker AI autoconsciente, está tomando o controle de sistemas de defesa.'),
    (uuid_generate_v4(), NULL, 20, 100, 400, 'Tyrant', 'Um cyber-ogro modificado, lidera os Steel Fangs em massacres brutais.'), 
    (uuid_generate_v4(), NULL, 20, 100, 400, 'Orion', 'A megacorp Shinsei Biotech criou um super-soldado para proteger seus segredos.'),
    (uuid_generate_v4(), NULL, 20, 100, 400, 'Viper', 'Um ex-executivo transformado em rei do crime, governa o submundo com punho de ferro.')

ON CONFLICT (nome) DO NOTHING;

-- Missoes
INSERT INTO Missao (id_missao, nome, descricao, dificuldade, objetivo, goal, recompensa) VALUES
    (uuid_generate_v4(), 'Saque diário', 'Derrote alguns Saqueadores Nômade.', 'Médio', 'Destruir 5 Saqueador Nômade', 5, 50),
    (uuid_generate_v4(), 'O Caçador se Torna a Presa', 'Derrote alguns Caçadores de Recompensas.', 'Médio', 'Eliminar 5 Caçador de Recompensas', 5, 50),
    (uuid_generate_v4(), 'Expurgo Urbano', 'Elimine os Andarilhos Corrompidos que espreitam nos becos abandonados.', 'Fácil', 'Derrotar 30 Andarilho Corrompido', 30, 1000),
    (uuid_generate_v4(), 'Caçada Radioativa', 'Neutralize os Mutantes das Minas antes que se espalhem pela cidade.', 'Fácil', 'Eliminar 30 Mutante das Minas', 30, 1200),
    (uuid_generate_v4(), 'O Regime não Dorme', 'Enfrente os Drones de Supressão e impeça a vigilância implacável.', 'Fácil', 'Destruir 30 Drone de Supressão', 30, 1100),
    (uuid_generate_v4(), 'Justiça nas Sombras', 'Acabe com a rede de violência imposta pelos Carrascos das Favelas.', 'Fácil', 'Eliminar 30 Carrasco das Favelas', 30, 1500),
    (uuid_generate_v4(), 'Terror Cibernético', 'Zero.exe, um hacker AI autoconsciente, está tomando o controle de sistemas de defesa.', 'Difícil', 'Derrotar Zero.exe', 1, 5000),
    (uuid_generate_v4(), 'Caçada ao Tyrant', 'Tyrant, um cyber-ogro modificado, lidera os Steel Fangs em massacres brutais.', 'Difícil', 'Derrotar Tyrant', 1, 5200),
    (uuid_generate_v4(), 'O Guardião do Labirinto', 'A megacorp Shinsei Biotech criou um super-soldado, Orion, para proteger seus segredos.', 'Difícil', 'Derrotar Orion', 1, 7000),
    (uuid_generate_v4(), 'Rei dos Bairros Baixos', 'Viper, um ex-executivo transformado em rei do crime, governa o submundo com punho de ferro.', 'Difícil', 'Derrotar Viper', 1, 100000)
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

```

### UPDATE

```sql

BEGIN TRANSACTION;

UPDATE PC
SET descricao = 'Nova Descrição', hp = 70
WHERE id_personagem = 2;

UPDATE NPC
SET tipo = 'Aliado'
WHERE id_personagem = 3;

UPDATE Comerciante
SET nome = 'Comerciante Atualizado', descricao = 'Nova Descrição do Comerciante'
WHERE id_comerciante = 2;

UPDATE Inimigo
SET dano = 15, xp = 20
WHERE id_inimigo = 2;

UPDATE Armadura
SET valor = 150, raridade = 'Rara'
WHERE id_item = 2;

UPDATE Arma
SET valor = 200, dano = 25
WHERE id_item = 2;

UPDATE Scoundrel
SET energia_bonus = 20, descricao = 'Nova Descrição do Scoundrel'
WHERE id_classe = 1;

UPDATE Faccao
SET nome = 'Nova Facção', ideologia = 'Nova Ideologia'
WHERE id_faccao = 2;

UPDATE Habilidade
SET custo_de_uso = 12, dano = 15
WHERE id_habilidade = 2;

UPDATE Dialogo
SET mensagem_atual = 'Mensagem Atualizada'
WHERE id_interacao = 2;

UPDATE Missao
SET objetivo = 'Novo Objetivo', dificuldade = 'Alta'
WHERE id_missao = 2;

COMMIT;

```

### DELETE

```sql

BEGIN TRANSACTION;

DELETE FROM Interacao WHERE id_personagem = 1;
DELETE FROM PC WHERE id_personagem = 1;
DELETE FROM NPC WHERE id_personagem = 1;
DELETE FROM Personagem WHERE id_personagem = 1;

DELETE FROM InstanciaItem WHERE id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = 1);
DELETE FROM Inventario WHERE id_inventario = (SELECT id_inventario FROM PC WHERE id_personagem = 1);
DELETE FROM PC WHERE id_personagem = 1;

DELETE FROM InstanciaInimigo WHERE id_inimigo = (SELECT id_personagem FROM NPC WHERE tipo = 'Inimigo' AND id_personagem = 1);
DELETE FROM Inimigo WHERE id_personagem = (SELECT id_personagem FROM NPC WHERE tipo = 'Inimigo' AND id_personagem = 1);
DELETE FROM Comerciante WHERE id_personagem = (SELECT id_personagem FROM NPC WHERE tipo = 'Comerciante' AND id_personagem = 1);
DELETE FROM NPC WHERE id_personagem = 1;

DELETE FROM InstanciaInimigo WHERE id_inimigo = 1;
DELETE FROM Inimigo WHERE id_inimigo = 1;

DELETE FROM Loja WHERE id_comerciante = 1;

DELETE FROM Comerciante WHERE id_comerciante = 1;

DELETE FROM InstanciaItem WHERE id_item = 1;
DELETE FROM Equipamento WHERE id_item = 1;
DELETE FROM Armadura WHERE id_item = 1;
DELETE FROM Arma WHERE id_item = 1;
DELETE FROM ImplanteCibernetico WHERE id_item = 1;
DELETE FROM Item WHERE id_item = 1;

DELETE FROM InstanciaItem WHERE id_inventario = 1;
DELETE FROM Inventario WHERE id_inventario = 1;

DELETE FROM Celula WHERE id_celula = 1;

DELETE FROM Classes WHERE id_classe = 1;

DELETE FROM Faccao WHERE id_faccao = 1 OR id_faccao = 2;

DELETE FROM Habilidade WHERE id_habilidade = 1;

DELETE FROM Dialogo WHERE id_interacao = 1;

DELETE FROM Interacao WHERE id_interacao = 1;

DELETE FROM Missao WHERE id_missao = 1;

COMMIT;

```

<center>

## Histórico de Versão
| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: | 
| `1.0`  | 13/01/2025 | Primeira versão do DML | [Arthur Fonseca](https://github.com/arthurfonsecaa), [Daniel Nunes](https://github.com/DanNunes777) |

</center>
