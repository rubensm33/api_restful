import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Portifolio = () => {
  const navigate = useNavigate();
  const [portifolio, setPortifolio] = useState([]);
  const [error, setError] = useState(null);

  const fetchPortifolio = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("Token não encontrado. Faça login novamente.");
      return;
    }

    try {
      const response = await axios.get("http://127.0.0.1:8000/coin/average-price", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setPortifolio(response.data);
    } catch (err) {
      console.error("Erro ao buscar portifólio:", err.message);
      setError("Erro ao buscar portifólio. Tente novamente mais tarde.");
    }
  };

  useEffect(() => {
    fetchPortifolio();
  }, []);

  return (
    <div className="portifolio-page">
      <h2>Portifólio</h2>
      {error && <p className="error-message">{error}</p>}
      <button className="back-button" onClick={() => navigate("/invest")}>
        Voltar
      </button>
      {portifolio.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Nome</th>
              <th>Quantidade</th>
              <th>Preço Médio</th>
            </tr>
          </thead>
          <tbody>
            {portifolio.map((portifolio, index) => (
              <tr key={index}>
                <td>{portifolio.name}</td>
                <td>{portifolio.quantity}</td>
                <td>{portifolio.average_price.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Nenhuma ação encontrada.</p>
      )}
    </div>
  );
};

export default Portifolio;
