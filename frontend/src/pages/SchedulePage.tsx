import { useState, useEffect } from "react";
import { getServices } from "../api/services";

export default function SchedulePage() {

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [services, setServices] = useState([]);

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
      background: "#fff",
      padding: "40px",
      borderRadius: "10px",
      boxShadow: "0 5px 15px rgba(0,0,0,0.1)"
    }}>

      {/* LOGO */}
      <img
        src="https://via.placeholder.com/120"
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
      <h2 style={{ margin: "10px 0" }}>
        Marcus Barbearia
      </h2>

      {/* TÍTULO */}
      <h3 style={{ marginTop: "30px", marginBottom: "20px" }}>
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
          border: "1px solid #ccc"
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
        <div style={{ marginTop: "20px" }}>

          <h3>Escolha o serviço</h3>

          {services.map((service: any) => (
            <div key={service.id}>
              <label>
                <input type="radio" name="service" />
               {service.name} ({service.duration_minutes} min)
              </label>
            </div>
    ))}

  </div>
)}

      {/* BOTÃO */}
      <button
        style={{
          width: "100%",
          padding: "12px",
          background: "#000",
          color: "#fff",
          border: "none",
          borderRadius: "5px",
          cursor: "pointer",
          fontSize: "16px"
        }}
      >
        Continuar
      </button>

    </div>
  );
}