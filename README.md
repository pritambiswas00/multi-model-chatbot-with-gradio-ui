# Multi-model Chatbot with Gradio UI

## Run

This project requires Python 3.12 or newer and `uv`. Set `ANTHROPIC_API_KEY`
in a local `.env` file, then run:

```sh
uv sync
uv run multi-model-chatbot-with-gradio-ui
```

The app launches a Gradio interface. Set `STREAMING` in
[main.py](src/multi_model_chatbot_with_gradio_ui/main.py) to choose between a
streaming reply (`True`, the default) and a complete reply shown at once.

## Error handling

Expected failures are returned as values, not raised. Functions return a
`Result` from the [`expression`](https://github.com/cognitedata/Expression)
library: `Ok(value)` on success or `Error(message)` with a human-readable
message on failure.

### Startup

[main.py](src/multi_model_chatbot_with_gradio_ui/main.py) chains the startup
steps with `load_config().bind(run_app)`, so the first failure stops the chain.

| Step | Failure | Result |
| --- | --- | --- |
| `load_config` | `ANTHROPIC_API_KEY` missing or not starting with `sk-ant` (pydantic `ValidationError`) | `Error("Invalid configuration: ...")` |
| `run_app` | Server cannot start, e.g. port in use (`OSError`) | `Error("Failed to start the server: ...")` |

When run as a script, an error is printed as `Error: <message>` and the process
exits with a non-zero status.

### Chat requests

[lib.py](src/multi_model_chatbot_with_gradio_ui/lib.py) catches Anthropic SDK
exceptions and converts them into `Error` messages, for both the streaming and
non-streaming paths:

| Situation | Message shown |
| --- | --- |
| Blank input | `Please enter a message` (no API call is made) |
| `AuthenticationError` | Invalid API key; check `ANTHROPIC_API_KEY` in `.env` |
| `RateLimitError` | Rate limit hit; wait a moment and try again |
| `APIConnectionError` | Couldn't reach the Anthropic API; check your connection |
| Other `APIStatusError` | `Error <status code>: <API message>` |

`to_display` and `to_display_stream` unwrap each `Result` into plain text, so
the UI shows either the reply or the error message in the same response box.
In streaming mode, an error that occurs mid-stream replaces the partial reply
with the error message.

Errors not listed above (programming errors, unexpected exceptions) are not
caught and surface normally.