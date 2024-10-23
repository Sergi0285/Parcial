from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError

# Inicializa la instancia de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuraciones para la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:contrasena12345#.@database-1.clw6drnudw9y.us-east-1.rds.amazonaws.com/sakila'
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

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/stores', methods=['GET'])
    def get_stores():
        """
        Obtiene una lista de todas las tiendas almacenadas en la base de datos.
        """
        try:
            stores = db.session.query(Store).all()
            return jsonify([{
                'store_id': s.store_id,
                'manager_staff_id': s.manager_staff_id,
                'address_id': s.address_id,
                'last_update': s.last_update.isoformat() if s.last_update else None
            } for s in stores])
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al acceder a la base de datos: " + error}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        """
        Comprueba si la conexión a la base de datos es exitosa.
        """
        try:
            db.session.execute('SELECT 1')
            return jsonify({"message": "Conexión a la base de datos exitosa!"}), 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al conectar a la base de datos: " + error}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
