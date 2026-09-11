"""
AI Chatbot — Gradio UI on top of OpenRouter's free models.

Setup:
    pip install gradio requests python-dotenv
    Create a .env file with:
        OPENROUTER_API_KEY=your_openrouter_key
    Get a free key (no card needed) at https://openrouter.ai/keys

Run:
    python ai_chatbot_gradio.py
    Opens a local chat window in your browser.
"""

import os
import requests
import gradio as gr
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODELS_URL = "https://openrouter.ai/api/v1/models"


# ---------- fetch current free models, so the dropdown never goes stale ----------

def list_free_models():
    try:
        r = requests.get(MODELS_URL, timeout=15)
        r.raise_for_status()
        all_models = r.json()["data"]
        free_ids = [m["id"] for m in all_models if m["id"].endswith(":free")]
        free_ids.sort()
    except Exception:
        free_ids = []
    # openrouter/free is a built-in router that always works, so it's always first
    return ["openrouter/free"] + free_ids


# ---------- send one chat turn to OpenRouter ----------

def ask_openrouter(messages, model):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://jekacode.africa",
        "X-Title": "AI Chatbot",
    }
    payload = {"model": model, "messages": messages}
    r = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"].strip()


# ---------- Gradio's chat function: takes new message + history, returns reply ----------

def chat_fn(message, history, model):
    # rebuild the full conversation so far, in the format OpenRouter expects
    messages = []
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    try:
        return ask_openrouter(messages, model)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:
            return "Rate limited — this free model is getting too many requests. Try again in a moment, or switch models."
        if e.response.status_code == 404:
            return f"Model '{model}' isn't available anymore. Pick a different one from the dropdown."
        return f"Error: {e}"
    except Exception as e:
        return f"Something went wrong: {e}"


# ---------- build the UI ----------

free_models = list_free_models()
default_model = free_models[0] if free_models else "openrouter/free"

model_picker = gr.Dropdown(
    choices=free_models,
    value=default_model,
    label="Model (free tier)",
)

demo = gr.ChatInterface(
    fn=chat_fn,
    additional_inputs=[model_picker],
    type="messages",
    title="AI Chatbot — free models via OpenRouter",
    description="Pick a free model, then chat. Model list is fetched live from OpenRouter, so it stays current.",
)

if __name__ == "__main__":
    demo.launch()
