# AgentChat Migration Guide for v0.2 to v0.4

This guide helps users migrate from AutoGen AgentChat v0.2 to v0.4, which introduces new APIs and features with breaking changes.

## Overview of v0.4

AutoGen v0.4 is a rewrite adopting an asynchronous, event-driven architecture for improved observability, flexibility, interactive control, and scalability.

The v0.4 API is layered:

*   **Core API**: A scalable, event-driven actor framework.
*   **AgentChat API**: Built on Core, offering a task-driven, high-level framework (replacement for AutoGen v0.2).

## Key Changes and Migration Steps

### Model Client

*   **v0.2**: Configured using `OpenAIWrapper` with a list of model configurations.
*   **v0.4**: Two options:
    *   **Component Config**: Use the generic component configuration system.
    *   **Direct Model Client Class**: Instantiate `OpenAIChatCompletionClient` or `AzureOpenAIChatCompletionClient` directly.

### Assistant Agent

*   **v0.2**: Created using `AssistantAgent` with `llm_config`.
*   **v0.4**: Created using `AssistantAgent` with `model_client` instead of `llm_config`. Use `on_messages` or `on_messages_stream` to handle incoming messages.

### User Proxy

*   **v0.2**: Created using `UserProxyAgent` with specific configurations for human input, code execution, etc.
*   **v0.4**: Simply an agent that takes user input. Customize the input function for specific behavior.

### RAG Agent

*   **v0.2**: Implemented using `TeachableAgent` and `Teachability` with a database config.
*   **v0.4**: Implement a RAG agent using the `Memory` class and a custom memory store.

### Conversable Agent and Register Reply

*   **v0.2**: Used `ConversableAgent` and `register_reply` to define custom reply functions.
*   **v0.4**: Create a custom agent inheriting from `BaseChatAgent` and implement `on_messages`, `on_reset`, and `produced_message_types` methods.

### Save and Load Agent State

*   **v0.2**: No built-in way to save/load state; required manual handling of `chat_messages`.
*   **v0.4**: Use `save_state` and `load_state` methods on agents and teams.

### Two-Agent Chat

*   **v0.2**: Used `AssistantAgent` and `UserProxyAgent` with specific configurations.
*   **v0.4**: Use `AssistantAgent` and `CodeExecutorAgent` together in a `RoundRobinGroupChat`.

### Tool Use

*   **v0.2**: Required two agents (one for calling, one for executing) and a user proxy for routing.
*   **v0.4**: Use a single `AssistantAgent` with the `tools` parameter.

### Chat Result

*   **v0.2**: `initiate_chat` returned a `ChatResult` object with `summary`, `chat_history`, `cost`, and `human_input`.
*   **v0.4**: `run` or `run_stream` return a `TaskResult` object with a `messages` list (different format than `chat_history`). No `summary`, `human_input`, or `cost` fields; these must be extracted manually.

### Conversion between v0.2 and v0.4 Messages

Conversion functions are provided to convert between v0.4 `BaseAgentEvent | BaseChatMessage` and v0.2 `Dict[str, Any]` message formats.

### Group Chat

*   **v0.2**: Used `GroupChat` and `GroupChatManager` with a user proxy to initiate the chat.
*   **v0.4**: Use `RoundRobinGroupChat` or `SelectorGroupChat`.

### Group Chat with Resume

*   **v0.2**: Required explicit saving and loading of group chat messages.
*   **v0.4**: Call `run` or `run_stream` again with the same group chat object. Use `save_state` and `load_state` for persistence.

### Group Chat with Tool Use

*   **v0.2**: Required registering tool functions on a user proxy.
*   **v0.4**: Add tools directly to the `AssistantAgent`.

### Group Chat with Custom Selector (Stateflow)

*   **v0.2**: Used a custom function for `speaker_selection_method`.
*   **v0.4**: Use `SelectorGroupChat` with `selector_func`.

### Nested Chat

*   **v0.2**: Used `register_nested_chats` on `ConversableAgent`.
*   **v0.4**: Create a custom agent that takes a team or agent as a parameter and implements `on_messages` to trigger the nested chat.

### Sequential Chat

*   **v0.2**: Used the `initiate_chats` function.
*   **v0.4**: No built-in function; create an event-driven sequential workflow using the Core API.

### GPTAssistantAgent

*   **v0.2**: A special agent class backed by the OpenAI Assistant API.
*   **v0.4**: Use the `OpenAIAssistantAgent` class.

### Long Context Handling

*   **v0.2**: Used the `transforms` capability on `ConversableAgent`.
*   **v0.4**: Use the `ChatCompletionContext` base class and implementations like `BufferedChatCompletionContext` to manage message history.

### Observability and Control

*   **v0.4**: Use `on_messages_stream` and `run_stream` to stream agent and team activity. Use `CancellationToken` to cancel streams and termination conditions to stop teams. Use Python's `logging` module for events.

### Code Executors

Code executors are nearly identical, except v0.4 executors support async API and `CancellationToken`.

## Missing Features (Future Releases)

*   Model Client Cost
*   Teachable Agent
*   RAG Agent
