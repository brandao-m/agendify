import { useState, useEffect } from "react";
import { getServices } from "../api/services";
import "../styles/SchedulePage.css";
import logo from '../assets/logo.jpg'

export default function SchedulePage() {

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [services, setServices] = useState([]);
  const [selectedService, setSelectedService] = useState<number | null>(null);
  const theme = {
    background: "#ff6fae",
    primary: "#ff4fa0",
    pink: "#ff4fa0",
    pinkh3: "#36232c",
    blue: "#4db8ff",
    white: "#ffffff"
};

  useEffect(() => {

  async function loadServices() {
    try {
      const data = await getServices();
      setServices(data);
    } catch (error) {
      console.error(error);
    }
  }

  loadServices();

}, []);

  return (
    <div style={{
      maxWidth: "420px",
      margin: "80px auto",
      fontFamily: "Arial",
      textAlign: "center",
      background: theme.white,
      padding: "40px",
      borderRadius: "14px",
      boxShadow: "0 12px 30px rgba(0,0,0,0.15)"
    }}>

      {/* LOGO */}
      <img
        src={logo}
        alt="Logo"
        style={{
          width: "120px",
          height: "120px",
          borderRadius: "50%",
          objectFit: "cover",
          marginBottom: "15px"
        }}
      />

      {/* NOME DO ESTABELECIMENTO */}
      <h2 style={{ 
        margin: "10px 0",
        color: theme.pink
        }}>
        Dra. Daisy Almeida
      </h2>

      {/* TÍTULO */}
      <h3 style={{ 
        marginTop: "30px",
        marginBottom: "20px",
        color: theme.pinkh3 
        }}>
        AGENDAMENTO
      </h3>

      {/* INPUT NOME */}
      <input
        type="text"
        placeholder="Seu nome"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{
          width: "100%",
          padding: "12px",
          marginBottom: "15px",
          borderRadius: "5px",
          border: "1px solid #e5e5e5"
        }}
      />

      {/* INPUT TELEFONE */}
      <input
        type="text"
        placeholder="Seu telefone"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        style={{
          width: "100%",
          padding: "12px",
          marginBottom: "25px",
          borderRadius: "5px",
          border: "1px solid #ccc"
        }}
      />

      {services.length > 0 && (
        <div style={{
          marginTop: "20px",
          color: theme.pinkh3
          }}>

          <h3>Escolha o serviço</h3>

          {services.map((service: any) => {

  const isSelected = selectedService === service.id;

  return (
    <div
      key={service.id}
      onClick={() => setSelectedService(service.id)}
      className={`service-card ${
        selectedService === service.id ? "service-selected" : ""
        }`}
      style={{
        marginBottom: "12px",
        padding: "14px",
        borderRadius: "8px",
        border: isSelected ? "3px solid ${theme.blue}" : "1px solid #ddd",
        background: isSelected ? "#e8f6ff" : "#fff",
        cursor: "pointer",
        textAlign: "left",
        transition: "0.2s"
      }}
    >
      <strong>{service.name}</strong>
      <div style={{ fontSize: "14px", color: "#666" }}>
        {service.duration_minutes} minutos
      </div>
    </div>
  );
})}

  </div>
)}

      {/* BOTÃO CONTINUAR */}
      <button className="continue-button">
        Continuar
      </button>

    </div>
  );
}