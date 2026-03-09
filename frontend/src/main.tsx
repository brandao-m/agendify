import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import SchedulePage from "./pages/SchedulePage";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>

    <BrowserRouter>

      <Routes>

        <Route path="/:slug" element={<SchedulePage />} />

      </Routes>

    </BrowserRouter>

  </React.StrictMode>
);