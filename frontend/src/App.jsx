import { useState, useEffect } from "react"

const API = import.meta.env.VITE_API_URL || "http://localhost:8000"

const SEVERITY_COLOR = {
  alta:   { bg: "#fff1f0", border: "#ff4d4f", text: "#cf1322" },
  media:  { bg: "#fffbe6", border: "#faad14", text: "#ad6800" },
  baixa:  { bg: "#f6ffed", border: "#52c41a", text: "#389e0d" },
}

export default function App() {
  const [pains, setPains]         = useState([])
  const [questions, setQuestions] = useState([])
  const [participation, setParticipation] = useState([])
  const [loading, setLoading]     = useState(true)
  const [aba, setAba]             = useState("dores")

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/pains`).then(r => r.json()),
      fetch(`${API}/api/questions`).then(r => r.json()),
      fetch(`${API}/api/participation`).then(r => r.json()),
    ]).then(([p, q, part]) => {
      setPains(p.data || [])
      setQuestions(q.data || [])
      setParticipation(part.data || [])
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  if (loading) return (
    <div style={styles.center}>
      <p style={{color:"#888"}}>Carregando dados...</p>
    </div>
  )

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1 style={styles.title}>⚡ Daily Insights</h1>
        <p style={styles.subtitle}>Dores e dúvidas identificadas nas dailies do time</p>
      </header>

      <div style={styles.tabs}>
        {["dores","perguntas","participacao"].map(t => (
          <button key={t} style={{...styles.tab, ...(aba===t ? styles.tabActive : {})}}
            onClick={() => setAba(t)}>
            {t === "dores" ? "🔴 Dores" : t === "perguntas" ? "❓ Perguntas" : "👥 Participação"}
          </button>
        ))}
      </div>

      <main style={styles.main}>
        {aba === "dores" && (
          <div>
            {pains.length === 0
              ? <p style={styles.empty}>Nenhuma dor identificada. Rode o pipeline primeiro.</p>
              : pains.map((p, i) => {
                  const cor = SEVERITY_COLOR[p.severity] || SEVERITY_COLOR.baixa
                  return (
                    <div key={i} style={{...styles.card, borderLeft: `4px solid ${cor.border}`}}>
                      <div style={styles.cardTop}>
                        <span style={{...styles.badge, background: cor.bg, color: cor.text}}>
                          {p.severity?.toUpperCase()}
                        </span>
                        <span style={styles.category}>{p.category}</span>
                      </div>
                      <p style={styles.cardDesc}>{p.description}</p>
                      <div style={styles.cardFooter}>
                        <span style={styles.speaker}>👤 {p.speaker}</span>
                        <span style={styles.topic}>📚 {p.suggested_topic}</span>
                      </div>
                    </div>
                  )
                })
            }
          </div>
        )}

        {aba === "perguntas" && (
          <div>
            {questions.length === 0
              ? <p style={styles.empty}>Nenhuma pergunta detectada.</p>
              : questions.map((q, i) => (
                <div key={i} style={styles.card}>
                  <p style={styles.cardDesc}>{q}</p>
                </div>
              ))
            }
          </div>
        )}

        {aba === "participacao" && (
          <div>
            {participation.map((p, i) => (
              <div key={i} style={{...styles.card, display:"flex", alignItems:"center", gap:"1rem"}}>
                <div style={styles.avatar}>{p.speaker?.charAt(0)}</div>
                <div>
                  <strong style={{color:"#1a1a2e"}}>{p.speaker}</strong>
                  <p style={{fontSize:"13px",color:"#666",margin:0}}>{p.utterances} falas registradas</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  )
}

const styles = {
  app:        { maxWidth: 720, margin: "0 auto", padding: "1.5rem", fontFamily: "system-ui, sans-serif" },
  center:     { display:"flex", justifyContent:"center", alignItems:"center", height:"100vh" },
  header:     { marginBottom: "1.5rem" },
  title:      { fontSize: 26, fontWeight: 700, margin: 0, color: "#1a1a2e" },
  subtitle:   { fontSize: 14, color: "#888", margin: "4px 0 0" },
  tabs:       { display:"flex", gap:8, marginBottom:"1.5rem" },
  tab:        { padding:"8px 18px", borderRadius:8, border:"1px solid #e0e0e0", background:"#fafafa", cursor:"pointer", fontSize:13, fontWeight:500, color:"#555" },
  tabActive:  { background:"#6c63ff", color:"#fff", border:"1px solid #6c63ff" },
  main:       { },
  card:       { background:"#fff", border:"1px solid #eee", borderRadius:10, padding:"1rem 1.25rem", marginBottom:"1rem", boxShadow:"0 1px 3px rgba(0,0,0,0.06)" },
  cardTop:    { display:"flex", alignItems:"center", gap:8, marginBottom:8 },
  badge:      { padding:"2px 10px", borderRadius:99, fontSize:11, fontWeight:700 },
  category:   { fontSize:12, color:"#888", background:"#f5f5f5", padding:"2px 8px", borderRadius:4 },
  cardDesc:   { fontSize:14, color:"#333", margin:0, lineHeight:1.6 },
  cardFooter: { display:"flex", gap:16, marginTop:10, flexWrap:"wrap" },
  speaker:    { fontSize:12, color:"#666" },
  topic:      { fontSize:12, color:"#6c63ff", fontWeight:500 },
  avatar:     { width:40, height:40, borderRadius:"50%", background:"#6c63ff", color:"#fff", display:"flex", alignItems:"center", justifyContent:"center", fontWeight:700, fontSize:18, flexShrink:0 },
  empty:      { color:"#888", textAlign:"center", padding:"2rem" },
}