"""Week 4 — Gradio chat (fastest UI).

What this file is for
---------------------
Talk to Gemini, Grok, DeepSeek, or Ollama from a webpage without writing HTML.

How to run (course root, venv on)
    python week04-ai-apps/gradio_chat.py
Then open the http://127.0.0.1:7860 link printed in the terminal.

How to get models working
    See guides/HOW_TO.md  (Ollama install, Gemini key, Grok key)
"""

import sys
from pathlib import Path

# Make `import jekacode` work when we run this file from any folder.
sys.path.append(str(Path(__file__).resolve().parents[1]))

# gradio draws buttons and boxes. We nickname it gr to type less.
import gradio as gr

# ask() is our one door to every classroom model.
from jekacode.ai import ask

# SYSTEM is a job description sent with every question (a "system prompt").
SYSTEM = "You are a Jekacode tutor. Simple English. African examples when useful."


def reply(message: str, provider: str) -> str:
    """This function runs when the student clicks Submit on the web page."""
    # strip() removes extra spaces. Empty text should not call the API (saves money/time).
    if not message.strip():
        return "Type a question first."
    # provider is the kitchen: gemini, grok, deepseek, or ollama.
    return ask(message, provider=provider, system=SYSTEM)


# Interface = "here is a form". fn= which Python function to call.
demo = gr.Interface(
    fn=reply,
    inputs=[
        gr.Textbox(label="Your question", lines=4, placeholder="Explain photosynthesis like I am 12"),
        gr.Dropdown(["gemini", "grok", "deepseek", "ollama"], value="gemini", label="Model"),
    ],
    outputs=gr.Textbox(label="Answer", lines=12),
    title="Jekacode · Gradio",
    description="Fast UI. HTML chatbot looks more like a company product.",
)

# Only launch the website if we typed: python gradio_chat.py
# (If another file imported this, we would not want a server to start.)
if __name__ == "__main__":
    demo.launch()
