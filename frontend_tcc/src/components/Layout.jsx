import Sidebar from "./Sidebar";

function resolveRole(propRole) {
  if (propRole) return propRole;
  try {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    if (user.role === "professor") return "Professor";
    if (user.role === "admin") return "Admin";
  } catch (e) {
    // ignore
  }
  return "Admin";
}

export default function Layout({ children, role, userName = "" }) {
  const finalRole = resolveRole(role);
  let displayName = userName;
  if (!displayName) {
    try {
      const user = JSON.parse(localStorage.getItem("user") || "{}");
      displayName = user.full_name || user.institutional_email || "";
    } catch (e) {
      // ignore
    }
  }
  return (
    <div className="app-shell">
      <Sidebar role={finalRole} />
      <main className="main-content">
        <header className="topbar">{displayName || "Sistema de Avaliação"}</header>
        {children}
      </main>
    </div>
  );
}
