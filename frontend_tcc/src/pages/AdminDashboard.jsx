import { useEffect, useState } from "react";
import Layout from "../components/Layout";
import StatCard from "../components/StatCard";
import api from "../services/api";
export default function AdminDashboard(){
  const [o,setO]=useState({total_courses:0,total_professors:0,total_responses:0});
  useEffect(()=>{api.get("dashboard/overview/").then(res=>setO({total_courses:res.data.total_courses??res.data.total_disciplinas??0,total_professors:res.data.total_professors??res.data.total_professores??0,total_responses:res.data.total_responses??res.data.total_respostas??0})).catch(console.error)},[]);
  return <Layout role="Admin"><section className="page"><h1>Início</h1><h2>Visão geral</h2><div className="stats-grid"><StatCard number={o.total_professors} label="Professores registrados"/><StatCard number={o.total_courses} label="Disciplinas"/><StatCard number={o.total_responses} label="Respostas"/></div></section></Layout>;
}
