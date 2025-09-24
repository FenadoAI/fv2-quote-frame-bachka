import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import QuoteGenerator from "./components/QuoteGenerator";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<QuoteGenerator />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
