import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import AdminDashboard from "./pages/AdminDashboard";
import Professores from "./pages/Professores";
import Disciplinas from "./pages/Disciplinas";
import Relatorios from "./pages/Relatorios";
import ProfessorDashboard from "./pages/ProfessorDashboard";
import EvaluationForm from "./pages/EvaluationForm";
import SetPassword from "./pages/SetPassword";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";
import PerguntasPadrao from "./pages/PerguntasPadrao";

function PrivateRoute({ children }) {
  if (!localStorage.getItem("token")) {
    return <Navigate to="/" replace />;
  }
  // Se o usuário precisa trocar senha (primeiro login), não deixa acessar
  // outras telas até concluir a troca.
  try {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    if (user.must_change_password) {
      return <Navigate to="/trocar-senha" replace />;
    }
  } catch (e) {
    // ignore
  }
  return children;
}

function PasswordRoute({ children }) {
  return localStorage.getItem("token") ? children : <Navigate to="/" replace />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/esqueci-senha" element={<ForgotPassword />} />
        <Route path="/reset-password/:uid/:token" element={<ResetPassword />} />
        <Route path="/trocar-senha" element={<PasswordRoute><SetPassword /></PasswordRoute>} />
        <Route path="/admin" element={<PrivateRoute><AdminDashboard /></PrivateRoute>} />
        <Route path="/professores" element={<PrivateRoute><Professores /></PrivateRoute>} />
        <Route path="/disciplinas" element={<PrivateRoute><Disciplinas /></PrivateRoute>} />
        <Route path="/perguntas-padrao" element={<PrivateRoute><PerguntasPadrao /></PrivateRoute>} />
        <Route path="/relatorios" element={<PrivateRoute><Relatorios /></PrivateRoute>} />
        <Route path="/professor" element={<PrivateRoute><ProfessorDashboard /></PrivateRoute>} />
        <Route path="/formulario/:courseId" element={<EvaluationForm />} />
      </Routes>
    </BrowserRouter>
  );
}
export default App;
