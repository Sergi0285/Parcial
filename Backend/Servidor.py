from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


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
        Staff = Base.classes.staff
        Film = Base.classes.film

    # Configura CORS
    CORS(app)

    @app.route('/stores', methods=['GET'])
    def get_stores():
        try:
            stores = db.session.query(Store.store_id).all()
            return jsonify([{
                'store_id': s[0]
            } for s in stores])
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al acceder a la base de datos: " + error}), 500

    @app.route('/customers/<int:store_id>', methods=['GET'])
    def get_customers_by_store(store_id):
        try:
            customers = db.session.query(Customer.customer_id, Customer.first_name, Customer.last_name).filter(Customer.store_id == store_id).all()
            return jsonify([{
                'customer_id': c[0],
                'first_name': c[1],
                'last_name': c[2]
            } for c in customers])
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al acceder a la base de datos: " + error}), 500

    @app.route('/staff/<int:store_id>', methods=['GET'])
    def get_staff_by_store(store_id):
        try:
            staff = db.session.query(Staff.staff_id, Staff.first_name, Staff.last_name).filter(Staff.store_id == store_id).all()
            return jsonify([{
                'staff_id': s[0],
                'first_name': s[1],
                'last_name': s[2]
            } for s in staff])
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al acceder a la base de datos: " + error}), 500

    @app.route('/inventory/<int:store_id>', methods=['GET'])
    def get_inventory_by_store(store_id):
        try:
            # Consulta que une las tablas Inventory y Film
            inventory = db.session.query(Inventory.inventory_id, Inventory.film_id, Film.title, Film.replacement_cost).join(Film, Inventory.film_id == Film.film_id)  # Realiza la unión con la tabla Film
            
            # Filtra por el store_id
            inventory = inventory.filter(Inventory.store_id == store_id).all()

            return jsonify([{
                'inventory_id': i[0],
                'film_id': i[1],
                'film_title': i[2],
                'replacement_cost': i[3]
            } for i in inventory])
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al acceder a la base de datos: " + error}), 500
        
    @app.route('/rent', methods=['OPTIONS', 'POST'])  # Cambiar a POST ya que estás creando un nuevo registro
    def rent_movie():
        
        data = request.json
        try:
            # Extrae los datos del request
            inventory_id = data.get('inventory_id')
            customer_id = data.get('customer_id')
            staff_id = data.get('staff_id')
            rental_date = datetime.utcnow()
            # Calcula la fecha de devolución (una semana después de la fecha actual)
            return_date = rental_date + timedelta(weeks=1)

            # Crea un nuevo registro de renta
            new_rental = Rental(
                inventory_id=inventory_id,
                customer_id=customer_id,
                staff_id=staff_id,
                rental_date=rental_date,
                return_date=return_date,  # Asegúrate de que este campo exista en tu modelo Rental
                last_update=rental_date
            )

            # Guarda el nuevo registro en la base de datos
            db.session.add(new_rental)
            db.session.commit()

            return jsonify({"message": "Renta creada exitosamente!", "rental_id": new_rental.rental_id, "return_date": return_date.isoformat()}), 201
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
        Obtiene las últimas 20 rentas junto con sus respectivos pagos y detalles adicionales.
        """
        try:
            # Consulta para obtener las últimas 20 rentas con detalles
            recent_rentals = db.session.query(
                Rental,
                Payment,
                Customer.first_name.label('customer_first_name'),
                Customer.last_name.label('customer_last_name'),
                Film.title.label('film_title'),
                Store.store_id,
                Staff.first_name.label('staff_first_name'),
                Staff.last_name.label('staff_last_name'),
                Payment.amount
            ).join(Payment, Rental.rental_id == Payment.rental_id) \
            .join(Customer, Rental.customer_id == Customer.customer_id) \
            .join(Inventory, Rental.inventory_id == Inventory.inventory_id) \
            .join(Film, Inventory.film_id == Film.film_id) \
            .join(Staff, Rental.staff_id == Staff.staff_id) \
            .join(Store, Staff.store_id == Store.store_id) \
            .order_by(Rental.rental_date.asc()).limit(20).all()

            # Formatear la respuesta
            response = [{
                'rental_id': rental.rental_id,
                'customer_full_name': f"{rental.customer_first_name} {rental.customer_last_name}",
                'film_title': rental.film_title,
                'store_id': rental.store_id,
                'staff_full_name': f"{rental.staff_first_name} {rental.staff_last_name}",
                'amount': payment.amount,
                'rental_date': rental.rental_date.isoformat() if rental.rental_date else None,
                'payment_date': payment.payment_date.isoformat() if payment.payment_date else None
            } for rental, payment in recent_rentals]

            return jsonify(response), 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return jsonify({"error": "Error al obtener las rentas: " + error}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
