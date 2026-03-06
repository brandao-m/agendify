import { useState } from 'react';

export default function SchedulePage() {

    const [name, setName] = useState("");
    const [phone, setPhone] = useState("");

    return (
        <div style={{
            maxWidth: '500px',
            margin: '80px auto',
            fontFamily: 'Arial'
        }}>

            <h1>Agendar Horario</h1>

            <div style={{ marginTop: '30px'}}>
                <label>Nome</label>
                <input
                type='text'
                value={name}
                onChange={(e) => setName(e.target.value)}
                style={{ width: '100%', padding: '10px', marginTop: '5px' }}
                />
            </div>
    
        <div style={{ marginTop: '20px' }}>
            <label>Telefone</label>
            <input
                type='text'
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                style={{ width: '100%', padding: '10px', marginTop: '5px' }}
                />
            </div>

            <button
                style={{
                    marginTop: '30px',
                    padding: '12px',
                    width: '100%',
                    background: '#000',
                    color: '#fff',
                    border: 'none',
                    cursor: 'pointer'
                }}
                >
                    Continuar
                </button>

            </div>
    );
}