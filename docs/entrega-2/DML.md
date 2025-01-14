# <center>Entrega do Trabalho 2 - SQL</center>

## **DML**

A DML (Data Manipulation Language), ao contrário da DDL, foca na manipulação e alteração dos dados dentro de um banco de dados. Ela permite que os usuários insiram, atualizem e excluam dados em tabelas de forma eficiente. A DML é composta por comandos que alteram o conteúdo dos dados armazenados, mas sem modificar a estrutura das tabelas ou do banco de dados em si.

### INSERT

```sql

BEGIN TRANSACTION;

INSERT INTO Personagem (id_personagem, tipo) VALUES 
(1, 'PC'),
(2, 'NPC'),
(3, 'NPC');

INSERT INTO PC (id_personagem, id_celula, id_faccao, id_classe, id_inventario, descricao, dano, hp, hp_atual, nome, level, energia, xp) VALUES
(1, 10, 20, 30, 40, 'Descrição 1', 50, 60, 0, 'Personagem 1', 80, 90, 100),
(2, 11, 21, 31, 41, 'Descrição 2', 51, 61, 25, 'Personagem 2', 81, 91, 1),
(3, 12, 22, 32, 42, 'Descrição 3', 52, 62, 50, 'Personagem 3', 82, 92, 2),
(4, 13, 23, 33, 43, 'Descrição 4', 53, 63, 75, 'Personagem 4', 83, 93, 3),
(5, 14, 24, 34, 44, 'Descrição 5', 54, 64, 100, 'Personagem 5', 84, 94, 4);

INSERT INTO NPC (id_personagem, tipo) VALUES 
(2, 'Comerciante'),
(3, 'Inimigo');

INSERT INTO Inimigo (id_inimigo, id_personagem, id_celula, nome) VALUES 
(1, 3, 10, 'Inimigo 1');

INSERT INTO InstanciaInimigo (id_instancia_inimigo, id_inimigo, id_celula, hp, hp_atual, xp, dano, dificuldade) VALUES 
(1, 1, 3, 50, 5, 10, 5, 'Normal');

INSERT INTO Comerciante (id_comerciante, id_personagem, id_celula, nome, descricao) VALUES 
(1, 2, 3, 'Comerciante 1', 'Descrição do comerciante 1');

INSERT INTO Loja (id_comerciante, id_instancia_item) VALUES 
(1, 1);

INSERT INTO Item (id_item, nome, descricao) VALUES 
(1, 'Item 1', 'Descricao 1'),
(2, 'Item 2', 'Descricao 2');

INSERT INTO Equipamento (id_item, tipo) VALUES 
(1, 'Arma'),
(2, 'Consumível');

INSERT INTO Armadura (id_item, id_celula, nome, descricao, valor, hp_bonus, raridade) VALUES 
(1, 1, 'Armadura Básica', 'Descrição da armadura básica', 100, 10, 'Comum'),
(2, 2, 'Armadura Avançada', 'Descrição da armadura avançada', 200, 20, 'Rara');

INSERT INTO Arma (id_item, id_celula, nome, descricao, valor, raridade, municao, dano) VALUES 
(1, 1, 'Espada de Ferro', 'Descrição da espada de ferro', 150, 'Comum', 0, 10),
(2, 2, 'Pistola', 'Descrição da pistola', 300, 'Rara', 15, 25);

INSERT INTO ImplanteCibernetico (id_item, id_celula, nome, descricao, valor, raridade, custo_energia, dano) VALUES 
(1, 1, 'Braço Cibernético', 'Descrição do braço cibernético', 500, 'Épico', 5, 15),
(2, 2, 'Olho Cibernético', 'Descrição do olho cibernético', 400, 'Raro', 3, 10);

INSERT INTO InstanciaItem (id_instancia_item, id_inventario, id_item) VALUES 
(1, 1, 1),
(2, 1, 2);

INSERT INTO Inventario (id_inventario, quantidade_itens, capacidade_maxima) VALUES
(1, 10, 20);

INSERT INTO Inventario_tem_item (id_inventario, id_instancia_item) VALUES
(1, 10, 20);

INSERT INTO Distrito (id_distrito, nome, descricao, range_maximo, quantidade_personagens) VALUES 
(1, 'Distrito 1', 'Descrição do distrito 1', 100, 10);

INSERT INTO Celula (id_celula, id_distrito, nome, descricao, destino) VALUES 
(1, 1, 'Célula 1', 'Descrição da célula 1', 'Destino 1'),
(2, 1, 'Célula 2', 'Descrição da célula 2', 'Destino 2');

INSERT INTO Classes (id_classe, tipo, enegia_bonus, hp_bonus, descricao, dano_bonus) VALUES 
(1, 'Scoundrel', 5, 5, 'Descrição da Classe Scoundrel', 5),
(1, 'Hacker', 5, 5, 'Descrição da Classe Hacker', 5),
(1, 'Daimyo', 5, 5, 'Descrição da Classe Daimyo', 5),

INSERT INTO Faccao (id_faccao, nome, descricao, ideologia) VALUES 
(1, 'Yazuka', 'Descrição da Yazuka', 'Ideologia Yazuka'),
(2, 'Triad', 'Descrição da Triad', 'Ideologia Triad');

INSERT INTO Habilidade (id_habilidade, nome, tipo_habilidade, descricao, custo_de_uso, dano, velocidade_movimento) VALUES 
(1, 'Ataque Rápido', 'Ofensiva', 'Ataque rápido e preciso', 5, 10, 2),
(2, 'Defesa Forte', 'Defensiva', 'Aumenta a defesa temporariamente', 8, 0, 0);

INSERT INTO Dialogo (id_interacao, mensagem_atual, responsavel_mensagem) VALUES 
(1, 'Olá, como posso ajudar?', 'Comerciante'),        
(2, 'Prepare-se para a batalha!', 'Inimigo');

INSERT INTO Interacao (id_interacao, id_personagem, id_dialogo) VALUES 
(1, 2, 1),
(2, 3, 2);

INSERT INTO Missao (id_missao, nome, descricao, dificuldade, objetivo) VALUES 
(1, 'Derrotar os Inimigos', 'Encontre e elimine os Inimigos.', 'Média', 'Elimine todos os Inimigos');

COMMIT;

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