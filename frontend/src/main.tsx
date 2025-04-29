// frontend/src/main.tsx
import React from "react";
import ReactDOM from "react-dom/client";
import UsersPage from "./UsersPage";   //  ←  this line must exist

ReactDOM.createRoot(document.getElementById("root")!)
        .render(<UsersPage />);
