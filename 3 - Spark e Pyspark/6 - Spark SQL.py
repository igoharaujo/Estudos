# Databricks notebook source
# MAGIC %md
# MAGIC # Spark SQL
# MAGIC
# MAGIC O Spark SQL é um módulo do Apache Spark que permite realizar consultas SQL diretamente em `DataFrames` ou `RDDs`. Ele facilita a análise de dados, permitindo o uso de comandos SQL junto com operações PySpark e suporta vários formatos de dados, como Parquet, JSON e CSV.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Principais Recursos do Spark SQL
# MAGIC
# MAGIC - **Consultas SQL**: Permite comandos como `SELECT`, `JOIN`, `GROUP BY` e `ORDER BY` diretamente em `DataFrames` e tabelas.
# MAGIC - **Integração com DataFrames**: `DataFrames` podem ser registrados como tabelas temporárias e consultados usando SQL.
# MAGIC - **Suporte a Vários Formatos de Dados**: Suporta dados em Parquet, JSON, CSV, ORC e outros.
# MAGIC - **Integração com BI e Ferramentas Analíticas**: Compatível com ferramentas de BI via JDBC/ODBC, como Tableau.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Exemplos Básicos
# MAGIC
# MAGIC 1. **Criação de Tabelas Temporárias**
# MAGIC ```python
# MAGIC    df.createOrReplaceTempView("minha_tabela")
# MAGIC ```
# MAGIC

# COMMAND ----------

from pyspark.sql.types import *
import os
arqschema = "id INT, nome STRING, status STRING, cidade STRING, vendas INT, data STRING"
df = spark.read.format('csv')\
                .option('header', 'False') \
                .option('interSchema', 'True')\
                .option('sep', ',') \
                .schema(arqschema)\
                .load(f"file:{os.getcwd()}/download/despachantes.csv")

# COMMAND ----------

# Para vermos os bancos de dados
spark.sql("show databases").show()

# Criando banco de dados
spark.sql("CREATE DATABASE IF NOT EXISTS desp")

# Vamos usar o banco
spark.sql("use desp").show()

# Criar tabela despachantes
#df.createOrReplaceTempView("despachantes")
#spark.sql("CREATE TABLE IF NOT EXISTS Despachantes")

# Dropa a tabela
#park.sql("drop table Despachantes")

# Dessa forma tmb cria a tabela e ja salva os dados do csv na tabela
df.write.saveAsTable("Despachantes", mode='overwrite')

# COMMAND ----------

spark.sql("SELECT * from despachantes").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## Tabelas Gerenciadas e externas

# COMMAND ----------

# MAGIC %md
# MAGIC # Diferença entre Tabela Gerenciada e Tabela Externa no Spark
# MAGIC
# MAGIC No Spark, ao criar tabelas no metastore, temos duas opções principais: **tabelas gerenciadas** e **tabelas externas**. Cada tipo de tabela tem características e usos específicos.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Tabela Gerenciada
# MAGIC
# MAGIC - **Definição**: Em uma tabela gerenciada, o Spark controla tanto a **metadata** quanto os **dados físicos**.
# MAGIC - **Localização**: O Spark armazena os dados no diretório padrão do metastore (geralmente dentro da pasta do Spark ou do Hive).
# MAGIC - **Gerenciamento de Dados**: O Spark é responsável pela criação, gerenciamento e exclusão dos dados.
# MAGIC - **Exclusão**: Se você excluir uma tabela gerenciada (`DROP TABLE`), os dados e a metadata da tabela serão **removidos completamente**.
# MAGIC
# MAGIC ### Quando Usar?
# MAGIC Use tabelas gerenciadas quando você deseja que o Spark controle completamente os dados e não precisa compartilhar os dados diretamente com outros sistemas.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Tabela Externa
# MAGIC
# MAGIC - **Definição**: Em uma tabela externa, o Spark armazena a **metadata** da tabela, mas os **dados permanecem em uma localização externa** (ex.: HDFS, S3 ou um sistema de arquivos local).
# MAGIC - **Localização**: Os dados são armazenados em um diretório especificado pelo usuário.
# MAGIC - **Gerenciamento de Dados**: O usuário é responsável pelo gerenciamento do diretório de dados externo.
# MAGIC - **Exclusão**: Se você excluir uma tabela externa (`DROP TABLE`), **apenas a metadata é removida**. Os dados físicos permanecem intactos.
# MAGIC
# MAGIC ### Quando Usar?
# MAGIC Use tabelas externas quando os dados são compartilhados entre diferentes sistemas ou quando você precisa armazenar dados em uma localização externa específica.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Resumo
# MAGIC
# MAGIC | Característica            | Tabela Gerenciada               | Tabela Externa                  |
# MAGIC |---------------------------|----------------------------------|---------------------------------|
# MAGIC | Controle de Dados         | Spark                           | Usuário                         |
# MAGIC | Localização dos Dados     | Diretório padrão do metastore   | Diretório especificado pelo usuário |
# MAGIC | Exclusão (`DROP TABLE`)   | Remove dados e metadata         | Remove apenas metadata          |
# MAGIC | Caso de Uso               | Dados exclusivos do Spark       | Dados compartilhados com outros sistemas |
# MAGIC
# MAGIC Em resumo, **tabelas gerenciadas** são mais simples para uso exclusivo do Spark, enquanto **tabelas externas** são ideais para dados que precisam ser acessados ou gerenciados por diferentes sistemas.
# MAGIC

# COMMAND ----------

# - > Cod para ver se a tabela é gerenciada

spark.sql("show create table despachantes").show(truncate=False)

# Se aparecer o metadado, a estrutura a tabela é gerenciada
# Se aparecer o local do arquivo, a tabela não é gerenciada

# COMMAND ----------

# MAGIC %md
# MAGIC ## Diferença entre View Temporária e View Temporária Global no Spark
# MAGIC
# MAGIC No Spark, podemos criar **views** para facilitar o acesso e manipulação dos dados em `DataFrames` usando comandos SQL. As views podem ser **temporárias** ou **temporárias globais**, e cada tipo tem características e usos específicos.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ### View Temporária
# MAGIC
# MAGIC - **Definição**: Uma view temporária é uma visualização de dados em memória, associada à sessão Spark atual.
# MAGIC - **Escopo**: A view só está acessível dentro da sessão Spark onde foi criada. Assim que a sessão é encerrada, a view é descartada.
# MAGIC - **Uso**: Ideal para operações temporárias ou para simplificar o código dentro de uma mesma sessão.
# MAGIC
# MAGIC ### View Temporária Global
# MAGIC
# MAGIC A **View Temporária Global** no Spark é uma visualização de dados em memória que permite o acesso aos dados de um `DataFrame` entre diferentes sessões Spark no mesmo cluster. É útil para cenários em que múltiplos usuários ou notebooks precisam consultar os mesmos dados de forma colaborativa, sem precisar recriar a visualização em cada sessão.
# MAGIC
# MAGIC ---
# MAGIC
# MAGIC ## Características da View Temporária Global
# MAGIC
# MAGIC - **Escopo**: A View Temporária Global é acessível por **todas as sessões Spark** no cluster, diferentemente de uma view temporária regular, que só é acessível na sessão em que foi criada.
# MAGIC - **Persistência**: A view permanece ativa **enquanto a aplicação Spark estiver em execução**. Quando a aplicação é encerrada, a view global também é removida.
# MAGIC - **Namespace**: Para acessar a view em outras sessões, é necessário prefixar o nome com `global_temp`, que é o namespace reservado para views globais.
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# Criando view temporaria
# Em sql:
#spark.sql("create or replace temp view desp_view as select * from despachantes").show()
# Em spark:
df.createOrReplaceTempView("Despachantes_view")
spark.sql("select * from despachantes_view").show()

# COMMAND ----------

# Criando view Globla
# Em sql:
#spark.sql("create or replace global temp view desp_view2 as select * from despachantes").show()
df.createOrReplaceGlobalTempView("Despachantes_view1")

spark.sql("select * from global_temp.despachantes_view1").show()


# COMMAND ----------

from pyspark.sql import functions as Func
from pyspark.sql.functions import *
import pyspark.pandas as ps


teste = ps.read_table("global_temp.despachantes_view1")

# COMMAND ----------

teste

# COMMAND ----------

# MAGIC %md
# MAGIC Joins