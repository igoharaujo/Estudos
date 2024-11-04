from banco import *

class View(Conexao):

    def vw_produto(self):
        conexao = self.conecta_banco()
        if conexao is not None:
            conexao.execute('CREATE VIEW IF NOT EXISTS dados_produto AS SELECT * FROM produto')
            print('View Criada')

        else:
            print("Erro: Conexão com o banco de dados não foi estabelecida.")

view = View()
view.vw_produto()
fechar_conexao.close()