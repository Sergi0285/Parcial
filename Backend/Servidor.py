from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Inicializa la instancia de SQLAlchemy, pero sin conectarla aún a la app
db = SQLAlchemy()

# Define el modelo de Usuario
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    fechaNacimiento = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Crea la aplicación Flask y configura la base de datos
def create_app():
    app = Flask(__name__)
    
    # Configuraciones para base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@172.31.80.194:3306/trabajo'  # Cambia según tu configuración
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa la base de datos con la aplicación
    db.init_app(app)

    # Rutas CRUD para la entidad usuario
    @app.route('/usuarios', methods=['POST'])
    def create_usuario():
        data = request.get_json()
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            fechaNacimiento=data['fechaNacimiento'],
            password=data['password']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

    @app.route('/usuarios', methods=['GET'])
    def get_usuarios():
        usuarios = Usuario.query.all()
        return jsonify([{
            'id': u.id,
            'nombre': u.nombre,
            'apellido': u.apellido,
            'fechaNacimiento': u.fechaNacimiento
        } for u in usuarios])

    @app.route('/usuarios/<int:id>', methods=['GET'])
    def get_usuario(id):
        usuario = Usuario.query.get_or_404(id)
        return jsonify({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'fechaNacimiento': usuario.fechaNacimiento
        })

    @app.route('/usuarios/<int:id>', methods=['PUT'])
    def update_usuario(id):
        data = request.get_json()
        usuario = Usuario.query.get_or_404(id)
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.apellido = data.get('apellido', usuario.apellido)
        usuario.fechaNacimiento = data.get('fechaNacimiento', usuario.fechaNacimiento)
        usuario.password = data.get('password', usuario.password)
        db.session.commit()
        return jsonify({"mensaje": "Usuario actualizado exitosamente"})

    @app.route('/usuarios/<int:id>', methods=['DELETE'])
    def delete_usuario(id):
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

    return app

def create_test_app():
    app = Flask(__name__)
    
    # Configuraciones para pruebas
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    # Inicializa la base de datos con la aplicación
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Crea todas las tablas necesarias para las pruebas
    
    # Define las rutas necesarias para las pruebas
    @app.route('/usuarios', methods=['POST'])
    def create_usuario():
        data = request.get_json()
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            apellido=data['apellido'],
            fechaNacimiento=data['fechaNacimiento'],
            password=data['password']
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        return jsonify({"mensaje": "Usuario creado exitosamente"}), 201

    @app.route('/usuarios', methods=['GET'])
    def get_usuarios():
        usuarios = Usuario.query.all()
        return jsonify([{
            'id': u.id,
            'nombre': u.nombre,
            'apellido': u.apellido,
            'fechaNacimiento': u.fechaNacimiento
        } for u in usuarios])

    @app.route('/usuarios/<int:id>', methods=['GET'])
    def get_usuario(id):
        usuario = Usuario.query.get_or_404(id)
        return jsonify({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'fechaNacimiento': usuario.fechaNacimiento
        })

    @app.route('/usuarios/<int:id>', methods=['PUT'])
    def update_usuario(id):
        data = request.get_json()
        usuario = Usuario.query.get_or_404(id)
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.apellido = data.get('apellido', usuario.apellido)
        usuario.fechaNacimiento = data.get('fechaNacimiento', usuario.fechaNacimiento)
        usuario.password = data.get('password', usuario.password)
        db.session.commit()
        return jsonify({"mensaje": "Usuario actualizado exitosamente"})

    @app.route('/usuarios/<int:id>', methods=['DELETE'])
    def delete_usuario(id):
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
