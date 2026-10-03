from mem0 import Memory
import ollama

config = {
    "vector_store": {
        "provider": "chroma",
        "config": {
            "collection_name": "nitin_memory",
            "path": "./mem0_db"   # stored locally, no server needed
        }
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "deepseek-coder-v2:16b",
            "ollama_base_url": "http://localhost:11434"
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": "http://localhost:11434"
        }
    }
}

m = Memory.from_config(config)
user_id = "nitin"

def chat(user_input):
    found = m.search(query=user_input, user_id=user_id, limit=5)
    context = "\n".join(r["memory"] for r in found.get("results", []))

    prompt = f"Relevant context from past conversations:\n{context}\n\nUser: {user_input}"
    response = ollama.chat(model="deepseek-coder-v2:16b", messages=[{"role": "user", "content": prompt}])
    reply = response["message"]["content"]

    m.add(
        [{"role": "user", "content": user_input}, {"role": "assistant", "content": reply}],
        user_id=user_id,
    )
    return reply

print("Chat started. Type 'exit' to quit.\n")
while True:
    user_input = input("You: ")
    if user_input.lower() in ("exit", "quit"):
        break
    print("AI:", chat(user_input), "\n")