import React, { useState, useEffect } from 'react';
import { getUsuarios, createUsuario, deleteUsuario } from '../services/api';
import './App.css'; // Asegúrate de que el CSS esté importado

const Usuario = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [formData, setFormData] = useState({
    nombre: '',
    apellido: '',
    fechaNacimiento: '',
    password: ''
  });

  useEffect(() => {
    cargarUsuarios();
  }, []);

  const cargarUsuarios = async () => {
    const data = await getUsuarios();
    setUsuarios(data);
  };

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createUsuario(formData);
    setFormData({ nombre: '', apellido: '', fechaNacimiento: '', password: '' });
    cargarUsuarios();
  };

  const handleDelete = async (id) => {
    await deleteUsuario(id);
    cargarUsuarios();
  };

  return (
    <div className="usuario-container">
      <h2>Usuarios</h2>
      <ul className="usuario-list">
        {usuarios.map(usuario => (
          <li key={usuario.id} className="usuario-list-item">
            {usuario.nombre} {usuario.apellido} - {usuario.fechaNacimiento}
            <button onClick={() => handleDelete(usuario.id)}>Eliminar</button>
          </li>
        ))}
      </ul>

      <h3>Crear Usuario</h3>
      <form onSubmit={handleSubmit}>
        <input type="text" name="nombre" placeholder="Nombre" value={formData.nombre} onChange={handleInputChange} />
        <input type="text" name="apellido" placeholder="Apellido" value={formData.apellido} onChange={handleInputChange} />
        <input type="date" name="fechaNacimiento" placeholder="Fecha Nacimiento" value={formData.fechaNacimiento} onChange={handleInputChange} />
        <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleInputChange} />
        <button type="submit">Crear</button>
      </form>
    </div>
  );
};

export default Usuario;
