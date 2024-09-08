import pytest
from app import app, db, Usuario
from flask import json

@pytest.fixture
def client():
    # Configurar la aplicación para pruebas
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Base de datos en memoria para pruebas
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Crear una instancia de cliente de pruebas
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Crear todas las tablas
        yield client
        with app.app_context():
            db.drop_all()  # Eliminar todas las tablas al final

def test_create_usuario(client):
    # Datos de ejemplo para la creación de un usuario
    data = {
        'nombre': 'Juan',
        'apellido': 'Perez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    }
    
    # Enviar la solicitud POST al endpoint /usuarios
    response = client.post('/usuarios', json=data)
    
    # Verificar el código de estado 201 (creado exitosamente)
    assert response.status_code == 201
    
    # Verificar que el usuario ha sido creado en la base de datos
    usuario = Usuario.query.filter_by(nombre='Juan').first()
    assert usuario is not None
    assert usuario.apellido == 'Perez'

def test_get_usuarios(client):
    # Insertar un usuario en la base de datos
    usuario = Usuario(nombre='Maria', apellido='Lopez', fechaNacimiento='1995-05-15', password='password456')
    db.session.add(usuario)
    db.session.commit()

    # Enviar la solicitud GET al endpoint /usuarios
    response = client.get('/usuarios')
    data = json.loads(response.data)
    
    # Verificar que el código de estado sea 200 y que el usuario esté en la respuesta
    assert response.status_code == 200
    assert len(data) == 1
    assert data[0]['nombre'] == 'Maria'

def test_get_usuario_by_id(client):
    # Insertar un usuario en la base de datos
    usuario = Usuario(nombre='Carlos', apellido='Garcia', fechaNacimiento='1988-12-12', password='password789')
    db.session.add(usuario)
    db.session.commit()

    # Enviar la solicitud GET al endpoint /usuarios/<id>
    response = client.get(f'/usuarios/{usuario.id}')
    data = json.loads(response.data)
    
    # Verificar que el código de estado sea 200 y que los datos coincidan
    assert response.status_code == 200
    assert data['nombre'] == 'Carlos'
    assert data['apellido'] == 'Garcia'

def test_update_usuario(client):
    # Insertar un usuario en la base de datos
    usuario = Usuario(nombre='Ana', apellido='Martinez', fechaNacimiento='2000-03-10', password='password000')
    db.session.add(usuario)
    db.session.commit()

    # Datos actualizados
    updated_data = {
        'nombre': 'Ana Maria',
        'apellido': 'Martinez Gonzalez',
        'password': 'newpassword000'
    }

    # Enviar la solicitud PUT al endpoint /usuarios/<id>
    response = client.put(f'/usuarios/{usuario.id}', json=updated_data)
    
    # Verificar que el código de estado sea 200
    assert response.status_code == 200
    
    # Verificar que el usuario haya sido actualizado
    usuario = Usuario.query.get(usuario.id)
    assert usuario.nombre == 'Ana Maria'
    assert usuario.apellido == 'Martinez Gonzalez'

def test_delete_usuario(client):
    # Insertar un usuario en la base de datos
    usuario = Usuario(nombre='Pedro', apellido='Suarez', fechaNacimiento='1993-07-07', password='password999')
    db.session.add(usuario)
    db.session.commit()

    # Enviar la solicitud DELETE al endpoint /usuarios/<id>
    response = client.delete(f'/usuarios/{usuario.id}')
    
    # Verificar que el código de estado sea 200
    assert response.status_code == 200
    
    # Verificar que el usuario haya sido eliminado
    usuario = Usuario.query.get(usuario.id)
    assert usuario is None
