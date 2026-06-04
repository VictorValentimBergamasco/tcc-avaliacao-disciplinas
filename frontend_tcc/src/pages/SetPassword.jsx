import { useState, useEffect } from "react";
import api from "../services/api";

export default function SetPassword() {
  const [user, setUser] = useState({});
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    try {
      setUser(JSON.parse(localStorage.getItem("user") || "{}"));
    } catch (e) {
      setUser({});
    }
  }, []);

  const isFirstLogin = !!user.must_change_password;

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (newPassword.length < 6) {
      setError("A nova senha deve ter pelo menos 6 caracteres.");
      return;
    }
    if (newPassword !== confirmPassword) {
      setError("As senhas não coincidem.");
      return;
    }

    setLoading(true);
    try {
      const payload = { new_password: newPassword };
      if (!isFirstLogin) {
        payload.current_password = currentPassword;
      }

      await api.post("users/me/change-password/", payload);

      // Recarrega o usuário para atualizar o must_change_password no localStorage.
      try {
        const me = await api.get("users/me/");
        localStorage.setItem("user", JSON.stringify(me.data));
        window.location.href = me.data.role === "professor" ? "/professor" : "/admin";
      } catch (err) {
        window.location.href = "/";
      }
    } catch (err) {
      const detail = err?.response?.data?.detail
        || err?.response?.data?.new_password?.[0]
        || "Não foi possível alterar a senha. Tente novamente.";
      setError(detail);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={handleSubmit}>
        <h1>{isFirstLogin ? "Defina sua senha" : "Trocar senha"}</h1>

        {isFirstLogin && (
          <p style={{ fontSize: "0.9rem", color: "#444", marginBottom: "8px" }}>
            Olá, {user.first_name || user.institutional_email}! Este é o seu
            primeiro acesso. Por segurança, defina uma nova senha pessoal antes
            de continuar.
          </p>
        )}

        {error && <div className="login-error">{error}</div>}

        {!isFirstLogin && (
          <>
            <label>Senha atual</label>
            <input
              type="password"
              value={currentPassword}
              onChange={(e) => setCurrentPassword(e.target.value)}
              required
            />
          </>
        )}

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
      </form>
    </div>
  );
}
