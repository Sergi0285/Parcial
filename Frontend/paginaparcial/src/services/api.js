const API_URL = 'http://ec2-54-89-111-85.compute-1.amazonaws.com:5000';

export const getUsuarios = async () => {
  const response = await fetch(`${API_URL}/usuarios`);
  return await response.json();
};

export const createUsuario = async (data) => {
  const response = await fetch(`${API_URL}/usuarios`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return await response.json();
};

export const deleteUsuario = async (id) => {
  const response = await fetch(`${API_URL}/usuarios/${id}`, {
    method: 'DELETE',
  });
  return await response.json();
};

export const updateUsuario = async (id, data) => {
  const response = await fetch(`${API_URL}/usuarios/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  return await response.json();
};
