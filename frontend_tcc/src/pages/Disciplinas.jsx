import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import api, { getMediaUrl } from "../services/api";

export default function Disciplinas() {
  const [courses, setCourses] = useState([]);
  const [professores, setProfessores] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [erro, setErro] = useState("");

  // As 24 perguntas padrao da FT-UNICAMP sao criadas automaticamente pelo
  // backend assim que uma disciplina e cadastrada (ver Course.save() e
  // apps/evaluations/standard_questions.py). Nao e mais necessario enviar
  // do frontend.

  const [form, setForm] = useState({
    name: "",
    code: "",
    professor: "",
    enrollment_count: 0,
  });

  function load() {
    api.get("courses/")
      .then((res) => setCourses(Array.isArray(res.data) ? res.data : []))
      .catch((err) => {
        console.error(err);
        setErro("Erro ao carregar disciplinas.");
      });

    api.get("users/professores/")
      .then((res) => setProfessores(Array.isArray(res.data) ? res.data : []))
      .catch((err) => {
        console.error(err);
        setErro("Erro ao carregar professores.");
      });
  }

  useEffect(() => {
    load();
  }, []);

  async function cadastrar(e) {
    e.preventDefault();
    setErro("");

    try {
      const payloadInicial = {
        name: form.name,
        code: form.code,
        professor: Number(form.professor),
        enrollment_count: Number(form.enrollment_count || 0),
        google_form_link: "http://localhost:5173/formulario/0",
      };

      const response = await api.post("courses/", payloadInicial);

      const courseId = response.data.id;
      const linkFormulario = `http://localhost:5173/formulario/${courseId}`;

      // Atualiza o link do formulario (e o QR Code do backend regenera).
      // As 24 perguntas padrao foram criadas automaticamente no save() do Course.
      await api.patch(`courses/${courseId}/`, {
        google_form_link: linkFormulario,
      });

      setForm({
        name: "",
        code: "",
        professor: "",
        enrollment_count: 0,
      });

      setShowForm(false);
      load();
    } catch (err) {
      console.error(err);
      setErro("Erro ao cadastrar disciplina. Verifique se todos os campos foram preenchidos.");
    }
  }

  async function excluir(id) {
    if (!confirm("Deseja excluir esta disciplina?")) return;

    try {
      await api.delete(`courses/${id}/`);
      load();
    } catch (err) {
      console.error(err);
      setErro("Erro ao excluir disciplina.");
    }
  }

  return (
    <Layout role="Admin">
      <section className="page">
        <h1>Disciplinas</h1>

        {erro && <p style={{ color: "red" }}>{erro}</p>}

        {!showForm && (
          <button className="primary-button" onClick={() => setShowForm(true)}>
            Cadastrar disciplina
          </button>
        )}

        {showForm ? (
          <form className="form-card large" onSubmit={cadastrar}>
            <h2>Cadastrar Disciplina</h2>

            <input
              placeholder="Nome"
              value={form.name}
              required
              onChange={(e) => setForm({ ...form, name: e.target.value })}
            />

            <input
              placeholder="Código"
              value={form.code}
              required
              onChange={(e) => setForm({ ...form, code: e.target.value })}
            />

            <select
              value={form.professor}
              required
              onChange={(e) => setForm({ ...form, professor: e.target.value })}
            >
              <option value="">Selecione o professor responsável</option>
              {professores.map((p) => (
                <option key={p.id} value={p.id}>
                  {p.full_name || `${p.first_name} ${p.last_name}`} - {p.institutional_email}
                </option>
              ))}
            </select>

            <input
              type="number"
              placeholder="Número de matriculados"
              value={form.enrollment_count}
              min="0"
              required
              onChange={(e) => setForm({ ...form, enrollment_count: e.target.value })}
            />

            <div className="form-actions">
              <button className="primary-button" type="submit">
                Cadastrar
              </button>

              <button
                type="button"
                className="secondary-button"
                onClick={() => setShowForm(false)}
              >
                Cancelar
              </button>
            </div>
          </form>
        ) : (
          <div className="list-box">
            {courses.length === 0 && (
              <div className="list-row">
                Nenhuma disciplina cadastrada.
              </div>
            )}

            {courses.map((course) => (
              <div key={course.id} className="course-row">
                <div>
                  <strong>{course.name}</strong>
                  <small>
                    {course.code} • {course.professor_name}
                  </small>
                  <small>
                    Formulário: http://localhost:5173/formulario/{course.id}
                  </small>
                </div>

                <div className="row-actions">
                  <a
                    href={`http://localhost:5173/formulario/${course.id}`}
                    target="_blank"
                    rel="noreferrer"
                  >
                    Formulário
                  </a>

                  {course.qr_code_url && (
                    <a
                      href={getMediaUrl(course.qr_code_url)}
                      target="_blank"
                      rel="noreferrer"
                    >
                      QR Code
                    </a>
                  )}

                  <button
                    onClick={() => excluir(course.id)}
                    className="trash-button"
                  >
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