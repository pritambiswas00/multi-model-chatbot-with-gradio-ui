"""Initialize the multi-model chatbot library."""
from anthropic import (
    Anthropic,
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    RateLimitError,
)
from expression import Result, Ok, Error
from collections.abc import Iterator


def chat_with_model(model_client: Anthropic, user_input: str):
    """Send user input to the model and return its text response."""
    if not user_input.strip():
        return Ok("Please enter a message")
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
    """Send user input to the model and return its text response."""
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
    """Unwrap a Result into text for the UI. Both branches are shown to the user."""
    result = chat_with_model(model_client, message)
    return result.default_with(lambda err: err)

def to_display_stream(model_client: Anthropic, message: str) -> Iterator[str]:
    result = chat_with_model_with_stream(model_client, message)
    for r in result:
        yield r.default_with(lambda err: err)