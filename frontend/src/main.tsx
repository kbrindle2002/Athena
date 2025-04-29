import React from "react";
import ReactDOM from "react-dom/client";

const App = () => (
  <div className="flex h-screen items-center justify-center">
    <h1 className="text-4xl font-semibold text-blue-700">ATHENA Frontend Works!</h1>
  </div>
);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(<App />);
