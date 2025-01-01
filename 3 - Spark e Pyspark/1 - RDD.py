# Databricks notebook source
# MAGIC %md
# MAGIC ## O que é um RDD?
# MAGIC
# MAGIC O **RDD** (Resilient Distributed Dataset) é a estrutura de dados fundamental do **Apache Spark**, projetada para armazenar dados de forma distribuída e resiliente em clusters. Ele é essencial para o processamento de grandes volumes de dados e oferece as seguintes vantagens:
# MAGIC
# MAGIC - **Distribuição**: Dados são automaticamente divididos e distribuídos entre os nós de um cluster, aproveitando o processamento paralelo.
# MAGIC - **Resiliência**: Se algum nó falha, o Spark consegue reconstruir os dados perdidos usando o *lineage* (histórico de operações aplicadas ao RDD).
# MAGIC
# MAGIC ### Principais Características do RDD
# MAGIC
# MAGIC 1. **Imutabilidade**: Depois de criado, um RDD não pode ser alterado; qualquer modificação gera um novo RDD.
# MAGIC 2. **Lazy Evaluation**: Operações aplicadas ao RDD são avaliadas apenas quando uma *action* (como `.collect()` ou `.count()`) é executada, o que otimiza o processamento.
# MAGIC 3. **Transformações e Ações**: Existem dois tipos principais de operações:
# MAGIC    - **Transformações** (ex.: `map`, `filter`): Criam novos RDDs a partir de operações aplicadas ao original.
# MAGIC    - **Ações** (ex.: `collect`, `count`): Executam as operações e retornam resultados.
# MAGIC
# MAGIC ### Exemplo de Uso
# MAGIC
# MAGIC ```python
# MAGIC # Cria um RDD a partir de uma lista de números
# MAGIC numeros = sc.parallelize([1, 2, 3, 4, 5])
# MAGIC
# MAGIC # Aplica uma transformação (map) e uma ação (collect) ao RDD
# MAGIC quadrados = numeros.map(lambda x: x ** 2)  # Transformação
# MAGIC print(quadrados.collect())  # Ação
# MAGIC

# COMMAND ----------

numeros = sc.parallelize([1,2,3,4,5,6,7,8,9,10])
numeros2 = sc.parallelize([6, 7, 8, 9, 10])

# COMMAND ----------

print('todos os elementos', numeros.collect())  # Retorna todos os elementos
print('primeiros 5 elementos', numeros.take(5))  # Retorna os 5 primeiros elementos
print('5 maiores elementos', numeros.top(5))  # Retorna os 5 maiores elementos
print('quantidade de elementos', numeros.count())  # Retorna a quantidade de elementos
print('soma de todos os elementos', numeros.sum())  # Retorna a soma de todos os elementos
print('média dos elementos', numeros.mean())  # Retorna a média de todos os elementos
print('maior elemento', numeros.max())  # Retorna o maior elemento
print('menor elemento', numeros.min())  # Retorna o menor elemento


# COMMAND ----------

# -> Filtro para os maiores que 2
filtro = numeros.filter(lambda filtro: filtro > 2 )
print(filtro.collect())

# -> Aplicando multiplicação por dois em toda lista
mapa = numeros.map(lambda mapa: mapa * 2)
print(mapa.collect())

# -> União das duas listas
uniao = numeros.union(numeros2)
print(uniao.collect())

print('-----------------------------------')

# -> Elementos em comuns
interseccao = numeros.intersection(numeros2)
print(interseccao.collect()) 

# -> A diferença, oq não está no outro
subtrai = numeros.subtract(numeros2)
print(subtrai.collect())

# -> Cartesiano 
cartesiano = numeros.cartesian(numeros2)
print(cartesiano.collect())

# COMMAND ----------

# MAGIC %md
# MAGIC Cenário 2

# COMMAND ----------

# -> Temos clientes e valores. (id, valor)
compras = sc.parallelize([(1,200),(2, 300),(3,120),(4,250),(5,78)])

# COMMAND ----------

# Chamando os ids:
print(compras.keys().collect())

# Chamando os valores:
print(compras.values().collect())

# Contando
print(compras.countByKey())
