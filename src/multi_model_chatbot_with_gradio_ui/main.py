"""Main entry point for the multi-model chatbot with Gradio UI."""
from multi_model_chatbot_with_gradio_ui.model import initialize_model_client
from multi_model_chatbot_with_gradio_ui.config import Config
from multi_model_chatbot_with_gradio_ui.ui import create_input
from multi_model_chatbot_with_gradio_ui.lib import chat_with_model, to_display

def main() -> None:
    """Display the configured API key and a startup message."""
    config = Config()  # pyright: ignore[reportCallIssue]
    model_client = initialize_model_client(config)
    interface = create_input(lambda x: to_display(chat_with_model(model_client, x)))
    interface.launch()
    print("Hello from multi-model-chatbot-with-gradio-ui!")
    print("Configuration loaded successfully.")

if __name__ == "__main__":
    main()