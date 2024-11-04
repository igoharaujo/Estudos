import sqlite3

import sqlite3


class Conexao:
    def __init__(self):
        self.con = sqlite3.connect("bdloja.db")
        self.cur = self.con.cursor()
        if self.con is not None:
            print("Conexao bem sucedida")

    def conecta_banco(self):
            return self.cur

class FechaConexao(Conexao):
    def close(self):
        if self.con is not None:
            self.con.close()
            print("CONEXÃO ENCERRADA")
        else:
            print("Erro: Conexão com o banco de dados não foi estabelecida.")


class Tabela:
    def __init__(self, conexao: Conexao):
        self.conexao = conexao

    def tb_produto(self):

        self.conexao.cur.execute('''CREATE TABLE if not exists produto(
                                id INTEGER PRIMARY KEY  autoincrement, 
                                nome VARCHAR(39), 
                                qtd INT, 
                                valor FLOAT,
                                validade DATE)''')
        self.conexao.con.commit()



abre_conexao = Conexao()
fechar_conexao = FechaConexao()

#abre_conexao.conecta_banco()
fechar_conexao.close()
