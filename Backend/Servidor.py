from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

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
        Store = Base.classes.store
        Rental = Base.classes.rental
        Payment = Base.classes.payment
        Inventory = Base.classes.inventory
        Customer = Base.classes.customer

    # Configura CORS
    CORS(app)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/stores', methods=['GET'])
    def get_stores():
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

    @app.route('/rent', methods=['POST'])
    def rent_movie():
        """
        Crea un nuevo registro de renta en la base de datos.
        """
        data = request.json
        try:
            # Extrae los datos del request
            inventory_id = data.get('inventory_id')
            customer_id = data.get('customer_id')
            staff_id = data.get('staff_id')
            rental_date = datetime.utcnow()

            # Crea un nuevo registro de renta
            new_rental = Rental(
                inventory_id=inventory_id,
                customer_id=customer_id,
                staff_id=staff_id,
                rental_date=rental_date,
                last_update=rental_date
            )

            # Guarda el nuevo registro en la base de datos
            db.session.add(new_rental)
            db.session.commit()

            return jsonify({"message": "Renta creada exitosamente!", "rental_id": new_rental.rental_id}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al crear la renta: " + error}), 500

    @app.route('/pay', methods=['POST'])
    def make_payment():
        """
        Crea un nuevo registro de pago en la base de datos.
        """
        data = request.json
        try:
            # Extrae los datos del request
            rental_id = data.get('rental_id')
            customer_id = data.get('customer_id')
            staff_id = data.get('staff_id')
            amount = data.get('amount')
            payment_date = datetime.utcnow()

            # Crea un nuevo registro de pago
            new_payment = Payment(
                customer_id=customer_id,
                staff_id=staff_id,
                rental_id=rental_id,
                amount=amount,
                payment_date=payment_date,
                last_update=payment_date
            )

            # Guarda el nuevo registro en la base de datos
            db.session.add(new_payment)
            db.session.commit()

            return jsonify({"message": "Pago registrado exitosamente!", "payment_id": new_payment.payment_id}), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al registrar el pago: " + error}), 500

    @app.route('/recent_rentals', methods=['GET'])
    def get_recent_rentals():
        """
        Obtiene las últimas 20 rentas junto con sus respectivos pagos.
        """
        try:
            # Consulta para obtener las últimas 20 rentas y sus pagos
            recent_rentals = db.session.query(Rental, Payment).join(
                Payment, Rental.rental_id == Payment.rental_id
            ).order_by(Rental.rental_date.desc()).limit(20).all()
    
            # Formatear la respuesta
            response = [{
                'rental_id': rental.rental_id,
                'inventory_id': rental.inventory_id,
                'customer_id': rental.customer_id,
                'staff_id': rental.staff_id,
                'rental_date': rental.rental_date.isoformat() if rental.rental_date else None,
                'payment_id': payment.payment_id,
                'amount': payment.amount,
                'payment_date': payment.payment_date.isoformat() if payment.payment_date else None
            } for rental, payment in recent_rentals]
    
            return jsonify(response), 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al obtener las rentas: " + error}), 500


    @app.route('/health', methods=['GET'])
    def health_check():
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
