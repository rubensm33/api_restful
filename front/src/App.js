import React from "react";
import { Routes, Route } from "react-router-dom";
import HomePage from "./components/HomePage";
import Register from "./pages/Register";
import Invest from "./pages/Invest";
import Portifolio from "./pages/Portifolio";
import Transactions from "./pages/Transactions";
import Sell from "./pages/Sell";

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/register" element={<Register />} />
      <Route path="/invest" element={<Invest />} />
      <Route path="/portifolio" element={<Portifolio />} />
      <Route path="/transactions" element={<Transactions />} />
      <Route path="/sell" element={<Sell />} />
    </Routes>
  );
}

export default App;
