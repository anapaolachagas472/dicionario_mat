from flask import Flask, request, jsonify
from flask_mysql_connector import MySQL

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Altere se necessário
app.config['MYSQL_USER'] = 'seu_usuario'  # Substitua pelo usuário do MySQL
app.config['MYSQL_PASSWORD'] = 'sua_senha'  # Substitua pela senha do MySQL
app.config['MYSQL_DATABASE'] = 'dicionario'  # Nome do banco de dados

mysql = MySQL(app)

# Rota principal de teste
@app.route('/')
def index():
    return "API do Dicionário de Matemática está funcionando!"

# Rota para cadastrar um termo
@app.route('/termos', methods=['POST'])
def cadastrar_termo():
    dados = request.json
    termo = dados.get('termo')
    definicao = dados.get('definicao')

    if not termo or not definicao:
        return jsonify({"erro": "Termo e definição são obrigatórios"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO termos (termo, definicao) VALUES (%s, %s)", (termo, definicao))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensagem": "Termo cadastrado com sucesso!"}), 201

# Rota para listar todos os termos
@app.route('/termos', methods=['GET'])
def listar_termos():
    cursor = mysql.connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM termos")
    termos = cursor.fetchall()
    cursor.close()

    return jsonify(termos), 200

# Rota para atualizar um termo
@app.route('/termos/<int:id>', methods=['PUT'])
def atualizar_termo(id):
    dados = request.json
    novo_termo = dados.get('termo')
    nova_definicao = dados.get('definicao')

    if not novo_termo or not nova_definicao:
        return jsonify({"erro": "Termo e definição são obrigatórios"}), 400

    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE termos SET termo = %s, definicao = %s WHERE id = %s",
        (novo_termo, nova_definicao, id)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensagem": "Termo atualizado com sucesso!"}), 200

# Rota para deletar um termo
@app.route('/termos/<int:id>', methods=['DELETE'])
def deletar_termo(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM termos WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()

    return jsonify({"mensagem": "Termo deletado com sucesso!"}), 200

if __name__ == '__main__':
    app.run(debug=True)
