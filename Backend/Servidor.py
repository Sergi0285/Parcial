from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la conexión a MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@172.31.80.194:3306/trabajo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definición del modelo
class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=True)
    apellido = db.Column(db.String(100), nullable=True)
    fechaNacimiento = db.Column(db.Date, nullable=True)
    password = db.Column(db.String(100), nullable=True)

# Endpoint para crear un nuevo usuario
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    nuevo_usuario = Usuario(
        nombre=data.get('nombre'),
        apellido=data.get('apellido'),
        fechaNacimiento=data.get('fechaNacimiento'),
        password=data.get('password')
    )
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente'}), 201

# Endpoint para obtener todos los usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    usuarios = Usuario.query.all()
    usuarios_list = [{'id': u.id, 'nombre': u.nombre, 'apellido': u.apellido, 'fechaNacimiento': u.fechaNacimiento, 'password': u.password} for u in usuarios]
    return jsonify(usuarios_list), 200

# Endpoint para obtener un usuario por ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def get_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'apellido': usuario.apellido, 'fechaNacimiento': usuario.fechaNacimiento, 'password': usuario.password}), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404

# Endpoint para actualizar un usuario
@app.route('/usuarios/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    usuario = Usuario.query.get(id)
    if usuario:
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.apellido = data.get('apellido', usuario.apellido)
        usuario.fechaNacimiento = data.get('fechaNacimiento', usuario.fechaNacimiento)
        usuario.password = data.get('password', usuario.password)
        db.session.commit()
        return jsonify({'message': 'Usuario actualizado exitosamente'}), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404

# Endpoint para borrar un usuario
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_usuario(id):
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'message': 'Usuario borrado exitosamente'}), 200
    return jsonify({'message': 'Usuario no encontrado'}), 404

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
