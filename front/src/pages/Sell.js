import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Sell = () => {
  const navigate = useNavigate();
  const [portfolio, setPortfolio] = useState([]);
  const [selectedCoin, setSelectedCoin] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [sellPrice, setSellPrice] = useState(0);
  const [error, setError] = useState(null);

  const fetchPortfolio = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("Token não encontrado. Faça login novamente.");
      return;
    }

    try {
      const response = await axios.get("http://127.0.0.1:8000/coin/user", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setPortfolio(response.data);
    } catch (err) {
      console.error("Erro ao buscar portfólio:", err.message);
      setError("Erro ao buscar portfólio. Tente novamente mais tarde.");
    }
  };

  const handleSellCoin = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("Token não encontrado. Faça login novamente.");
      return;
    }

    if (!selectedCoin || quantity < 1 || sellPrice <= 0) {
      alert("Selecione uma moeda, insira uma quantidade válida e um preço de venda.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/coin/sell",
        {
          coin_id: selectedCoin.id,
          quantity: parseInt(quantity),
          sell_price: parseFloat(sellPrice),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      alert("Venda realizada com sucesso!");
      fetchPortfolio(); 
    } catch (err) {
      console.error("Erro ao vender moeda:", err.message);
      alert("Erro ao realizar a venda.");
    }
  };

  useEffect(() => {
    fetchPortfolio();
  }, []);

  return (
    <div className="sell-page">
      <h2>Vender Ações</h2>
      <button className="back-button" onClick={() => navigate("/invest")}>
        Voltar
      </button>
      {error && <p className="error-message">{error}</p>}

      {portfolio.length > 0 ? (
        <div className="sell-form">
          <select
            onChange={(e) =>
              setSelectedCoin(
                portfolio.find((coin) => coin.id === parseInt(e.target.value))
              )
            }
          >
            <option value="">Selecione uma moeda</option>
            {portfolio.map((coin) => (
              <option key={coin.id} value={coin.id}>
                {coin.name} - Quantidade: {coin.quantity}
              </option>
            ))}
          </select>
          {selectedCoin && (
            <div>
              <p>
                Preço de Compra: ${selectedCoin.price.toFixed(2)} | Quantidade:{" "}
                {selectedCoin.quantity}
              </p>
              <input
                type="number"
                min="1"
                max={selectedCoin.quantity}
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="Quantidade"
              />
              <input
                type="number"
                min="0.01"
                step="0.01"
                value={sellPrice}
                onChange={(e) => setSellPrice(e.target.value)}
                placeholder="Preço de Venda"
              />
              <button onClick={handleSellCoin}>Vender</button>
            </div>
          )}
        </div>
      ) : (
        <p>Seu portfólio está vazio.</p>
      )}
    </div>
  );
};

export default Sell;
