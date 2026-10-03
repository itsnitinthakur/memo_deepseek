#!/usr/bin/env python3
import subprocess, sys, requests, pathlib

MEM_URL = "http://localhost:8123"
task = " ".join(sys.argv[1:]) or "general Django project work"

resp = requests.post(f"{MEM_URL}/search", json={"query": task})
memories = resp.json().get("memories", [])
pathlib.Path(".aider_memory.md").write_text(
    "# Relevant context from past sessions\n" + "\n".join(f"- {m}" for m in memories)
)

subprocess.run(["aider", "--model", "ollama/deepseek-coder-v2:16b", "--read", ".aider_memory.md"])

history_file = pathlib.Path(".aider.chat.history.md")
if history_file.exists():
    requests.post(f"{MEM_URL}/add", json={"text": history_file.read_text()[-3000:]})
    print("Session saved to memory.")