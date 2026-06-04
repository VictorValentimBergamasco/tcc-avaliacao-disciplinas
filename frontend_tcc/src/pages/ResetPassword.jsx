import { useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../services/api";

export default function ResetPassword() {
  const { uid, token } = useParams();
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (newPassword.length < 6) {
      setError("A nova senha deve ter pelo menos 6 caracteres.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError("As senhas nao coincidem.");
      return;
    }

    setLoading(true);
    try {
      await api.post("users/password-reset/confirm/", {
        uid,
        token,
        new_password: newPassword,
      });
      setSuccess(true);
    } catch (err) {
      const detail =
        err?.response?.data?.detail ||
        err?.response?.data?.new_password?.[0] ||
        "Link invalido ou expirado. Solicite um novo.";
      setError(detail);
    } finally {
      setLoading(false);
    }
  }

  if (success) {
    return (
      <div className="login-page">
        <div className="login-card">
          <h1>Senha redefinida</h1>
          <p style={{ marginTop: 8 }}>
            Sua senha foi atualizada com sucesso. Ja pode entrar normalmente.
          </p>
          <p style={{ marginTop: 16, textAlign: "center" }}>
            <Link to="/">Ir para o login</Link>
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>Definir nova senha</h1>

        {error && <div className="login-error">{error}</div>}

        <label>Nova senha</label>
        <input
          type="password"
          value={newPassword}
          onChange={(e) => setNewPassword(e.target.value)}
          required
          minLength={6}
        />

        <label>Confirmar nova senha</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          required
          minLength={6}
        />

        <button type="submit" disabled={loading}>
          {loading ? "Salvando..." : "Salvar nova senha"}
        </button>

        <small>
          <Link to="/">Voltar para o login</Link>
        </small>
      </form>
    </div>
  );
}
