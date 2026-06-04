import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api from "../services/api";

export default function PerguntasPadrao() {
  const [questions, setQuestions] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [erro, setErro] = useState("");
  const [info, setInfo] = useState("");
  const [syncing, setSyncing] = useState(false);

  const emptyForm = {
    text: "",
    question_type: "scale",
    order: "",
    is_active: true,
  };
  const [form, setForm] = useState(emptyForm);

  function loadQuestions() {
    api.get("evaluations/standard-questions/")
      .then((res) => setQuestions(Array.isArray(res.data) ? res.data : []))
      .catch(() => setErro("Erro ao carregar perguntas padrao."));
  }

  useEffect(() => {
    loadQuestions();
  }, []);

  function novaPergunta() {
    setEditingId(null);
    const nextOrder = questions.length
      ? Math.max(...questions.map((q) => q.order)) + 1
      : 1;
    setForm({ ...emptyForm, order: nextOrder });
    setErro("");
    setInfo("");
    setShowForm(true);
  }

  function editarPergunta(q) {
    setEditingId(q.id);
    setForm({
      text: q.text,
      question_type: q.question_type,
      order: q.order,
      is_active: q.is_active,
    });
    setErro("");
    setInfo("");
    setShowForm(true);
  }

  async function salvar(e) {
    e.preventDefault();
    setErro("");
    setInfo("");

    try {
      const payload = {
        text: form.text,
        question_type: form.question_type,
        order: Number(form.order),
        is_active: !!form.is_active,
      };

      if (editingId) {
        await api.patch(`evaluations/standard-questions/${editingId}/`, payload);
      } else {
        await api.post("evaluations/standard-questions/", payload);
      }

      setShowForm(false);
      setEditingId(null);
      setForm(emptyForm);
      loadQuestions();
    } catch (err) {
      const detail =
        err?.response?.data?.order?.[0] ||
        err?.response?.data?.text?.[0] ||
        err?.response?.data?.detail ||
        "Erro ao salvar pergunta. Verifique se a ordem nao esta duplicada.";
      setErro(detail);
    }
  }

  async function excluir(id) {
    if (!confirm(
      "Excluir esta pergunta padrao? Disciplinas que ja existem continuam " +
      "com a pergunta (a remocao so afeta novas disciplinas)."
    )) return;

    try {
      await api.delete(`evaluations/standard-questions/${id}/`);
      loadQuestions();
    } catch {
      setErro("Erro ao excluir pergunta.");
    }
  }

  async function aplicarEmTodas(overwrite) {
    const msg = overwrite
      ? "Isso vai atualizar TAMBEM o texto das perguntas existentes em todas as disciplinas. Confirmar?"
      : "Isso vai criar as perguntas faltantes em todas as disciplinas existentes (sem mexer nas que ja existem). Confirmar?";
    if (!confirm(msg)) return;

    setSyncing(true);
    setErro("");
    setInfo("");

    try {
      const url = overwrite
        ? "evaluations/standard-questions/sync/?overwrite=1"
        : "evaluations/standard-questions/sync/";
      const r = await api.post(url);
      setInfo(
        `Sincronizacao concluida. Disciplinas processadas: ${r.data.cursos_processados}. ` +
        `Perguntas criadas: ${r.data.perguntas_criadas}. ` +
        `Perguntas atualizadas: ${r.data.perguntas_atualizadas}.`
      );
    } catch {
      setErro("Erro ao sincronizar com as disciplinas existentes.");
    } finally {
      setSyncing(false);
    }
  }

  return (
    <Layout>
      <section className="page">
        <h1>Perguntas padrao</h1>

        <p style={{ marginTop: "-6px", color: "#555" }}>
          Estas perguntas sao usadas como base no formulario de toda disciplina nova.
          Editar ou excluir aqui <strong>nao</strong> altera disciplinas que ja foram
          cadastradas - para isso use o botao "Aplicar em todas as disciplinas".
        </p>

        {erro && <p style={{ color: "red", marginTop: 12 }}>{erro}</p>}
        {info && (
          <p style={{ color: "#1F4E5F", background: "#EAF3F7", padding: "10px 14px",
                       borderRadius: 6, marginTop: 12 }}>
            {info}
          </p>
        )}

        {!showForm && (
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginTop: 16 }}>
            <button className="primary-button" onClick={novaPergunta}>
              Nova pergunta
            </button>
            <button
              className="secondary-button"
              onClick={() => aplicarEmTodas(false)}
              disabled={syncing}
            >
              {syncing ? "Sincronizando..." : "Aplicar em todas as disciplinas"}
            </button>
            <button
              className="secondary-button"
              onClick={() => aplicarEmTodas(true)}
              disabled={syncing}
              title="Tambem atualiza o texto de perguntas existentes"
            >
              {syncing ? "Sincronizando..." : "Aplicar e sobrescrever textos"}
            </button>
          </div>
        )}

        {showForm ? (
          <form className="form-card large" onSubmit={salvar}>
            <h2>{editingId ? "Editar pergunta padrao" : "Nova pergunta padrao"}</h2>

            <label>Ordem (numero unico)</label>
            <input
              type="number"
              min="1"
              value={form.order}
              required
              onChange={(e) => setForm({ ...form, order: e.target.value })}
            />

            <label>Tipo</label>
            <select
              value={form.question_type}
              onChange={(e) => setForm({ ...form, question_type: e.target.value })}
            >
              <option value="scale">Escala (DT/DP/Neutro/CP/CT)</option>
              <option value="text">Texto livre (comentario aberto)</option>
            </select>

            <label>Texto da pergunta</label>
            <textarea
              rows={4}
              value={form.text}
              required
              onChange={(e) => setForm({ ...form, text: e.target.value })}
            />

            <label style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <input
                type="checkbox"
                checked={!!form.is_active}
                onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
              />
              Ativa (aparece em disciplinas novas)
            </label>

            <div className="form-actions">
              <button className="primary-button" type="submit">
                {editingId ? "Salvar alteracoes" : "Cadastrar"}
              </button>
              <button
                type="button"
                className="secondary-button"
                onClick={() => {
                  setShowForm(false);
                  setEditingId(null);
                  setForm(emptyForm);
                  setErro("");
                }}
              >
                Cancelar
              </button>
            </div>
          </form>
        ) : (
          <div className="list-box" style={{ marginTop: 16 }}>
            {questions.length === 0 && (
              <div className="list-row">Nenhuma pergunta padrao cadastrada.</div>
            )}

            {questions.map((q) => (
              <div key={q.id} className="course-row">
                <div style={{ flex: 1 }}>
                  <strong>
                    Q{q.order} - {q.question_type === "scale" ? "Escala" : "Texto"}
                    {!q.is_active && " (inativa)"}
                  </strong>
                  <small style={{ display: "block", marginTop: 4 }}>{q.text}</small>
                </div>
                <div className="row-actions">
                  <button className="secondary-button" onClick={() => editarPergunta(q)}>
                    Editar
                  </button>
                  <button className="trash-button" onClick={() => excluir(q.id)}>
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
