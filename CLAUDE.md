# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## API Key Setup

The app requires a Gemini API key stored in `.streamlit/secrets.toml` (not committed to git):

```toml
GEMINI_API_KEY = "your_key_here"
```

Get a key from Google AI Studio: https://aistudio.google.com/app/apikey

## Architecture

This is a single-file Streamlit app (`app.py`) with no separate modules. All logic lives in one file:

- **`init_gemini()`** — reads `GEMINI_API_KEY` from `st.secrets` and returns a `genai.Client`
- **`build_system_prompt()`** — returns the Korean-language system prompt that defines AI output structure
- **`generate_itinerary()`** — calls `gemini-2.0-flash` with combined system + user prompt; no streaming
- **Layout** — two-column layout (`col_input` / `col_result`) with a sidebar for history
- **Session state** — `st.session_state.history` (list, max 5), `current_result` (str), `current_info` (dict)

The app is entirely in Korean. All AI output is also in Korean per the system prompt.

Deployment target is Streamlit Cloud; secrets are set via the Streamlit Cloud dashboard instead of `secrets.toml`.
