import { BrowserRouter, Routes, Route } from "react-router-dom";
import SchedulePage from "./pages/SchedulePage";

function App() {

  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<div style={{color:"white", textAlign:"center", marginTop:"100px"}}>Agendify</div>} />

        <Route path="/:slug" element={<SchedulePage />} />

      </Routes>

    </BrowserRouter>
  )

}

export default App