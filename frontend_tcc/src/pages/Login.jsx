import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    setError("");
    try {
      const r = await api.post("auth/login/", {
        institutional_email: email,
        password,
      });
      localStorage.setItem("token", r.data.access);
      try {
        const me = await api.get("users/me/");
        localStorage.setItem("user", JSON.stringify(me.data));

        // Primeiro acesso (ou senha resetada pelo admin): obrigar a trocar senha.
        if (me.data.must_change_password) {
          window.location.href = "/trocar-senha";
          return;
        }

        window.location.href =
          me.data.role === "professor" ? "/professor" : "/admin";
      } catch {
        window.location.href = "/admin";
      }
    } catch {
      setError("Email ou senha inválida");
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleLogin}>
        <h1>LOGIN</h1>
        {error && <div className="login-error">{error}</div>}
        <label>Email</label>
        <input value={email} onChange={(e) => setEmail(e.target.value)} />
        <label>Senha</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button>Entrar</button>
        <small>
          <Link to="/esqueci-senha">Esqueceu sua senha?</Link>
        </small>
      </form>
    </div>
  );
}
