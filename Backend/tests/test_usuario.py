import pytest
from Servidor import create_test_app, db, Usuario

@pytest.fixture
def client():
    app = create_test_app()
    with app.test_client() as client:
        yield client
    # Clean up after each test
    with app.app_context():
        db.drop_all()

def test_create_usuario(client):
    response = client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'secret'
    })
    assert response.status_code == 201
    assert response.json.get('message') == 'Usuario creado exitosamente'

def test_get_usuarios(client):
    client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'secret'
    })
    response = client.get('/usuarios')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_usuario(client):
    res = client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'secret'
    })
    assert res.status_code == 201
    user_id = res.json.get('id')  # Use get to avoid KeyError
    response = client.get(f'/usuarios/{user_id}')
    assert response.status_code == 200
    assert response.json.get('nombre') == 'Juan'

def test_update_usuario(client):
    res = client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'secret'
    })
    assert res.status_code == 201
    user_id = res.json.get('id')  # Use get to avoid KeyError
    response = client.put(f'/usuarios/{user_id}', json={
        'nombre': 'Juan Updated'
    })
    assert response.status_code == 200
    assert response.json.get('message') == 'Usuario actualizado exitosamente'

def test_delete_usuario(client):
    res = client.post('/usuarios', json={
        'nombre': 'Juan',
        'apellido': 'Pérez',
        'fechaNacimiento': '1990-01-01',
        'password': 'secret'
    })
    assert res.status_code == 201
    user_id = res.json.get('id')  # Use get to avoid KeyError
    response = client.delete(f'/usuarios/{user_id}')
    assert response.status_code == 200
    assert response.json.get('message') == 'Usuario borrado exitosamente'
    response = client.get(f'/usuarios/{user_id}')
    assert response.status_code == 404
