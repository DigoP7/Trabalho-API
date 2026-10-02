from config.database import conectar

class produto:
    
    @staticmethod
    def consultar_todos():
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos")
        resultado = [dict(row) for row in cursor.fetchall()]
        conexao.close()
        return resultado

    @staticmethod
    def consultar_por_id(id_produto):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id_produto,))
        row = cursor.fetchone()
        conexao.close()
        return dict(row) if row else None

    @staticmethod
    def cadastrar(dados):
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "INSERT INTO produtos (nome, categoria, preco, estoque, descricao) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(sql, (dados['nome'], dados['categoria'], dados['preco'], dados['estoque'], dados['descricao']))
        conexao.commit()
        novo_id = cursor.lastrowid
        conexao.close()
        return novo_id

    @staticmethod
    def atualizar(id_produto, dados):
        conexao = conectar()
        cursor = conexao.cursor()
        sql = "UPDATE produtos SET nome = ?, categoria = ?, preco = ?, estoque = ?, descricao = ? WHERE id = ?"
        cursor.execute(sql, (dados['nome'], dados['categoria'], dados['preco'], dados['estoque'], dados['descricao'], id_produto))
        conexao.commit()
        afetadas = cursor.rowcount
        conexao.close()
        return afetadas

    @staticmethod
    def excluir(id_produto):
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM produtos WHERE id = ?", (id_produto,))
        conexao.commit()
        afetadas = cursor.rowcount
        conexao.close()
        return afetadas