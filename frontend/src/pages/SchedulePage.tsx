import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getServices } from "../api/services";
import "../styles/SchedulePage.css";
import logo from "../assets/logo.jpg";

export default function SchedulePage() {

  const { slug } = useParams();

  const [tenant, setTenant] = useState<any>(null);

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");

  const [services, setServices] = useState<any[]>([]);
  const [selectedService, setSelectedService] = useState<number | null>(null);

  const [date, setDate] = useState("");
  const [slots, setSlots] = useState<string[]>([]);
  const [selectedSlot, setSelectedSlot] = useState<string | null>(null);

  const [confirmation, setConfirmation] = useState<any | null>(null);

  const theme = {
    pink: "#ff4fa0",
    pinkDark: "#36232c"
  };

  // ================================
  // CARREGA TENANT PELO SLUG
  // ================================
  useEffect(() => {

    async function loadTenant() {

      try {

        const response = await fetch(
          `http://127.0.0.1:8000/tenants/slug/${slug}`
        );

        const data = await response.json();

        setTenant(data);

      } catch (error) {

        console.error("Erro ao carregar tenant", error);

      }

    }

    if (slug) loadTenant();

  }, [slug]);

  // ================================
  // CARREGA SERVICOS
  // ================================
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

  // ================================
  // CARREGA HORARIOS DISPONIVEIS
  // ================================
  async function loadSlots(selectedDate: string) {

    if (!selectedService || !tenant) return;

    try {

      const response = await fetch(
        `http://127.0.0.1:8000/slots/available?tenant_id=${tenant.id}&service_id=${selectedService}&appointment_date=${selectedDate}`
      );

      const data = await response.json();

      setSlots(data);

    } catch (error) {

      console.error("Erro ao buscar horários", error);

    }

  }

  // ================================
  // CRIAR AGENDAMENTO
  // ================================
  async function handleSchedule() {

    if (!name || !phone || !selectedService || !selectedSlot || !date) {
      alert("Preencha todos os campos");
      return;
    }

    try {

      const customerResponse = await fetch(
        "http://127.0.0.1:8000/customers/find-or-create",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            tenant_id: tenant.id,
            name,
            phone
          })
        }
      );

      const customer = await customerResponse.json();

      const startAt = `${date}T${selectedSlot}`;

      const appointmentResponse = await fetch(
        "http://127.0.0.1:8000/appointments/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            tenant_id: tenant.id,
            customer_id: customer.id,
            service_id: selectedService,
            start_at: startAt
          })
        }
      );

      // TRATAMENTO DE ERRO DO BACKEND
      if (!appointmentResponse.ok) {

        const error = await appointmentResponse.json();

        alert(error.detail);

        return;
      }

      await appointmentResponse.json();

      setConfirmation({
        customerName: name,
        serviceId: selectedService,
        date,
        slot: selectedSlot
      });

    } catch (error) {

      console.error("Erro ao agendar", error);

    }

  }

  // ================================
  // NOME DO SERVICO
  // ================================
  function getServiceName() {

    const service = services.find(
      (s: any) => s.id === selectedService
    );

    return service ? service.name : "";

  }

  // ================================
  // FORMATACAO PARA DATAS BR
  // ================================
  function formatDateBR(dateString: string) {

    const date = new Date(dateString + "T00:00:00");

    const formattedDate = date.toLocaleDateString("pt-BR");

    const weekday = date.toLocaleDateString("pt-BR", {
      weekday: "long"
    });

    const capitalizedWeekday =
      weekday.charAt(0).toUpperCase() + weekday.slice(1);

    return `${formattedDate} (${capitalizedWeekday})`;

  }

  // ================================
  // TELA DE CONFIRMACAO
  // ================================
  if (confirmation) {

    return (

      <div className="confirmation-card">

        <h2 style={{ color: "#ff4fa0" }}>
          Agendamento confirmado 🎉
        </h2>

        <p><strong>Paciente:</strong> {confirmation.customerName}</p>

        <p><strong>Serviço:</strong> {getServiceName()}</p>

        <p><strong>Data:</strong> {formatDateBR(confirmation.date)}</p>

        <p><strong>Horário:</strong> {confirmation.slot.substring(0, 5)}</p>

      </div>

    );

  }

  // ================================
  // PAGINA DE AGENDAMENTO
  // ================================
  return (

    <div className="schedule-container">

      <img
        src={logo}
        alt="Logo"
        className="schedule-logo"
      />

      <h2 style={{
        color: theme.pink,
        fontWeight: 600
      }}>
        {tenant?.name}
      </h2>

      <h3 style={{
        color: theme.pinkDark,
        fontWeight: 600,
        marginTop: "25px",
        marginBottom: "25px"
      }}>
        Agendamento
      </h3>

      <input
        type="text"
        placeholder="Seu nome"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="schedule-input"
      />

      <input
        type="text"
        placeholder="Seu telefone"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        className="schedule-input"
      />

      {services.length > 0 && (

        <div>

          <h3>Escolha o serviço</h3>

          {services.map((service: any) => (

            <div
              key={service.id}
              onClick={() => setSelectedService(service.id)}
              className={`service-card ${
                selectedService === service.id ? "service-selected" : ""
              }`}
            >

              <strong>{service.name}</strong>

              <div className="service-duration">
                {service.duration_minutes} minutos
              </div>

            </div>

          ))}

        </div>

      )}

      {selectedService && (

        <>

          <h3>Escolha a data</h3>

          <input
            type="date"
            value={date}
            onChange={(e) => {

              const selectedDate = e.target.value;

              setDate(selectedDate);

              loadSlots(selectedDate);

            }}
            className="schedule-input"
          />

        </>

      )}

      {slots.length > 0 && (

        <div>

          <h3>Horários disponíveis</h3>

          {slots.map((slot: string, index: number) => (

            <div
              key={index}
              onClick={() => setSelectedSlot(slot)}
              className={`slot-card ${
                selectedSlot === slot ? "slot-selected" : ""
              }`}
            >

              {slot.substring(0, 5)}

            </div>

          ))}

        </div>

      )}

      <button
        className="continue-button"
        onClick={handleSchedule}
      >
        CONFIRMAR
      </button>

    </div>

  );

}