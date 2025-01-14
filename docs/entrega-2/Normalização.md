# <center>Entrega do Trabalho 2 - SQL</center>

## **Normalização**

**O que é Normalização?**

A normalização é um processo no design de bancos de dados relacionais que organiza os dados para minimizar redundâncias e evitar inconsistências. Ela envolve dividir tabelas maiores em tabelas menores e definir relacionamentos claros entre elas, seguindo regras (ou formas normais) específicas. O objetivo principal é garantir que o banco de dados seja eficiente, confiável e fácil de manter.

**Para que serve a Normalização?**

1.	Evitar redundância de dados: Armazenar informações repetidas em várias tabelas pode aumentar o tamanho do banco de dados e causar inconsistências quando os dados precisam ser atualizados.
2.	Garantir integridade dos dados: Ao organizar os dados corretamente, reduz-se o risco de erros ou duplicações que podem surgir durante a manipulação.
3.	Facilitar a manutenção: Bancos de dados normalizados são mais fáceis de modificar, uma vez que a estrutura é lógica e organizada.
4.	Melhorar o desempenho: Apesar de a normalização às vezes introduzir mais tabelas (o que pode impactar consultas complexas), ela reduz o tamanho total do banco e facilita operações como inserção, atualização e exclusão.

**Por que é importante?**

A normalização é crucial para manter a qualidade dos dados, garantindo que as informações armazenadas no banco de dados estejam consistentes e organizadas. Sem normalização, problemas como redundância, dificuldade de manutenção e integridade comprometida podem surgir, impactando diretamente o desempenho e a confiabilidade do sistema.


***As Formas Normais***

*1ª Forma Normal (1FN):*

Critérios:

1. Todos os campos devem conter apenas valores atômicos (não divisíveis).

2. Cada linha deve ser única, ou seja, deve possuir uma chave primária.

Objetivo:

Eliminar grupos repetidos e estruturar os dados em tabelas onde cada célula contém um único valor.

***2ª Forma Normal (2FN):***

Critérios:

1. A tabela deve estar na 1FN.
2. Todos os atributos não-chave devem depender totalmente da chave primária (dependência funcional completa).

Objetivo:

Eliminar dependências parciais, onde um atributo depende de apenas parte da chave primária em tabelas com chaves compostas.

***3ª Forma Normal (3FN):***

Critérios:

1. A tabela deve estar na 2FN.
2. Todos os atributos não-chave devem depender diretamente da chave primária e não de outros atributos não-chave (eliminação de dependências transitivas).

Objetivo:

Remover atributos que são indiretamente dependentes da chave primária.

***Forma Normal de Boyce-Codd (FNBC):***

Critérios:

1. A tabela deve estar na 3FN.
2. Cada determinante (atributo que define outro atributo) deve ser uma chave candidata.

Objetivo:

Resolver anomalias que podem ocorrer mesmo quando a tabela está na 3FN, eliminando dependências funcionais que não sejam atribuídas a chaves candidatas

***4ª Forma Normal (4FN):***

Critérios:

1. A tabela deve estar na 3FN.
2. Deve eliminar dependências multivaloradas, ou seja, quando um atributo pode estar relacionado a múltiplos valores de outro atributo independentemente.

Objetivo:

Resolver problemas em que várias relações independentes são representadas na mesma tabela.

## Tabelas normalizadas:

Legenda:
#

*Tabela normalizada*

*Tabela original*

*Explicação*

#

## Personagem 

Personagem ( id_personagem, tipo)

<s>Personagem ( id_personagem, tipo)</s>

A tabela Personagem já estava na 4FN.

## PC 

PC ( id_personagem, nome,id_celula, id_faccao, id_classe, descricao, dano, hp, hp_atual, level, energia, xp, id_inventario)

<s>PC ( id_personagem, id_celula, id_faccao, id_classe, id_inventario, descricao, dano, hp, hp_atual, nome, level, energia, xp)</s>

A tabela PC tinha atributos dependentes de atributos não chave primária ( do nome). Para normalizar foi tornado parte da PK, o atributo ‘nome’. Agora a tabela está na 4FN.

## NPC

NPC (id_personagem, tipo)

<s>NPC (id_personagem, tipo)</s>

A tabela NPC já estava na 4FN.

## Inimigo 

Inimigo (id_inimigo, id_personagem, id_celula, nome, hp, xp, dano)

<s>Inimigo (id_inimigo, id_personagem, id_celula, nome, descricao)</s>

A tabela Inimigo possuía atributos dependentes de atributos não chave primária ( do id_personagem). Para normalizar foi tornado parte da PK, o atributo ‘id_personagem’. Além disso, foram movidos para essa tabela os atributos xp, dano e hp devido serem atributos que todas as instâncias compartilham. O atributo ‘descricao’ foi removido por ser repetitivo para os inimigos. Agora a tabela está na 4FN.

## Instancia_Inimigo 

Instancia_Inimigo (id_instancia_inimigo, id_inimigo, id_celula, hp_atual, id_inventario)

<s>Instancia_Inimigo (id_instancia_inimigo, id_inimigo, id_celula, hp, hp_atual, xp, dano)</s>

A tabela Instancia_Inimigo está na 4FN. Porém, para melhor utilizar a instanciação, os atributos xp, dano e hp, devido a serem atributos que todas as instâncias compartilham, foram movidos para essa tabela.

## Comerciante 

Comerciante (id_comerciante, id_personagem, nome, id_celula, descricao)

<s>Comerciante (id_comerciante, id_personagem, id_celula, nome, descricao)</s>

A tabela Comerciante tinha atributos dependentes de atributos não chave primária ( do id_personagem). Para normalizar foi tornado parte da PK, o atributo ‘id_personagem’. Agora a tabela está na 4FN.

## Loja 

Loja (id_comerciante, id_instancia_item)

<s>Loja (id_loja, id_comerciante, id_instancia_item)</s>

Foi retirado a chave id_loja e agora a tabela representa relação entre comerciamente e uma instância de item. Agora a tabela está na 4FN.

##  Item 

Item (id_item, tipo)

<s>Item (id_item, tipo)</s>

A tabela Item já estava na 4FN.

##  Equipamento 

Equipamento (id_item, tipo)

<s>Equipamento (id_item, tipo)</s>

A tabela Equipamento já estava na 4FN.

## Armadura 

Armadura (id_item, nome, descricao, valor, hp_bonus, raridade)

<s>Armadura (id_item, id_celula, nome, descricao, valor, hp_bonus, raridade)</s>

A tabela Armadura tinha atributos dependentes de atributos não chave primária ( do nome). Para normalizar foi tornado parte da PK, o atributo ‘nome’. Além disso, foi removido o atributo id_celula, pois este já se encontra na tabela ‘Instancia Item’. Agora a tabela está na 4FN.

## Arma 

Arma (id_item, nome, descricao, valor, raridade, municao, dano)

<s>Arma (id_item, id_celúla, nome, descricao, valor, raridade, municao, dano)</s>

A tabela Arma tinha atributos dependentes de atributos não chave primária ( do nome). Para normalizar foi tornado parte da PK, o atributo ‘nome’. Além disso, foi removido o atributo id_celula, pois este já se encontra na tabela ‘Instancia Item’. Agora a tabela está na 4FN.

## Implante Cibernético

Implante Cibernético (id_item, nome, descricao, valor, raridade, custo_energia, dano)

<s>Implante Cibernético (id_item, id_celúla, nome, descricao, valor, raridade, custo_energia, dano)</s>

A tabela Implante Cibernético tinha atributos dependentes de atributos não chave primária ( do nome). Para normalizar foi tornado parte da PK, o atributo ‘nome’. Além disso, foi removido o atributo id_celula, pois este já se encontra na tabela ‘Instancia Item’. Agora a tabela está na 4FN.

## Instancia Item

Instancia Item (id_instancia_item, id_item, id_celula)

<s>Instancia Item (id_instancia_item, id_inventario, id_item)</s>

A tabela Instancia Item estava na 4FN, porem ela tinha um atributo desnecessário ( id_inventario) e não possuía outro que era necessário ( id_celula).

## Interação 

Interação (id_interacao, id_personagem, id_dialogo)

<s>Interação (id_interacao, id_personagem, id_dialogo)</s>

A tabela Interação já estava na 4FN.

## Distrito 

Distrito (id_distrito, nome, descricao, range_maximo, quantidade_personagens)

<s>Distrito (id_distrito, nome, descricao, range_maximo, quantidade_personagens)</s>

A tabela Distrito já estava na 4FN.

## Inventário

Inventário (id_inventario, quantidade_itens, capacidade_maxima)

<s>Inventário (id_inventario, quantidade_itens, capacidade_maxima)</s>

A tabela Inventário já estava na 4FN.

## Inventario_tem_item 

Inventario_tem_item (id_inventario,id_instancia_item)

Foi criada uma tabela para representar um inventário ter uma instância de item. A tabela está na 4FN.

## Célula 

Célula (id_celula,nome ,id_distrito, descricao, destino)

<s>Célula (id_celula, id_distrito, nome, descricao, destino)</s>

A tabela Célula tinha atributos dependentes de atributos não chave primária ( do nome). Para normalizar foi tornado parte da PK, o atributo ‘nome’. Agora a tabela está na 4FN.

## Classes 

Classes (id_classe, tipo, enegia_bonus, hp_bonus, descricao, dano_bonus)

<s>Classes (id_classe, tipo)</s>

A tabela Classes está na 4FN. Porém, para melhor utilizar a especialização, os atributos tipo, enegia_bonus, hp_bonus, descricao e dano_bonus, devido a serem atributos que todas as especializações compartilham, foram movidos para essa tabela.

## Hacker 

Hacker (id_classe, especialidade)

<s>Hacker (id_classe, enegia_bonus, hp_bonus, descricao, dano_bonus)</s>

## Daiymo 

Daiymo (id_classe, especialidade)

<s>Daiymo (id_classe, enegia_bonus, hp_bonus, descricao, dano_bonus)</s>

## Scoundrel 

Scoundrel (id_classe, especialidade)

<s>Scoundrel (id_classe, enegia_bonus, hp_bonus, descricao, dano_bonus)</s>

## Facção 

Facção (id_faccao, nome, descricao, ideologia)

<s>Facção (id_faccao)</s>

A tabela Facção era irrelevante e utilizava especialização sem motivo, por isso as especializações foram removidas.

## Yazuka 

Yazuka (id_faccao, nome, descricao, ideologia)

As especializações de Facção foram removidas.

## TRIAD 

TRIAD (id_faccao, nome, descricao, ideologia)

As especializações de Facção foram removidas.

## Diálogo 

Diálogo (id_interação, mensagem_atual, responsavel_mensagem)

<s>Diálogo (id_interação, mensagem_atual, responsavel_mensagem)</s>

A tabela Diálogo já estava na 4FN

## Missão 

Missão (id_Missão, nome, descricao, dificuldade, objetivo)

<s>Missão (id_Missão, nome, descricao, dificuldade, objetivo)</s>

A tabela Missão já estava na 4FN

<center>

## Histórico de Versão
| Versão | Data | Descrição | Autor(es) |
| :-: | :-: | :-: | :-: | 
| `1.0`  | 13/01/2025 | Primeira normalização | [Arthur Fonseca](https://github.com/arthrfonsecaa), [Mateus Santos](https://github.com/14luke08)|

</center>