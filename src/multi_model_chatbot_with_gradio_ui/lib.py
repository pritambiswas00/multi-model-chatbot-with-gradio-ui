"""Chat helpers for the multi-model chatbot.

Wraps the Anthropic Messages API and reports failures as ``Result`` values
(``Ok`` with the reply, ``Error`` with a user-facing Markdown message) rather
than raising, so the UI layer can display either outcome directly.
"""
from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)
from expression import Result, Ok, Error
from collections.abc import Iterator


def chat_with_model(model_client: Anthropic, user_input: str) -> Result[str, str]:
    """Send a single message to the model and return the complete reply.

    Args:
        model_client: Configured Anthropic client used to make the request.
        user_input: The user's message. Blank input is not sent to the API.

    Returns:
        ``Ok`` with the concatenated text blocks of the model's reply.
        ``Ok`` with a prompt asking for a message if ``user_input`` is blank.
        ``Error`` with a user-facing message if the API call fails
        (invalid API key, rate limit, connection problem or other HTTP error).
    """
    if not user_input.strip():
        return Error("Please enter a message")
    try:
        response = model_client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_input}],
        )
    except AuthenticationError:
        return Error("**Error:** Invalid API key. Check `ANTHROPIC_API_KEY` in your `.env`.")
    except RateLimitError:
        return Error("**Error:** Rate limit hit. Wait a moment and try again.")
    except APIConnectionError:
        return Error("**Error:** Couldn't reach the Anthropic API. Check your internet connection.")
    except APIStatusError as e:
        return Error(f"**Error {e.status_code}:** {e.message}")
    result = ""
    for message in response.content:
        if message.type == "text":
            result += message.text
    return Ok(result)

def chat_with_model_with_stream(model_client: Anthropic, user_input: str) -> Iterator[Result[str, str]]:
    """Send a single message to the model and stream the reply as it is generated.

    Args:
        model_client: Configured Anthropic client used to make the request.
        user_input: The user's message. Blank input is not sent to the API.

    Yields:
        ``Ok`` with the *accumulated* reply text so far, once per text delta,
        so the last item is the full reply. Yields a single ``Error`` if the
        input is blank or the API call fails (invalid API key, rate limit,
        connection problem or other HTTP error).
    """
    if not user_input.strip():
        yield Error("Please enter a message")
        return
    try:
        response =  model_client.messages.create(
            model="claude-sonnet-5-5",
            max_tokens=1024,
            messages=[{"role": "user", "content": user_input}],
            stream=True
        )
        result = ""
        for event in response:
            if event.type == "content_block_delta" and event.delta.type == "text_delta":
                result += event.delta.text
                yield Ok(result)
    except AuthenticationError:
        yield Error("**Error:** Invalid API key. Check `ANTHROPIC_API_KEY` in your `.env`.")
    except RateLimitError:
        yield Error("**Error:** Rate limit hit. Wait a moment and try again.")
    except APIConnectionError:
        yield Error("**Error:** Couldn't reach the Anthropic API. Check your internet connection.")
    except APIStatusError as e:
        yield Error(f"**Error {e.status_code}:** {e.message}")


def to_display(model_client: Anthropic, message: str) -> str:
    """Get a complete reply as display text for the UI.

    Calls ``chat_with_model`` and unwraps the ``Result``. Both the reply and
    any error message are shown to the user.

    Args:
        model_client: Configured Anthropic client used to make the request.
        message: The user's message.

    Returns:
        The model's reply, or the error message if the request failed.
    """
    result = chat_with_model(model_client, message)
    return result.default_with(lambda err: err)

def to_display_stream(model_client: Anthropic, message: str) -> Iterator[str]:
    """Stream a reply as display text for the UI.

    Calls ``chat_with_model_with_stream`` and unwraps each ``Result``. Both
    reply text and error messages are shown to the user.

    Args:
        model_client: Configured Anthropic client used to make the request.
        message: The user's message.

    Yields:
        The accumulated reply text so far, or the error message if the
        request failed.
    """
    result = chat_with_model_with_stream(model_client, message)
    for r in result:
        yield r.default_with(lambda err: err)