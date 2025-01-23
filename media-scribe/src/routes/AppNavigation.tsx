import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainLayout from "../layouts/MainLayout";
import Sessions from "../pages/Sessions";
import Knowledges from "../pages/Knowledges";
import Chat from "../pages/Chat";

function AppNavigation() {
  return (
    <BrowserRouter>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Sessions />} />
          <Route path="/*" element={<Sessions />} />
          <Route path="/Knowledges" element={<Knowledges />} />
          <Route path="/session/:sessionId" element={<Chat />} />
        </Routes>
      </MainLayout>
    </BrowserRouter>
  );
}

export default AppNavigation;
