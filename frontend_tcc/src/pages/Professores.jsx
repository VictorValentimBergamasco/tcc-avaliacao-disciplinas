import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../services/api";

export default function Professores() {
  const [professores, setProfessores] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [erro, setErro] = useState("");

  const emptyForm = {
    first_name: "",
    last_name: "",
    institutional_email: "",
    password: "123456",
    role: "professor",
  };

  const [form, setForm] = useState(emptyForm);

  function loadProfessores() {
    api.get("users/professores/")
      .then((res) => setProfessores(Array.isArray(res.data) ? res.data : []))
      .catch(() => setErro("Erro ao carregar professores."));
  }

  useEffect(() => {
    loadProfessores();
  }, []);

  function novoProfessor() {
    setEditingId(null);
    setForm(emptyForm);
    setShowForm(true);
  }

  function editarProfessor(prof) {
    setEditingId(prof.id);
    setForm({
      first_name: prof.first_name || "",
      last_name: prof.last_name || "",
      institutional_email: prof.institutional_email || "",
      password: "",
      role: "professor",
    });
    setShowForm(true);
  }

  async function salvar(e) {
    e.preventDefault();
    setErro("");

    try {
      const payload = { ...form };

      if (!payload.password) {
        delete payload.password;
      }

      if (editingId) {
        await api.patch(`users/professores/${editingId}/`, payload);
      } else {
        await api.post("users/professores/", payload);
      }

      setForm(emptyForm);
      setEditingId(null);
      setShowForm(false);
      loadProfessores();
    } catch (err) {
      console.error(err);
      setErro("Erro ao salvar professor.");
    }
  }

  async function excluir(id) {
    if (!confirm("Deseja excluir este professor?")) return;

    try {
      await api.delete(`users/professores/${id}/`);
      loadProfessores();
    } catch (err) {
      console.error(err);
      setErro("Erro ao excluir professor. Verifique se ele possui disciplinas vinculadas.");
    }
  }

  return (
    <Layout role="Admin">
      <section className="page">
        <h1>Professores</h1>

        {erro && <p style={{ color: "red" }}>{erro}</p>}

        {!showForm && (
          <button className="primary-button" onClick={novoProfessor}>
            Cadastrar professor
          </button>
        )}

        {showForm ? (
          <form className="form-card" onSubmit={salvar}>
            <h2>{editingId ? "Editar Professor" : "Cadastrar Professor"}</h2>

            <input
              placeholder="Nome"
              value={form.first_name}
              required
              onChange={(e) => setForm({ ...form, first_name: e.target.value })}
            />

            <input
              placeholder="Sobrenome"
              value={form.last_name}
              required
              onChange={(e) => setForm({ ...form, last_name: e.target.value })}
            />

            <input
              placeholder="Email institucional"
              value={form.institutional_email}
              required
              onChange={(e) => setForm({ ...form, institutional_email: e.target.value })}
            />

            <input
              placeholder={editingId ? "Nova senha provisória (opcional)" : "Senha provisória"}
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
            <small style={{ color: "#666", marginTop: "-4px" }}>
              O professor será obrigado a trocar essa senha no primeiro login.
            </small>

            <div className="form-actions">
              <button className="primary-button">
                {editingId ? "Salvar alterações" : "Cadastrar"}
              </button>

              <button
                type="button"
                className="secondary-button"
                onClick={() => {
                  setShowForm(false);
                  setEditingId(null);
                  setForm(emptyForm);
                }}
              >
                Cancelar
              </button>
            </div>
          </form>
        ) : (
          <div className="list-box">
            {professores.map((prof) => (
              <div key={prof.id} className="course-row">
                <div>
                  <strong>{prof.full_name || `${prof.first_name} ${prof.last_name}`}</strong>
                  <small>{prof.institutional_email}</small>
                </div>

                <div className="row-actions">
                  <button className="secondary-button" onClick={() => editarProfessor(prof)}>
                    Editar
                  </button>

                  <button className="trash-button" onClick={() => excluir(prof.id)}>
                    🗑
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </Layout>
  );
}