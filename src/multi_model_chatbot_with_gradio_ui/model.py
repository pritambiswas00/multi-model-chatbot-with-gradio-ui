"""Initialize the model with the necessary configuration."""
from anthropic import Anthropic
from multi_model_chatbot_with_gradio_ui.config import Config

def initialize_model_client(config: Config) -> Anthropic:
    """Initialize the model with the provided configuration."""
    client = Anthropic(api_key=config.anthropic_api_key)
    print("Anthropic Instance initialized successfully.")
    return client
