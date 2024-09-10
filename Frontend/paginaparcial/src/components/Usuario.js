import React, { useState, useEffect } from 'react';
import { getUsuarios, createUsuario } from '../services/api';
import '../App.css'; // Ruta actualizada para reflejar la ubicación correcta

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

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const day = date.getDate().toString().padStart(2, '0');
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const year = date.getFullYear();
    return `${day}/${month}/${year}`;
  };

  return (
    <div className="usuario-container">
      <h2 className="titulo-centrado">Usuarios</h2>
      <table className="usuario-table">
        <thead>
          <tr>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Fecha de Nacimiento</th>
            <th>Contraseña</th>
          </tr>
        </thead>
        <tbody>
          {usuarios.map(usuario => (
            <tr key={usuario.id}>
              <td>{usuario.nombre}</td>
              <td>{usuario.apellido}</td>
              <td>{formatDate(usuario.fechaNacimiento)}</td>
              <td>{usuario.password}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3 className="titulo-centrado">Crear Usuario</h3>
      <form onSubmit={handleSubmit}>
        <label>
          Nombre:
          <input type="text" name="nombre" placeholder="Nombre" value={formData.nombre} onChange={handleInputChange} />
        </label>
        <label>
          Apellido:
          <input type="text" name="apellido" placeholder="Apellido" value={formData.apellido} onChange={handleInputChange} />
        </label>
        <label>
          Fecha de Nacimiento:
          <input type="date" name="fechaNacimiento" placeholder="Fecha Nacimiento" value={formData.fechaNacimiento} onChange={handleInputChange} />
        </label>
        <label>
          Contraseña:
          <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleInputChange} />
        </label>
        <button type="submit">Crear</button>
      </form>
    </div>
  );
};

export default Usuario;
