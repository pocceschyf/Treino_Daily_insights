"""
Gera dados fictícios simulando 7 dias de dailies no Teams
com contexto de IA, dashboards e área de Pessoas (RH).
"""

import json, random
from datetime import datetime, timedelta

SPEAKERS = [
    "Fellipe Pocceschy",
    "Bruno Lopes",
    "Dayanne Oliveira",
    "Eduarda Lira",
    "Octavio Campanha"
]

BLOCKERS = [
    "Estou com dificuldade pra atualizar o dataset de pessoas no Databricks, tá dando conflito de schema.",
    "O dashboard no Power BI não está atualizando os dados de movimentação de colaboradores.",
    "Não consigo acessar o endpoint do nosso modelo de IA, está retornando erro de autenticação.",
    "O pipeline de ingestão de dados de RH falhou e não chegou na camada silver.",
    "Estou com problema para versionar o modelo de previsão de turnover no MLflow.",
    "Os dados de headcount estão inconsistentes entre os sistemas.",
    "Não entendi como agendar a atualização automática do relatório no Power BI.",
    "O notebook de preparação de dados está muito lento pra rodar no Databricks.",
]

QUESTIONS = [
    "Alguém sabe como versionar melhor modelos de IA no MLflow?",
    "Qual a melhor forma de atualizar dashboards automaticamente no Power BI?",
    "Tem como monitorar drift nos modelos de previsão de turnover?",
    "Como validar qualidade dos dados de pessoas antes de usar nos modelos?",
    "Tem alguma forma de otimizar consultas no Databricks?",
    "Como integrar um modelo de IA com uma API interna?",
    "Como controlar custo de execução dos pipelines de dados?",
    "Faz sentido aplicar cache para datasets de pessoas?",
    "Qual a melhor prática pra documentar dashboards?",
    "Como garantir consistência entre bases diferentes de RH?",
]

UPDATES = [
    "Ontem trabalhei na atualização do dashboard de headcount.",
    "Avancei na melhoria do modelo de previsão de turnover.",
    "Finalizei a ingestão dos dados de movimentação de colaboradores.",
    "Atualizei a documentação do pipeline de dados de pessoas.",
    "Revisei indicadores de desempenho do time no dashboard.",
]

# -------------------------
# GERAR REUNIÕES (DAILIES)
# -------------------------
meetings = []

for day in range(7):
    date_str = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%dT09:05:00Z")
    utterances = []

    for speaker in random.sample(SPEAKERS, 4):
        texto = random.choice(UPDATES)

        if random.random() > 0.4:
            texto += " " + random.choice(BLOCKERS)

        if random.random() > 0.5:
            texto += " " + random.choice(QUESTIONS)

        utterances.append({
            "speaker": speaker,
            "text": texto,
            "timestamp": date_str,
        })

    meetings.append({
        "meeting_id": f"meeting_dia_{day}",
        "subject": "Daily — Time de Dados & IA (Pessoas)",
        "start_time": date_str,
        "utterances": utterances,
        "source": "teams_meeting",
    })

# -------------------------
# GERAR MENSAGENS DE CANAL
# -------------------------
channel_messages = []

for i, q in enumerate(QUESTIONS):
    channel_messages.append({
        "message_id": f"msg_{i:03d}",
        "channel_id": "canal_dados_pessoas_ia",
        "speaker": random.choice(SPEAKERS),
        "text": q,
        "timestamp": (datetime.now() - timedelta(days=i)).isoformat(),
        "source": "teams_channel",
    })

# -------------------------
# SALVAR JSON
# -------------------------
data = {
    "meetings": meetings,
    "channel_messages": channel_messages
}

with open("mock_teams_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Mock criado!")
print(f"   {len(meetings)} reuniões diárias")
print(f"   {len(channel_messages)} mensagens de canal")
print("   Arquivo: mock_teams_data.json")