from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL no Railway
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:JCYwAuppanAEKmxGGCajhaZgvMCQKvmX@postgres.railway.internal:5432/railway")
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do banco de dados para armazenar pedidos
class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_cliente = db.Column(db.String(255), nullable=False)
    produto = db.Column(db.String(255), nullable=False)
    data_entrega = db.Column(db.String(20), nullable=False)
    horario_entrega = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(50), default="Pendente")

# Criar tabelas no banco de dados
with app.app_context():
    db.create_all()

# Rota para receber os pedidos
@app.route("/api/pedido", methods=["POST"])
def receber_pedido():
    data = request.get_json()
    
    if not all(key in data for key in ("nome_cliente", "produto", "data_entrega", "horario_entrega")):
        return jsonify({"error": "Dados incompletos!"}), 400
    
    novo_pedido = Pedido(
        nome_cliente=data["nome_cliente"],
        produto=data["produto"],
        data_entrega=data["data_entrega"],
        horario_entrega=data["horario_entrega"]
    )
    
    db.session.add(novo_pedido)
    db.session.commit()
    
    return jsonify({"message": "Pedido recebido com sucesso!"}), 201

# Rota para listar pedidos
@app.route("/api/pedidos", methods=["GET"])
def listar_pedidos():
    pedidos = Pedido.query.all()
    pedidos_json = [{
        "id": pedido.id,
        "nome_cliente": pedido.nome_cliente,
        "produto": pedido.produto,
        "data_entrega": pedido.data_entrega,
        "horario_entrega": pedido.horario_entrega,
        "status": pedido.status
    } for pedido in pedidos]
    
    return jsonify(pedidos_json)

# Rodar a API
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)