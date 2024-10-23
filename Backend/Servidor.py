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

    # Configura CORS para permitir solicitudes desde cualquier origen
    CORS(app)

    @app.route('/films', methods=['GET'])
    def get_films():
        """
        Obtiene una lista de todos los filmes almacenados en la base de datos.
    
        Retorna:
            Response: Respuesta JSON con la lista de filmes.
        """
        films = Film.query.all()
        return jsonify([{
            'film_id': f.film_id,
            'title': f.title,
            'description': f.description,
            'release_year': f.release_year,
            'language_id': f.language_id,
            'rental_duration': f.rental_duration,
            'rental_rate': str(f.rental_rate),  # Convertir a string para JSON
            'length': f.length,
            'replacement_cost': str(f.replacement_cost),  # Convertir a string para JSON
            'rating': f.rating,
            'last_update': f.last_update.isoformat() if f.last_update else None,
            'special_features': f.special_features
        } for f in films])
        
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
