# Databricks notebook source
# MAGIC %md
# MAGIC # Filtros no Spark: `filter` vs. `where`
# MAGIC
# MAGIC Em **Apache Spark**, as operações de filtro ajudam a refinar os dados processados. Tanto o método `filter` quanto o `where` são usados para aplicar condições sobre `DataFrames` e `RDDs`. Eles são funcionalmente semelhantes, mas podem ter pequenas diferenças de usabilidade e impacto de desempenho, dependendo do contexto.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔹 `filter`
# MAGIC
# MAGIC O método `filter` é a opção mais comum para aplicar condições em Spark, suportando filtros tanto em `DataFrames` quanto em `RDDs`. A sintaxe é intuitiva e permite utilizar expressões Booleanas para filtrar linhas de dados:
# MAGIC
# MAGIC ```python
# MAGIC # Exemplo em Python com Spark DataFrame
# MAGIC from pyspark.sql import SparkSession
# MAGIC
# MAGIC # Inicializando Spark
# MAGIC spark = SparkSession.builder.appName("ExemploFilter").getOrCreate()
# MAGIC df = spark.read.csv("exemplo.csv", header=True)
# MAGIC
# MAGIC # Filtrando dados com o método filter
# MAGIC df_filtrado = df.filter(df['coluna'] > 100)
# MAGIC df_filtrado.show()
# MAGIC ```
# MAGIC ----------
# MAGIC
# MAGIC ## Comparação de Desempenho: `filter` vs. `where` no Spark
# MAGIC
# MAGIC Os métodos `filter` e `where` são usados para aplicar condições em Spark **DataFrames**. Embora ambos sejam praticamente idênticos em funcionalidade, entender como eles podem influenciar o desempenho é importante em grandes volumes de dados. Aqui está um resumo das principais diferenças e considerações de desempenho:
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### 🔹 Diferença entre `filter` e `where`
# MAGIC
# MAGIC - **Funcionalmente idênticos em DataFrames**: Ambos realizam a mesma tarefa. A diferença é que `filter` pode ser usado tanto em **DataFrames** quanto em **RDDs**, enquanto `where` é exclusivo de DataFrames.
# MAGIC - **Preferência por Legibilidade**: Muitos desenvolvedores escolhem `where` em DataFrames por questão de clareza, principalmente ao lidar com condições SQL-like.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### ⚙️ Desempenho em Spark
# MAGIC
# MAGIC Embora `filter` e `where` não apresentem diferenças de desempenho intrínsecas, boas práticas de uso podem melhorar a eficiência do processamento no Spark. Aqui estão algumas dicas:
# MAGIC
# MAGIC - **Predicate Pushdown**: O Spark tenta otimizar operações de filtro empurrando as condições para o sistema de armazenamento (como Parquet ou ORC). Isso reduz a quantidade de dados carregados, tornando a operação mais eficiente. Esse processo é chamado de "pushdown".
# MAGIC   
# MAGIC ```python
# MAGIC   # Exemplo de pushdown, filtrando antes de qualquer transformação
# MAGIC   df_filtrado = df.filter(df['coluna'] > 100)
# MAGIC ```
# MAGIC

# COMMAND ----------

from pyspark.sql import functions as Func
import os

arqschema = "id INT, nome STRING, status STRING, cidade STRING, vendas INT, data STRING"

desparchante = spark.read.format("csv") \
                          .option('header', 'False') \
                          .option('sep', ',') \
                          .option('interSchema', 'True') \
                          .schema(arqschema) \
                          .load(f"file:{os.getcwd()}/download/despachantes.csv")



# COMMAND ----------

# Vamos filtrar as vendas que são maior que vinte
desparchante.select("id", "nome", "vendas").where(Func.col("vendas") > 20).show()

# Vamos aplicar mais condição:
desparchante.select("id", "nome", "vendas").where((Func.col("vendas") > 20) 
                                                  & (Func.col("vendas") < 40)) \
                                                  .show()