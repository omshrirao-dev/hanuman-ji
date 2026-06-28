import { HashRouter, Route, Routes } from "react-router-dom";
import Landing from "./pages/Landing";
import Chat from "./pages/Chat";
import About from "./pages/About";

function App() {
  return (
    <HashRouter>
      <div className="om-watermark font-devanagari">ॐ</div>
      <div className="relative z-10 min-h-screen">
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </HashRouter>
  );
}

export default App;
