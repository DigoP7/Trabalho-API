from flask import Flask, jsonify
from flask_cors import CORS  # <-- 1. Importe o CORS
from flask_swagger_ui import get_swaggerui_blueprint
from controller.produto_controller import registrar_rotas_produto
from config.database import conectar

app = Flask(__name__)
CORS(app)
# Configuração do Swagger
SWAGGER_URL = '/projeto_api/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Produtos - Avaliação"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/static/swagger.json')
def swagger_json():
    return jsonify({
        "swagger": "2.0",
        "info": {
            "title": "API de Produtos",
            "description": "Documentação da API de Produtos em Flask seguindo MVC",
            "version": "1.0.0"
        },
        "host": "localhost:3000",
        "basePath": "/",
        "schemes": ["http"],
        "paths": {
            "/produtos": {
                "get": {
                    "summary": "Consultar todos os produtos",
                    "responses": {
                        "200": {
                            "description": "Lista de produtos retornada com sucesso"
                        }
                    }
                },
                "post": {
                    "summary": "Cadastrar um novo produto",
                    "parameters": [
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "nome": {"type": "string"},
                                    "categoria": {"type": "string"},
                                    "preco": {"type": "number"},
                                    "estoque": {"type": "integer"},
                                    "descricao": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "201": {
                            "description": "Produto cadastrado com sucesso"
                        }
                    }
                }
            },
            "/produtos/{id}": {
                "get": {
                    "summary": "Consultar produto por ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Produto encontrado"
                        },
                        "404": {
                            "description": "Não encontrado"
                        }
                    }
                },
                "put": {
                    "summary": "Atualizar um produto",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        },
                        {
                            "name": "body",
                            "in": "body",
                            "required": True,
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "nome": {"type": "string"},
                                    "categoria": {"type": "string"},
                                    "preco": {"type": "number"},
                                    "estoque": {"type": "integer"},
                                    "descricao": {"type": "string"}
                                }
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Atualizado com sucesso"
                        }
                    }
                },
                "delete": {
                    "summary": "Excluir um produto",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "type": "integer"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Excluído com sucesso"
                        }
                    }
                }
            }
        }
    })

def inicializar_banco():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            estoque INTEGER NOT NULL,
            descricao TEXT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conexao.commit()
    conexao.close()

inicializar_banco()
registrar_rotas_produto(app)

if __name__ == '__main__':
    app.run(debug=True, port=3000)