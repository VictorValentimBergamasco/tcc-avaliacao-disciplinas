import { Link, useLocation } from "react-router-dom";

export default function Sidebar({ role = "Admin" }) {
  const location = useLocation();
  const links = role === "Professor"
    ? [{ path: "/professor", label: "Disciplinas", icon: "▧" }, { path: "/relatorios", label: "Relatórios", icon: "▤" }]
    : [
        { path: "/admin", label: "Início", icon: "⌂" },
        { path: "/professores", label: "Professores", icon: "♟" },
        { path: "/disciplinas", label: "Disciplinas", icon: "☷" },
        { path: "/perguntas-padrao", label: "Perguntas padrão", icon: "?" },
        { path: "/relatorios", label: "Relatórios", icon: "▤" },
      ];
  function logout() { localStorage.clear(); window.location.href = "/"; }
  return <aside className="sidebar"><div className="sidebar-title">{role}</div><nav className="sidebar-nav">{links.map(l => <Link key={l.path} className={location.pathname===l.path ? "sidebar-link active" : "sidebar-link"} to={l.path}><span>{l.icon}</span>{l.label}</Link>)}</nav><button className="logout-button" onClick={logout}>Sair</button></aside>;
}
