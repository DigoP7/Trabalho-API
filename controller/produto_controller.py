from flask import jsonify, request
from model.produto import produto

def registrar_rotas_produto(app):

    @app.route('/produtos', methods=['GET'])
    def listar_produtos():
        dados = produto.consultar_todos()
        return jsonify({
            "endpoint": "consultatudo",
            "total": len(dados),
            "dados": dados
        })

    @app.route('/produtos/<int:id>', methods=['GET'])
    def buscar_produto(id):
        dado = produto.consultar_por_id(id)
        if not dado:
            return jsonify({"erro": "Registro não encontrado."}), 404
        return jsonify({
            "endpoint": "consultarid",
            "dados": dado
        })

    @app.route('/produtos', methods=['POST'])
    def criar_produto():
        conteudo = request.json
        novo_id = produto.cadastrar(conteudo)
        return jsonify({
            "mensagem": "Cadastrado com sucesso!",
            "id": novo_id
        }), 201

    @app.route('/produtos/<int:id>', methods=['PUT'])
    def alterar_produto(id):
        conteudo = request.json
        afetados = produto.atualizar(id, conteudo)
        if afetados == 0:
            return jsonify({"erro": "Registro não encontrado para atualizar."}), 404
        return jsonify({"mensagem": "Atualizado com sucesso!"})

    @app.route('/produtos/<int:id>', methods=['DELETE'])
    def deletar_produto(id):
        afetados = produto.excluir(id)
        if afetados == 0:
            return jsonify({"erro": "Registro não encontrado para excluir."}), 404
        return jsonify({"mensagem": "Excluído com sucesso!"})