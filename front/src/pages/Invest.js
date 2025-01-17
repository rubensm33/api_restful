import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import Chart from "chart.js/auto";

const Invest = () => {
  const navigate = useNavigate();

  const [selectedCoin, setSelectedCoin] = useState("Bitcoin");
  const [chartData, setChartData] = useState([]);
  const [coinDetails, setCoinDetails] = useState(null);
  const [chartInstance, setChartInstance] = useState(null);
  const [quantity, setQuantity] = useState(1);

  const coins = [
    "Bitcoin",
    "Ethereum",
    "XRP",
    "Tether USDt",
    "Solana",
    "BNB",
    "DogeCoin",
    "USDC",
    "Cardano",
    "TRON",
  ];

  const fetchCoinData = async (coinName) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/actives", {
        coin_name: coinName,
      });

      const data = response.data;
      const chartEntry = { time: new Date().toLocaleTimeString(), price: data.price };

      setChartData((prevData) => [...prevData.slice(-10), chartEntry]);
      setCoinDetails(data);
    } catch (error) {
      console.error("Erro ao buscar dados da moeda:", error.message);
    }
  };

  const updateChart = () => {
    if (chartInstance && chartData.length > 0) {
      chartInstance.data.labels = chartData.map((data) => data.time);
      chartInstance.data.datasets[0].data = chartData.map((data) => data.price);
      chartInstance.update();
    }
  };

  const handleBuyCoin = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      console.error("Token não encontrado. Faça login novamente.");
      return;
    }

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/transactions/buy",
        {
          coin_name: selectedCoin,
          quantity: parseFloat(quantity),
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      alert("Compra realizada com sucesso!");
    } catch (error) {
      console.error("Erro ao comprar moeda:", error.message);
      alert("Erro ao realizar a compra.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  useEffect(() => {
    const ctx = document.getElementById("cryptoChart").getContext("2d");

    const newChartInstance = new Chart(ctx, {
      type: "line",
      data: {
        labels: [],
        datasets: [
          {
            label: "Preço",
            data: [],
            borderColor: "#007BFF",
            backgroundColor: "rgba(0, 123, 255, 0.2)",
            tension: 0.4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { title: { display: true, text: "Horário" } },
          y: { title: { display: true, text: "Preço (USD)" } },
        },
      },
    });

    setChartInstance(newChartInstance);
    return () => newChartInstance.destroy();
  }, []);

  useEffect(() => {
    fetchCoinData(selectedCoin);
    const interval = setInterval(() => fetchCoinData(selectedCoin), 10000);
    return () => clearInterval(interval);
  }, [selectedCoin]);

  useEffect(() => {
    updateChart();
  }, [chartData]);

  return (
    <div className="invest-page">
      <div className="menu-lateral">
        <h3>Menu</h3>
        <ul>
          <li onClick={() => navigate("/transactions")}>Visualizar Transações</li>
          <li onClick={() => navigate("/portifolio")}>Portifólio</li>
          <li onClick={() => navigate("/sell")}>Vender Ações</li>
        </ul>
        <button className="logout-button" onClick={handleLogout}>
          Logout
        </button>
      </div>

      <div className="invest-container">
        <h2>Gráfico de Preço</h2>
        <select
          value={selectedCoin}
          onChange={(e) => setSelectedCoin(e.target.value)}
        >
          {coins.map((coin, index) => (
            <option key={index} value={coin}>
              {coin}
            </option>
          ))}
        </select>

        <div className="chart-container">
          <canvas id="cryptoChart"></canvas>
        </div>

        {coinDetails && (
          <div className="coin-details">
            <h3>Detalhes da Moeda</h3>
            <table>
              <thead>
                <tr>
                  <th>Volume (24h)</th>
                  <th>Variação (1h)</th>
                  <th>Variação (24h)</th>
                  <th>Variação (7d)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>{coinDetails.volume_24h.toFixed(2)}</td>
                  <td>{coinDetails.percent_change_1h.toFixed(2)}%</td>
                  <td>{coinDetails.percent_change_24h.toFixed(2)}%</td>
                  <td>{coinDetails.percent_change_7d.toFixed(2)}%</td>
                </tr>
              </tbody>
            </table>
            <div className="buy-section">
              <input
                type="number"
                min="1"
                value={quantity}
                onChange={(e) => setQuantity(e.target.value)}
                placeholder="Quantidade"
              />
              <button onClick={handleBuyCoin}>Comprar</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Invest;
