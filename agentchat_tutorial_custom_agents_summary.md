# Summary of AgentChat Tutorial - Custom Agents Page

(Source: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/custom-agents.html)

This page explains how to create custom agents in AgentChat when preset agents don't fit the required behavior.

## Core Concepts

-   **Inheritance:** Custom agents must inherit from `BaseChatAgent`.
-   **Abstract Methods/Attributes:** Must implement:
    -   `on_messages(messages, cancellation_token)`: Defines agent's response logic. Returns a `Response` object. Expected to be stateful and handle new messages incrementally.
    -   `on_reset(cancellation_token)`: Resets the agent's internal state.
    -   `produced_message_types` (property): A sequence of `BaseChatMessage` types the agent can produce.
-   **Optional Methods:**
    -   `on_messages_stream(messages, cancellation_token)`: Can be implemented for streaming output. If not, the default implementation calls `on_messages` and yields the response messages.

## Example 1: `CountDownAgent`

-   A simple agent that counts down from a number and streams the count.
-   **Implementation:**
    -   Inherits `BaseChatAgent`.
    -   `__init__`: Takes `name` and `count`.
    -   `produced_message_types`: Returns `(TextMessage,)`.
    -   `on_messages`: Calls `on_messages_stream` and returns the final `Response`.
    -   `on_messages_stream`: Iterates from `count` down to 1, yielding a `TextMessage` for each number. Finally, yields a `Response` with the final `TextMessage("Done!", ...)` and all intermediate messages in `inner_messages`.
    -   `on_reset`: Does nothing (`pass`).
-   **Usage:** Shows creating the agent and iterating through `on_messages_stream` to print the countdown and final message.

## Example 2: `ArithmeticAgent`

-   An agent that applies a specific arithmetic operation (passed as a function) to a number received in the last message.
-   **Implementation:**
    -   Inherits `BaseChatAgent`.
    -   `__init__`: Takes `name`, `description`, and `operator_func` (a `Callable[[int], int]`). Stores message history (`_message_history`).
    -   `produced_message_types`: Returns `(TextMessage,)`.
    -   `on_messages`: Appends incoming `messages` to `_message_history`. Parses the integer from the *last* message in history. Applies `_operator_func`. Creates and appends the result `TextMessage`. Returns a `Response` with the result message.
    -   `on_reset`: Does nothing (`pass`).
-   **Usage (in `SelectorGroupChat`):**
    -   Creates multiple `ArithmeticAgent` instances (add, multiply, subtract, divide, identity).
    -   Sets up a `SelectorGroupChat` with these agents.
    -   Crucially sets `allow_repeated_speaker=True` (to allow, e.g., multiple additions).
    -   Customizes the `selector_prompt` to guide the LLM selector.
    -   Runs the team with a task to transform 10 into 25. The output shows the selector choosing the appropriate agents sequentially.
    -   **Note:** Emphasizes that `on_messages` might receive an empty list if the agent was selected previously, highlighting the need for internal history (`_message_history`).

## Using Custom Model Clients in Custom Agents

-   Addresses scenarios where `AssistantAgent`'s `model_client` argument isn't sufficient (e.g., unsupported client, custom behavior).
-   **Example: `GeminiAssistantAgent`:**
    -   Shows creating a custom agent that directly uses the `google-genai` SDK.
    -   `__init__`: Initializes `genai.Client`, stores model name, API key, system message. Uses `UnboundedChatCompletionContext` for history.
    -   `on_messages_stream`: Adds incoming messages to context. Formats history. Calls `genai` client's `generate_content`. Creates `RequestUsage`. Adds response to context. Yields final `Response` with `TextMessage`.
    -   `on_reset`: Clears the model context.
    -   Demonstrates running this agent standalone.
    -   Demonstrates using this `GeminiAssistantAgent` as a critic within a `RoundRobinGroupChat` alongside a standard `AssistantAgent`, showcasing interoperability.

## Making the Custom Agent Declarative (`Component`)

-   Explains making custom agents serializable using Autogen's `Component` interface for saving/loading configurations.
-   **Implementation:**
    -   Inherit from `Component[YourConfigModel]`.
    -   Define a Pydantic `BaseModel` for configuration (`GeminiAssistantAgentConfig`).
    -   Implement `_from_config(cls, config)` classmethod to instantiate from config.
    -   Implement `_to_config(self)` method to return a config instance.
    -   Optionally set `component_provider_override` class variable to the full import path for reliable loading.
-   **Usage:** Shows calling `agent.dump_component()` to get the serializable config and `AgentClass.load_component(config)` to recreate the agent.

## Next Steps

-   Suggests extending the Gemini agent for function calling.
-   Suggests packaging a custom agent and using its declarative format in tools like AutoGen Studio.

The next section linked in the sidebar/footer is "Selector Group Chat".
