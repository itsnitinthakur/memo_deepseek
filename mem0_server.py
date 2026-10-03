from fastapi import FastAPI, Request
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {"collection_name": "nitin_memory", "path": "./mem0_db"}
    },
    "llm": {
        "provider": "ollama",
        "config": {"model": "deepseek-coder-v2:16b", "ollama_base_url": "http://localhost:11434"}
    },
    "embedder": {
        "provider": "ollama",
        "config": {"model": "nomic-embed-text", "ollama_base_url": "http://localhost:11434"}
    }
}
m = Memory.from_config(config)
app = FastAPI()
USER_ID = "nitin"

# Continue.dev calls this one — it expects back {name, description, content}
@app.post("/")
async def continue_context(request: Request):
    body = await request.json()
    query = body.get("query") or body.get("fullInput", "")
    results = m.search(query=query, user_id=USER_ID, limit=5)
    memories = [r["memory"] for r in results.get("results", [])]
    content = "\n".join(f"- {mem}" for mem in memories) or "No relevant past context found."
    return {"name": "Memory", "description": "Relevant context from past sessions", "content": content}

# Aider's wrapper script calls these two
@app.post("/search")
async def search(request: Request):
    body = await request.json()
    results = m.search(query=body.get("query", ""), user_id=USER_ID, limit=5)
    return {"memories": [r["memory"] for r in results.get("results", [])]}

@app.post("/add")
async def add(request: Request):
    body = await request.json()
    m.add([{"role": "user", "content": body.get("text", "")}], user_id=USER_ID)
    return {"status": "ok"}