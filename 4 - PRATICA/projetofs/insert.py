from banco import *

class Insert(Conexao):

    def insert_produto(self,nome, qtd, valor, validade ):
        conexao = self.conecta_banco()
        if conexao is not None:
            conexao.execute('''INSERT INTO produto (nome, qtd, valor, validade)
                               VALUES (?, ?, ?, ?)''', (nome, qtd, valor, validade))
            conexao.connection.commit()
            print('Produto inserido com sucesso')

        else:
            print("Erro: Conexão com o banco de dados não foi estabelecida.")


# Criando uma instância da classe Insert
inserir = Insert()

# Inserindo um produto usando a instância
inserir.insert_produto('oculos de sol', 20, 50.20, '2024-08-06')
