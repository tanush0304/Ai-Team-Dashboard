import { BrowserRouter, Routes, Route } from "react-router-dom";

import Layout from "./components/Layout";

import Home from "./pages/Home";
import TeamMembers from "./pages/TeamMembers";
import Projects from "./pages/Projects";
import DailyUpdates from "./pages/DailyUpdates";
import AIAssistant from "./pages/AIAssistant";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/team" element={<TeamMembers />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/updates" element={<DailyUpdates />} />
          <Route path="/ai" element={<AIAssistant />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;