"""Main entry point for the multi-model chatbot with Gradio UI."""
import sys
from collections.abc import Iterator

from expression import NOTHING, Error, Ok, Option, Result, Some
from gradio import Interface
from pydantic import ValidationError

from multi_model_chatbot_with_gradio_ui.config import Config
from multi_model_chatbot_with_gradio_ui.lib import to_display, to_display_stream
from multi_model_chatbot_with_gradio_ui.model import initialize_model_client
from multi_model_chatbot_with_gradio_ui.ui import create_input, create_input_stream

STREAMING = True
"""Selects the UI mode: ``True`` streams the reply as it is generated, ``False`` shows it at once."""


def load_config() -> Result[Config, str]:
    """Load configuration from the environment or the ``.env`` file.

    Returns:
        ``Ok`` with the loaded ``Config``, or ``Error`` with a message
        describing the validation failure (for example a missing or malformed
        ``ANTHROPIC_API_KEY``).
    """
    try:
        return Ok(Config())  # pyright: ignore[reportCallIssue]
    except ValidationError as e:
        return Error(f"Invalid configuration:\n{e}")


def run_app(config: Config) -> Result[None, str]:
    """Create the model client and launch the Gradio UI.

    The interface is streaming or non-streaming depending on ``STREAMING``.
    This call blocks while the server is running.

    Args:
        config: Validated application configuration.

    Returns:
        ``Ok(None)`` once the server stops, or ``Error`` with a message if the
        server could not start (for example the port is already in use).
    """
    model_client = initialize_model_client(config)
    print("Configuration loaded successfully.")

    interface: Option[Interface] = NOTHING
    if STREAMING:
        def response(message: str) -> Iterator[str]:
            yield from to_display_stream(model_client, message)

        interface = Some(create_input_stream(response))
    else:
        interface = Some(create_input(lambda x: to_display(model_client, x)))  # This is without stream

    if interface.is_some():
        try:
            interface.value.launch()
        except OSError as e:
            return Error(f"Failed to start the server: {e}")

    return Ok(None)


def main() -> Result[None, str]:
    """Load configuration, then launch the app, stopping at the first error.

    Returns:
        ``Ok(None)`` on a clean run, or the first ``Error`` from
        ``load_config`` or ``run_app``. When run as a script, an error is
        printed and the process exits with a non-zero status.
    """
    return load_config().bind(run_app)


if __name__ == "__main__":
    main().default_with(lambda err: sys.exit(f"Error: {err}"))