"""User interface for the multi-model chatbot using Gradio."""
from typing import Callable
from gradio import Interface, Textbox, Markdown

def create_input(fn: Callable[[str], str]) -> Interface:
    """Create a Gradio text interface for the given callback."""
    return Interface(fn=fn,  inputs=Textbox(label="Enter your message", lines=3), outputs=Markdown(label="Response"), title="Multi-Model Chatbot", flagging_mode="never",)