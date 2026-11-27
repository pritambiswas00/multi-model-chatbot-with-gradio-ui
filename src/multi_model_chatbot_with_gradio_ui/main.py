"""Main entry point for the multi-model chatbot with Gradio UI."""
from collections.abc import Iterator

from expression import  Option, Some, NOTHING
from gradio import Interface
from multi_model_chatbot_with_gradio_ui.model import initialize_model_client
from multi_model_chatbot_with_gradio_ui.config import Config
from multi_model_chatbot_with_gradio_ui.ui import create_input_stream, create_input
from multi_model_chatbot_with_gradio_ui.lib import to_display_stream, to_display

STREAMING = True

def main() -> None:
    """Display the configured API key and a startup message."""
    config = Config()  # pyright: ignore[reportCallIssue]
    model_client = initialize_model_client(config)
    interface: Option[Interface] = NOTHING
    if STREAMING:
        def response(message: str)-> Iterator[str]:
            yield from to_display_stream(model_client, message)
        interface = Some(create_input_stream(response))
    else:
        interface = Some(create_input(lambda x: to_display(model_client, x))) ## This is without stream 
    if interface.is_some():
        interface.value.launch()
    print("Hello from multi-model-chatbot-with-gradio-ui!")
    print("Configuration loaded successfully.")

if __name__ == "__main__":
    main()