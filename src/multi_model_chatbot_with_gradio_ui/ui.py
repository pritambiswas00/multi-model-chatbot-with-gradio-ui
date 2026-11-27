"""User interface for the multi-model chatbot using Gradio."""
from typing import Callable
from collections.abc import Iterator
from gradio import Interface, Textbox, Markdown

def create_input(fn: Callable[[str], str]) -> Interface:
    """Create a Gradio interface that shows a complete reply at once.

    Args:
        fn: Callback taking the user's message and returning the reply text
            (rendered as Markdown).

    Returns:
        A configured ``Interface``; call ``launch()`` to serve it.
    """
    return Interface(fn=fn,  inputs=Textbox(label="Enter your message", lines=3), outputs=Markdown(label="Response"), title="Multi-Model Chatbot", flagging_mode="never",)

def create_input_stream(fn: Callable[[str], Iterator[str]]) -> Interface:
    """Create a Gradio interface that updates the reply as it streams in.

    Args:
        fn: Generator callback taking the user's message and yielding the
            reply text accumulated so far (rendered as Markdown).

    Returns:
        A configured ``Interface``; call ``launch()`` to serve it.
    """
    return Interface(
        fn=fn,
        inputs=Textbox(label="Enter your message", lines=3),
        outputs=Markdown(label="Response"),
        title="Multi-Model Chatbot",
        flagging_mode="never",
    )