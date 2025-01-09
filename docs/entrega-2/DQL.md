# <center>Entrega do Trabalho 2 - SQL</center>

## **DQL**

## **DQL**

A DQL (Data Query Language) é a parte do SQL que se concentra na consulta e recuperação de dados. Ela permite que os usuários solicitem e visualizem dados de tabelas e outros objetos no banco de dados. A DQL é fundamental porque a maior parte da interação com bancos de dados envolve a leitura e extração de informações para relatórios, análises e outros fins. O principal comando da DQL é o SELECT, que pode ser usado de várias maneiras para filtrar, ordenar e agrupar os dados.

```sql
-- 1. Consultar todos os personagens e seus tipos
SELECT 
    P.id_personagem, 
    P.tipo 
FROM 
    Personagem AS P;

-- 2. Listar PCs (personagens jogáveis) com atributos e informações detalhadas
SELECT 
    PC.id_personagem, 
    PC.nome, 
    PC.descricao, 
    PC.energia, 
    PC.dano, 
    PC.hp, 
    PC.hp_atual, 
    PC.nivel, 
    PC.xp 
FROM 
    PC;

-- 3. Listar NPCs associados a diálogos
SELECT 
    NPC.id_personagem AS id_npc, 
    NPC.tipo, 
    D.id_interacao, 
    D.mensagem_atual 
FROM 
    Interacao AS I
JOIN 
    NPC ON I.personagem_origem = NPC.id_personagem
JOIN 
    Dialogo AS D ON I.id_interacao = D.id_interacao;

-- 4. Obter comerciantes e suas localizações
SELECT 
    C.id_comerciante, 
    C.nome AS comerciante, 
    C.descricao, 
    CM.nome AS celula 
FROM 
    Comerciante AS C
LEFT JOIN 
    CelulaMundo AS CM ON C.id_celula = CM.id_celula;

-- 5. Consultar inimigos em células específicas
SELECT 
    I.id_inimigo, 
    I.nome, 
    I.descricao, 
    I.dano, 
    I.xp, 
    CM.nome AS celula 
FROM 
    Inimigo AS I
LEFT JOIN 
    CelulaMundo AS CM ON I.id_celula = CM.id_celula;

-- 6. Listar missões atribuídas a personagens
SELECT 
    P.id_personagem, 
    P.tipo AS tipo_personagem, 
    M.nome AS missao, 
    M.descricao AS descricao_missao 
FROM 
    Missao AS M
JOIN 
    Interacao AS I ON I.personagem_destino = M.id_missao
JOIN 
    Personagem AS P ON I.personagem_origem = P.id_personagem;

-- 7. Consultar o inventário de um personagem específico
SELECT 
    I.id_inventario, 
    II.id_instancia_item, 
    IT.tipo AS tipo_item, 
    CM.nome AS localizacao 
FROM 
    Inventario AS I
JOIN 
    InstanciaItem AS II ON I.id_inventario = II.id_inventario
JOIN 
    Item AS IT ON II.id_item = IT.id_item
LEFT JOIN 
    CelulaMundo AS CM ON II.id_celula = CM.id_celula;

-- 8. Listar personagens e suas facções
SELECT 
    PC.nome AS personagem, 
    F.nome AS faccao, 
    F.ideologia 
FROM 
    PC
JOIN 
    Faccao AS F ON PC.id_faccao = F.id_faccao;

-- 9. Exibir as lojas e itens disponíveis em cada loja
SELECT 
    L.id_loja, 
    C.nome AS comerciante, 
    II.id_instancia_item, 
    IT.tipo AS tipo_item 
FROM 
    Loja AS L
JOIN 
    Comerciante AS C ON L.id_comerciante = C.id_comerciante
JOIN 
    InstanciaItem AS II ON L.id_instancia_item = II.id_instancia_item
JOIN 
    Item AS IT ON II.id_item = IT.id_item;

-- 10. Consultar relacionamentos entre PCs e instâncias de inimigos
SELECT 
    PC.id_personagem AS id_pc, 
    PC.nome AS nome_pc, 
    II.id_instancia_inimigo, 
    I.nome AS nome_inimigo, 
    CM.nome AS celula 
FROM 
    InstanciaInimigo AS II
JOIN 
    Inimigo AS I ON II.id_inimigo = I.id_inimigo
JOIN 
    CelulaMundo AS CM ON II.id_celula = CM.id_celula
JOIN 
    PC ON PC.id_celula = CM.id_celula;
