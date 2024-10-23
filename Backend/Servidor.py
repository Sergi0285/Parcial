from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Importa CORS

# Inicializa la instancia de SQLAlchemy, pero sin conectarla aún a la app
db = SQLAlchemy()

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
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:contrasena12345#.@database-1.clw6drnudw9y.us-east-1.rds.amazonaws.com/sakila'  # Cambiar según configuración real
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializa la base de datos con la aplicación
    db.init_app(app)
# Refleja la base de datos existente
    with app.app_context():
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        Store = Base.classes.store  # Obtiene la clase Store de la base de datos reflejada

    # Configura CORS
    CORS(app)

    @app.route('/stores', methods=['GET'])
    def get_stores():
        """
        Obtiene una lista de todas las tiendas almacenadas en la base de datos.
    
        Retorna:
            Response: Respuesta JSON con la lista de tiendas.
        """
        stores = db.session.query(Store).all()
        return jsonify([{
            'store_id': s.store_id,
            'manager_staff_id': s.manager_staff_id,
            'address_id': s.address_id,
            'last_update': s.last_update.isoformat() if s.last_update else None
        } for s in stores])
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
