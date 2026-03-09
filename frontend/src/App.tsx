import { BrowserRouter, Routes, Route } from "react-router-dom";
import SchedulePage from "./pages/SchedulePage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* ROTA DINÂMICA SaaS */}
        <Route path="/" element={<div>Informe o link da empresa</div>} />
        <Route path="/:slug" element={<SchedulePage />} />

      </Routes>
    </BrowserRouter>
  );
}

export default App;