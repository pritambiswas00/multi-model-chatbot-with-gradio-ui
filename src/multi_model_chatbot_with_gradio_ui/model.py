"""Model client setup for the multi-model chatbot."""
from anthropic import Anthropic
from multi_model_chatbot_with_gradio_ui.config import Config

def initialize_model_client(config: Config) -> Anthropic:
    """Create the Anthropic client used to talk to the model.

    Args:
        config: Application configuration providing ``anthropic_api_key``.

    Returns:
        An ``Anthropic`` client authenticated with the configured API key.
        The key is not validated here; an invalid key fails on the first request.
    """
    client = Anthropic(api_key=config.anthropic_api_key)
    print("Anthropic Instance initialized successfully.")
    return client
