import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Transactions = () => {
  const navigate = useNavigate();
  const [transactions, setTransactions] = useState([]);
  const [error, setError] = useState(null);

  const fetchTransactions = async () => {
    const token = localStorage.getItem("token");

    if (!token) {
      setError("Token não encontrado. Faça login novamente.");
      return;
    }

    try {
      const response = await axios.get("http://127.0.0.1:8000/transactions", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      setTransactions(response.data);
    } catch (err) {
      console.error("Erro ao buscar transações:", err.message);
      setError("Erro ao buscar transações. Tente novamente mais tarde.");
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  return (
    <div className="transactions-page">
      <h2>Histórico de Transações</h2>
      {error && <p className="error-message">{error}</p>}
      <button className="back-button" onClick={() => navigate("/invest")}>
        Voltar
      </button>
      {transactions.length > 0 ? (
        <table>
          <thead>
            <tr>
              <th>Nome da Moeda</th>
              <th>Quantidade</th>
              <th>Preço Total</th>
              <th>Tipo de Transação</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((transaction, index) => (
              <tr key={index}>
                <td>{transaction.coin_name}</td>
                <td>{transaction.quantity}</td>
                <td>{transaction.total_price.toFixed(2)}</td>
                <td>{transaction.transaction_type}</td>
                <td>{new Date(transaction.transaction_date).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>Nenhuma transação encontrada.</p>
      )}
    </div>
  );
};

export default Transactions;
