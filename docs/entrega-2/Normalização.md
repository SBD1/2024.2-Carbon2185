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

#

### Tabela PC: 

### Tabela NPC:

### Tabela Personagem:

### Tabela Classes:

### Tabela Facção:

### Tabela Inimigo:

### Tabela Distrito:

### Tabela Célula:

### Tabela Inventário:

### Tabela Item:

### Tabela Instância item:

### Tabela Equipamento:

### Tabela Armadura:

### Tabela Arma:

### Tabela Implante Cibernético:

### Tabela Comerciante:

### Tabela Loja:

### Tabela Interação:

### Tabela Dialogo:

### Tabela Instancia inimigo:


