import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const getPasswordStrength = (password) => {
  let strength = 0;

  if (password.length >= 8) strength++; 
  if (/[A-Z]/.test(password)) strength++; 
  if (/[0-9]/.test(password)) strength++; 
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) strength++; 

  return strength;
};

const Register = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
  });
  const [passwordStrength, setPasswordStrength] = useState(0);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    if (name === "password") {
      setPasswordStrength(getPasswordStrength(value));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
  
    const { nomeBanco, agencia, numeroConta, digitoVerificador, ...requestData } = formData;
  
    if (passwordStrength < 3) {
      setError("A senha deve ser forte. Inclua pelo menos 8 caracteres, letras maiúsculas, números e caracteres especiais.");
      return;
    }
  
    try {
      await axios.post("http://localhost:8000/users", requestData); 
      navigate("/");
    } catch (err) {
      console.error("Erro ao cadastrar:", err.response?.data || err.message);
      setError(err.response?.data?.detail || "Erro ao cadastrar.");
    }
  };
  

  const renderPasswordStrength = () => {
    let strengthText = "";
    let strengthColor = "";

    switch (passwordStrength) {
      case 0:
      case 1:
        strengthText = "Senha fraca";
        strengthColor = "red";
        break;
      case 2:
        strengthText = "Senha média";
        strengthColor = "yellow";
        break;
      case 3:
      case 4:
        strengthText = "Senha forte";
        strengthColor = "green";
        break;
      default:
        strengthText = "Insira uma senha";
    }

    return (
      <div className="password-strength">
        <p style={{ color: strengthColor }}>{strengthText}</p>
        <div className="strength-bar">
          <div
            style={{
              width: `${(passwordStrength / 4) * 100}%`,
              backgroundColor: strengthColor,
              height: "5px",
              borderRadius: "3px",
              transition: "width 0.3s ease",
            }}
          />
        </div>
      </div>
    );
  };

  return (
    <div className="register-page">
      <h2 className="register-title">Cadastro</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="name"
          placeholder="Nome"
          value={formData.name}
          onChange={handleChange}
          required
        />
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <div className="password-container">
          <input
            type="password"
            name="password"
            placeholder="Senha"
            value={formData.password}
            onChange={handleChange}
            required
          />
          {renderPasswordStrength()}
        </div>
        <input
          type="text"
          name="nomeBanco"
          placeholder="Nome do Banco"
          value={formData.nomeBanco}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="agencia"
          placeholder="Agência"
          value={formData.agencia}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="numeroConta"
          placeholder="Número da Conta"
          value={formData.numeroConta}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="digitoVerificador"
          placeholder="Dígito Verificador"
          value={formData.digitoVerificador}
          onChange={handleChange}
          required
        />
        <div className="button-container">
          <button type="submit">Cadastrar</button>
          <button type="button" onClick={() => navigate("/")}>
            Cancelar
          </button>
        </div>
      </form>
    </div>
  );
};

export default Register;
