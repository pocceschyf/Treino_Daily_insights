"""
API FastAPI local — serve os dados do pipeline para o frontend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json, os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Daily Insights API")

# Libera o frontend para acessar a API (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT = Path("output")

def ler(arquivo):
    """Lê um arquivo JSON de output. Retorna [] se não existir."""
    caminho = OUTPUT / arquivo
    if not caminho.exists():
        return []
    with open(caminho, encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
def raiz():
    return {
        "status": "ok",
        "mensagem": "Daily Insights API rodando!",
        "endpoints": ["/api/pains", "/api/questions", "/api/participation", "/api/gold"]
    }


@app.get("/api/pains")
def dores():
    """Retorna as dores identificadas pelo LLM."""
    return {"data": ler("pains.json")}


@app.get("/api/questions")
def perguntas():
    """Retorna as perguntas mais frequentes."""
    gold = ler("gold.json")
    return {"data": gold.get("top_questions", []) if gold else []}


@app.get("/api/participation")
def participacao():
    """Retorna dados de participação do time."""
    gold = ler("gold.json")
    return {"data": gold.get("participation", []) if gold else []}


@app.get("/api/gold")
def gold_completo():
    """Retorna todos os dados agregados."""
    return {"data": ler("gold.json")}


if __name__ == "__main__":
    import uvicorn
    porta = int(os.getenv("API_PORT", 8000))
    print(f"\nAPI rodando em: http://localhost:{porta}")
    print(f"Documentação:   http://localhost:{porta}/docs\n")
    uvicorn.run(app, host="0.0.0.0", port=porta)