import { BrowserRouter, Routes, Route } from "react-router-dom";
import SchedulePage from "./pages/SchedulePage";

function Home() {

  return (

    <div style={{
      display:"flex",
      justifyContent:"center",
      alignItems:"center",
      height:"100vh",
      fontSize:"40px",
      fontWeight:600,
      color:"#ffffff"
    }}>
      Agendify
    </div>

  );

}

function App() {

  return (

    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Home />} />

        <Route path="/:slug" element={<SchedulePage />} />

      </Routes>

    </BrowserRouter>

  );

}

export default App;