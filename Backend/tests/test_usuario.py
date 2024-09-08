import pytest
from Servidor import create_test_app, db, Usuario

@pytest.fixture
def client():
    app = create_test_app()

    # Abre el cliente de pruebas
    with app.test_client() as client:
        # Contexto de aplicación para operaciones con la base de datos
        with app.app_context():
            db.create_all()  # Crea todas las tablas
        yield client  # Lo que se devuelva aquí estará disponible en las pruebas
        # Limpiar la base de datos después de cada prueba
        with app.app_context():
            db.drop_all()

# Prueba para crear un usuario
def test_create_usuario(client):
    response = client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json()['mensaje'] == 'Usuario creado exitosamente'

# Prueba para obtener todos los usuarios
def test_get_usuarios(client):
    # Primero, creamos un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, verificamos que la lista de usuarios tiene al menos uno
    response = client.get('/usuarios')
    assert response.status_code == 200
    usuarios = response.get_json()
    assert len(usuarios) == 1
    assert usuarios[0]['nombre'] == 'Juan'

# Prueba para obtener un usuario específico
def test_get_usuario(client):
    # Primero, creamos un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, obtenemos el usuario por su ID
    response = client.get('/usuarios/1')
    assert response.status_code == 200
    usuario = response.get_json()
    assert usuario['nombre'] == 'Juan'

# Prueba para actualizar un usuario
def test_update_usuario(client):
    # Primero, creamos un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, lo actualizamos
    response = client.put('/usuarios/1', json={
        'nombre': 'Juan actualizado',
        'apellido': 'Pérez actualizado',
        'fechaNacimiento': '1990-01-01',
        'password': 'newpassword123'
    })
    assert response.status_code == 200
    assert response.get_json()['mensaje'] == 'Usuario actualizado exitosamente'

# Prueba para eliminar un usuario
def test_delete_usuario(client):
    # Primero, creamos un usuario
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'password123'
    })
    
    # Luego, eliminamos el usuario
    response = client.delete('/usuarios/1')
    assert response.status_code == 204
