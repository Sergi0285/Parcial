from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa CORS

# Inicializa la instancia de SQLAlchemy, pero sin conectarla aún a la app
db = SQLAlchemy()

# Modelo de Usuario que representa la tabla en la base de datos
class Usuario(db.Model):
    """
    Modelo que representa un Usuario en la base de datos.

    Atributos:
        id (int): Identificador único del usuario.
        nombre (str): Nombre del usuario.
        apellido (str): Apellido del usuario.
        fechaNacimiento (str): Fecha de nacimiento del usuario.
        password (str): Contraseña del usuario.
    """
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    fechaNacimiento = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Crea la aplicación Flask y configura la base de datos
def create_app():
    """
    Crea y configura la aplicación Flask.

    Configura la conexión a la base de datos y las rutas necesarias para
    las operaciones CRUD sobre usuarios.

    Retorna:
        Flask: La aplicación configurada.
    """
    app = Flask(__name__)
    
    # Configuraciones para la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@172.31.80.194:3306/trabajo'  # Cambiar según configuración real
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa la base de datos con la aplicación
    db.init_app(app)

    # Configura CORS para permitir solicitudes desde cualquier origen
    CORS(app)

    # Ruta para crear un nuevo usuario
    @app.route('/usuarios', methods=['POST'])
    def create_usuario():
        """
        Crea un nuevo usuario a partir de los datos proporcionados en el cuerpo de la solicitud.

        Retorna:
            Response: Respuesta JSON con un mensaje de éxito y el código de estado 201.
        """
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

    # Ruta para obtener la lista de todos los usuarios
    @app.route('/usuarios', methods=['GET'])
    def get_usuarios():
        """
        Obtiene una lista de todos los usuarios almacenados en la base de datos.

        Retorna:
            Response: Respuesta JSON con la lista de usuarios.
        """
        usuarios = Usuario.query.all()
        return jsonify([{
            'id': u.id,
            'nombre': u.nombre,
            'apellido': u.apellido,
            'fechaNacimiento': u.fechaNacimiento,
            'password' : u.password
        } for u in usuarios])

    # Ruta para obtener un usuario específico por su ID
    @app.route('/usuarios/<int:id>', methods=['GET'])
    def get_usuario(id):
        """
        Obtiene los detalles de un usuario específico por su ID.

        Parámetros:
            id (int): ID del usuario a buscar.

        Retorna:
            Response: Respuesta JSON con los detalles del usuario.
        """
        usuario = Usuario.query.get_or_404(id)
        return jsonify({
            'id': usuario.id,
            'nombre': usuario.nombre,
            'apellido': usuario.apellido,
            'fechaNacimiento': usuario.fechaNacimiento
        })

    # Ruta para actualizar un usuario específico por su ID
    @app.route('/usuarios/<int:id>', methods=['PUT'])
    def update_usuario(id):
        """
        Actualiza los detalles de un usuario existente.

        Parámetros:
            id (int): ID del usuario a actualizar.

        Retorna:
            Response: Respuesta JSON con un mensaje de éxito.
        """
        data = request.get_json()
        usuario = Usuario.query.get_or_404(id)
        usuario.nombre = data.get('nombre', usuario.nombre)
        usuario.apellido = data.get('apellido', usuario.apellido)
        usuario.fechaNacimiento = data.get('fechaNacimiento', usuario.fechaNacimiento)
        usuario.password = data.get('password', usuario.password)
        db.session.commit()
        return jsonify({"mensaje": "Usuario actualizado exitosamente"})

    # Ruta para eliminar un usuario por su ID
    @app.route('/usuarios/<int:id>', methods=['DELETE'])
    def delete_usuario(id):
        """
        Elimina un usuario específico por su ID.

        Parámetros:
            id (int): ID del usuario a eliminar.

        Retorna:
            Response: Respuesta vacía con código de estado 204.
        """
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204

    return app

def create_test_app():
    """
    Crea y configura una aplicación Flask para realizar pruebas unitarias.

    Configura una base de datos SQLite en memoria y prepara las rutas necesarias
    para las pruebas de operaciones CRUD sobre usuarios.

    Retorna:
        Flask: La aplicación configurada para pruebas.
    """
    app = Flask(__name__)
    
    # Configuraciones para pruebas (base de datos en memoria)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    # Inicializa la base de datos con la aplicación
    db.init_app(app)
    
    with app.app_context():
        db.create_all()  # Crea todas las tablas necesarias para las pruebas
    
    # Configura CORS
    CORS(app)
    
    # Rutas CRUD (similares a las anteriores)
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
            'fechaNacimiento': u.fechaNacimiento,
            'password': u.password
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
