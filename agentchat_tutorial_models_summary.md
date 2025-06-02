Summary of AgentChat Tutorial - Models Page (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/models.html):

This page explains how AgentChat agents use model clients provided by `autogen-core` and `autogen-ext` to interact with various LLM services.

Key Concepts & Clients:
-   **Model Client Protocol:** `autogen-core` defines a standard interface (`ChatCompletionClient`) for interacting with different LLM APIs. `autogen-ext` provides implementations for popular services.
-   **Caching:** Mentions `ChatCompletionCache` as a wrapper to cache model responses.
-   **Logging:** Model calls and responses are logged using the standard Python logging module under the logger name `autogen_core.EVENT_LOGGER_NAME` with event type `LLMCall`. Provides code to enable INFO level logging.
-   **OpenAI:**
    -   Requires `pip install "autogen-ext[openai]"`.
    -   Uses `OpenAIChatCompletionClient`.
    -   Requires OpenAI API key (can be set via `OPENAI_API_KEY` env var or passed directly).
    -   Provides code example for instantiation and making a test call.
    -   Notes potential compatibility with OpenAI-compatible endpoints (untested).
-   **Azure OpenAI:**
    -   Requires `pip install "autogen-ext[openai,azure]"`.
    -   Uses `AzureOpenAIChatCompletionClient`.
    -   Requires deployment ID, endpoint, API version, model name.
    -   Supports API key or Azure Active Directory (AAD) token authentication (using `AzureTokenProvider` and `DefaultAzureCredential`).
    -   Provides code example using AAD authentication.
-   **Azure AI Foundry (Studio):**
    -   Requires `pip install "autogen-ext[azure]"`.
    -   Uses `AzureAIChatCompletionClient`.
    -   Example provided for using Phi-4 model via GitHub Marketplace endpoint, requiring a GitHub PAT (`GITHUB_TOKEN` env var) via `AzureKeyCredential`.
    -   Requires providing `model_info` dictionary specifying capabilities.
-   **Anthropic (Experimental):**
    -   Requires `pip install -U "autogen-ext[anthropic]"`.
    -   Uses `AnthropicChatCompletionClient`.
    -   Requires Anthropic API key.
    -   Provides code example.
-   **Ollama (Experimental):**
    -   Requires `pip install -U "autogen-ext[ollama]"`.
    -   Uses `OllamaChatCompletionClient`.
    -   Assumes local Ollama server running.
    -   Notes potential capability limitations of local models.
    -   Provides code example.
-   **Gemini (Experimental):**
    -   Uses the standard `OpenAIChatCompletionClient` due to Gemini's OpenAI-compatible API (beta).
    -   Requires Gemini API key.
    -   Notes potential minor API differences (e.g., `finish_reason`).
    -   Provides code example.
-   **Semantic Kernel Adapter:**
    -   Allows using Semantic Kernel model clients via `SKChatCompletionAdapter`.
    -   Requires installing relevant provider extras (e.g., `semantic-kernel-anthropic`).
    -   Provides an example using Anthropic via Semantic Kernel.

The next step indicated in the tutorial is the "Messages" section.
