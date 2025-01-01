# Databricks notebook source
# MAGIC %md
# MAGIC 1. Crie um banco de dados no DW do Spark chamado Vendas Varejo, e persista todas as tabelas neste banco de dados.
# MAGIC 2. Crie uma consulta que mostre de cada item vendido: Nome do Cliente, Data da Venda, Produto, Vendedor e Valor Total do item.

# COMMAND ----------

import os

Clientes = spark.read.parquet(f"file:{os.getcwd()}/download/Atividades/Clientes.parquet")
ItensVendas = spark.read.parquet(f"file:{os.getcwd()}/download/Atividades/ItensVendas.parquet")
Produtos = spark.read.parquet(f"file:{os.getcwd()}/download/Atividades/Produtos.parquet")
Vendas = spark.read.parquet(f"file:{os.getcwd()}/download/Atividades/Vendas.parquet")
Vendedore = spark.read.parquet(f"file:{os.getcwd()}/download/Atividades/Vendedores.parquet")

# COMMAND ----------

Clientes.createOrReplaceTempView("Clientes_view")
ItensVendas.createOrReplaceTempView("ItensVendas_view")
Produtos.createOrReplaceTempView("Produtos_view")
Vendas.createOrReplaceTempView("Vendas_view")
Vendedore.createOrReplaceTempView("Vendedores_view")

# COMMAND ----------

spark.sql("""select 
          cli.Cliente
          ,ven.Data
          ,pro.Produto
          ,fuc.Vendedor
          ,iten.ValorTotal 
          from Vendas_view as ven inner join Clientes_view as cli
          on ven.ClienteID = cli.ClienteID 
          inner join Vendedores_view as fuc
          on ven.VendedorID = fuc.VendedorID
          inner join ItensVendas_view as iten
          on ven.VendasID = iten.VendasID 
          inner join Produtos_view as pro
          on iten.ProdutoID = pro.ProdutoID 
          order by Data""").show()

# COMMAND ----------

# Adicionando o arquivo JAR ao contexto do Spark
spark.sparkContext.addFile("dbfs:/FileStore/mssql-jdbc-3.5.1.jar")

# Definindo a URL de conexão
url = "jdbc:sqlserver://172.17.0.2:1433;databaseName=teste;encrypt=true;trustServerCertificate=true;"

# Parâmetros de conexão
properties = {
  "user": "SA", 
  "password": "igor123456!",
  "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Lendo os dados da tabela do SQL Server
df = spark.read.jdbc(url=url, table="coluna_test", properties=properties)

# Exibindo o conteúdo
df.show()


# COMMAND ----------

# Listar os arquivos no DBFS para verificar se o JAR está no caminho correto
dbutils.fs.ls("dbfs:/FileStore/")
