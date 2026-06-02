"""
Pipeline local: Bronze → Silver → Gold → LLM
Lê mock_teams_data.json e gera os arquivos em output/
"""
import json, re, os
from dotenv import load_dotenv
load_dotenv()


# ── BRONZE: carrega os dados brutos ──────────────────────────────
def bronze():
    with open("mock_teams_data.json", encoding="utf-8") as f:
        data = json.load(f)

    records = []
    # Reuniões
    for meeting in data["meetings"]:
        for utt in meeting["utterances"]:
            records.append({
                "meeting_id": meeting["meeting_id"],
                "subject":    meeting["subject"],
                "speaker":    utt["speaker"],
                "text":       utt["text"],
                "timestamp":  utt["timestamp"],
                "source":     "teams_meeting",
            })
    # Mensagens de canal
    for msg in data["channel_messages"]:
        records.append({
            "meeting_id": None,
            "subject":    None,
            "speaker":    msg["speaker"],
            "text":       msg["text"],
            "timestamp":  msg["timestamp"],
            "source":     "teams_channel",
        })

    print(f"[Bronze] {len(records)} registros carregados")
    return records


# ── SILVER: limpa e enriquece ─────────────────────────────────────
def silver(records):
    def limpar(t):
        t = re.sub(r'http\S+', '', t)        # remove URLs
        t = re.sub(r'<[^>]+>', '', t)        # remove HTML
        return re.sub(r'\s+', ' ', t).strip()

    def eh_pergunta(t):
        return any(k in t.lower() for k in [
            "?", "como ", "qual ", "alguém sabe",
            "não consigo", "dúvida", "tem como", "help"
        ])

    def eh_blocker(t):
        return any(k in t.lower() for k in [
            "travad", "bloqueado", "não consigo", "erro",
            "falhou", "quebrou", "blocker", "exception"
        ])

    resultado = []
    for r in records:
        texto = limpar(r["text"])
        palavras = len(texto.split())
        if palavras < 4:          # ignora textos muito curtos
            continue
        resultado.append({
            **r,
            "text_clean":  texto,
            "word_count":  palavras,
            "is_question": eh_pergunta(texto),
            "has_blocker": eh_blocker(texto),
        })

    perguntas = sum(1 for r in resultado if r["is_question"])
    blockers  = sum(1 for r in resultado if r["has_blocker"])
    print(f"[Silver] {len(resultado)} registros | {perguntas} perguntas | {blockers} blockers")
    return resultado


# ── GOLD: agrega métricas ─────────────────────────────────────────
def gold(silver_data):
    from collections import Counter

    perguntas   = [r["text_clean"] for r in silver_data if r["is_question"]]
    blockers    = [r for r in silver_data if r["has_blocker"]]
    participacao = Counter(r["speaker"] for r in silver_data)

    resultado = {
        "top_questions": perguntas[:10],
        "blockers": [
            {"speaker": r["speaker"], "text": r["text_clean"]}
            for r in blockers[:10]
        ],
        "participation": [
            {"speaker": s, "utterances": c}
            for s, c in participacao.most_common()
        ],
    }
    print(f"[Gold] {len(perguntas)} perguntas | {len(blockers)} blockers detectados")
    return resultado


# ── LLM: identifica dores com Groq ───────────────────────────────
def analisar_com_llm(silver_data):
    import os
    import json
    from groq import Groq

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("[LLM] GROQ_API_KEY não configurada — pulando análise")
        return []

    client = Groq(api_key=api_key)

    relevantes = [
        r for r in silver_data
        if r["is_question"] or r["has_blocker"]
    ][:20]

    if not relevantes:
        print("[LLM] Sem dados relevantes")
        return []

    falas = "\n".join([
        f"[{r['speaker']}]: {r['text_clean']}"
        for r in relevantes
    ])

    prompt = f"""
Analise falas de um time de Dados & IA da área de Pessoas.

Responda apenas JSON:
{{
  "pains": [
    {{
      "category": "dados|ia|dashboard|processo|infraestrutura",
      "description": "descrição",
      "severity": "alta|media|baixa",
      "speaker": "nome ou multiplas_pessoas",
      "suggested_topic": "tema"
    }}
  ]
}}


FALAS:
{falas}
"""

    print(">>> USANDO MODELO NOVO <<<")

    resposta = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500,
    )

    texto = resposta.choices[0].message.content

    try:
        resultado = json.loads(texto)
        dores = resultado.get("pains", [])
        print(f"[LLM] {len(dores)} dores identificadas")
        return dores
    except Exception:
        print("[LLM] Erro ao parsear resposta")
        print(texto)
        return []


# ── EXECUÇÃO ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== PIPELINE Daily Insights ===\n")

    dados_bronze = bronze()
    dados_silver = silver(dados_bronze)
    dados_gold   = gold(dados_silver)
    dores        = analisar_com_llm(dados_silver)

    # Salva os resultados
    os.makedirs("output", exist_ok=True)
    with open("output/silver.json", "w", encoding="utf-8") as f:
        json.dump(dados_silver, f, ensure_ascii=False, indent=2)
    with open("output/gold.json", "w", encoding="utf-8") as f:
        json.dump(dados_gold, f, ensure_ascii=False, indent=2)
    with open("output/pains.json", "w", encoding="utf-8") as f:
        json.dump(dores, f, ensure_ascii=False, indent=2)

    # Mostra resumo
    print("\n=== RESULTADOS ===\n")
    print("Top perguntas detectadas:")
    for q in dados_gold["top_questions"][:5]:
        print(f"  - {q[:80]}")

    print("\nBlockers identificados:")
    for b in dados_gold["blockers"][:3]:
        print(f"  [{b['speaker']}] {b['text'][:80]}")

    if dores:
        print("\nDores identificadas pelo LLM:")
        for d in dores[:3]:
            print(f"  [{d['severity'].upper()}] {d['description'][:80]}")
            print(f"  → Treinamento: {d['suggested_topic']}")

    print("\n✅ Arquivos salvos em output/")