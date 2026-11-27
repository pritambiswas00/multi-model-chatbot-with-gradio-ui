"""User interface for the multi-model chatbot using Gradio."""
from typing import Callable
from collections.abc import Iterator
from gradio import Interface, Textbox, Markdown

def create_input(fn: Callable[[str], str]) -> Interface:
    """Create a Gradio text interface for the given callback."""
    return Interface(fn=fn,  inputs=Textbox(label="Enter your message", lines=3), outputs=Markdown(label="Response"), title="Multi-Model Chatbot", flagging_mode="never",)

def create_input_stream(fn: Callable[[str], Iterator[str]]) -> Interface:
    """Create a Gradio text interface for the given streaming callback."""
    return Interface(
        fn=fn,
        inputs=Textbox(label="Enter your message", lines=3),
        outputs=Markdown(label="Response"),
        title="Multi-Model Chatbot",
        flagging_mode="never",
    )