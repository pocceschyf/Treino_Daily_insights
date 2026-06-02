
# 📊 Daily Insights AI

### Plataforma de análise de dailies com IA para identificação de dores e oportunidades do time

---

## 🧭 Contexto

Times de dados e tecnologia frequentemente enfrentam desafios na identificação estruturada de:

- Dúvidas recorrentes
- Bloqueios operacionais
- Gargalos em processos e ferramentas
- Necessidades de capacitação

Essas informações estão presentes nas dailies, porém de forma **não estruturada e difícil de escalar**.

O **Daily Insights AI** transforma essas interações em **insights acionáveis**, combinando engenharia de dados e inteligência artificial.

---

## 🎯 Objetivo

Automatizar a análise de interações do time para:

- Identificar padrões de dor
- Mapear gaps de conhecimento
- Apoiar decisões em People Analytics
- Priorizar melhorias operacionais

---

## 🧠 Principais Funcionalidades

- 📥 Processamento de dados (Bronze → Silver → Gold)
- 🔎 Detecção de perguntas e blockers
- 🤖 Análise de dores com LLM
- 🌐 API REST com FastAPI
- 📊 Dashboard em React

---

## 🏗️ Arquitetura

```
Dados
  ↓
Bronze
  ↓
Silver
  ↓
Gold
  ↓
LLM
  ↓
API
  ↓
Frontend
```

---

## 🛠️ Tecnologias

- Python
- FastAPI
- React + Vite
- Groq (LLM)

---

## ⚙️ Como rodar

### Backend

```bash
python scripts/criar_mock.py
python scripts/pipeline.py
python api/main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 🔐 Configuração

### .env

```env
GROQ_API_KEY=your_key
```

### frontend/.env

```env
VITE_API_URL=http://localhost:8000
```

---

## 📈 Aplicações

- People Analytics
- Gestão de times de dados
- Monitoramento de produtividade

---

## 🎯 Considerações

Projeto focado em demonstrar aplicação prática de dados, IA e produto em contexto corporativo.

---

## 👤 Autor

Desenvolvido como estudo aplicado de engenharia de dados e IA.
