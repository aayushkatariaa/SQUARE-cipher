import Home from "./components/Home";
import Register from "./components/Register";
import Login from "./components/Login";
import React from "react";
import { AuthApi } from "./App"
import { Navigate } from "react-router-dom";
import {
  Routes,
  Route,
} from "react-router-dom";
const RoutesPage = () => {
  const Auth = React.useContext(AuthApi);
  return (
    <Routes>
      <Route path="/register" element={<Register />} />
      <Route
        path="/login"
        element={!Auth.auth ? <Login /> : <Navigate to="/" replace />}
      />
      <Route path="/" element={Auth.auth ? <Home /> : <Navigate to="/login" replace />} />
      {/* <Route path="/" element={<Home /> } /> */}
    </Routes>
  );
};

export default RoutesPage;