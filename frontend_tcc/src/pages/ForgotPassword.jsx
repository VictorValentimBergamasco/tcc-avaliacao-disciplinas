import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../services/api";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await api.post("users/password-reset/", { institutional_email: email });
      setSent(true);
    } catch {
      setError("Nao foi possivel processar a solicitacao. Tente novamente.");
    } finally {
      setLoading(false);
    }
  }

  if (sent) {
    return (
      <div className="login-page">
        <div className="login-card">
          <h1>Verifique seu e-mail</h1>
          <p style={{ marginTop: 8 }}>
            Se o e-mail informado estiver cadastrado, enviamos um link para
            redefinir sua senha. Verifique tambem a pasta de spam.
          </p>
          <p style={{ marginTop: 16, textAlign: "center" }}>
            <Link to="/">Voltar para o login</Link>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>Recuperar senha</h1>
        <p style={{ marginTop: 4, color: "#555", fontSize: "0.92rem" }}>
          Informe seu e-mail institucional. Vamos enviar um link para voce criar
          uma nova senha.
        </p>

        {error && <div className="login-error">{error}</div>}

        <label>E-mail institucional</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? "Enviando..." : "Enviar link"}
        </button>

        <small>
          <Link to="/">Voltar para o login</Link>
        </small>
      </form>
    </div>
  );
}
