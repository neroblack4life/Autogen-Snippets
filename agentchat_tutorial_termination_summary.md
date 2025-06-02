# Summary of AgentChat Tutorial - Termination Page

(Source: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html)

This page explains how to control when an AgentChat team run stops using termination conditions.

## Key Concepts

-   **Purpose:** Termination conditions determine when a team's `run()` or `run_stream()` execution should end.
-   **Mechanism:** A termination condition is a callable object that receives the sequence of messages/events generated since its last call. It returns a `StopMessage` if termination should occur, otherwise `None`.
-   **State:** Conditions are stateful but reset automatically after each run finishes. They must be manually reset (`await condition.reset()`) if reused within the same run context (though this is less common).
-   **Combining:** Conditions can be combined using bitwise OR (`|`) and AND (`&`) operators.
-   **Timing (Group Chats):** For `RoundRobinGroupChat`, `SelectorGroupChat`, and `Swarm`, the condition is checked *once* after each agent completes its turn (including all inner messages like tool calls).

## Built-In Termination Conditions

-   `MaxMessageTermination(max_messages)`: Stops after `n` messages (task + agent messages).
-   `TextMentionTermination(text)`: Stops when specific `text` is found in a message.
-   `TokenUsageTermination(...)`: Stops based on prompt/completion token counts (requires agents to report usage).
-   `TimeoutTermination(seconds)`: Stops after a duration.
-   `HandoffTermination(target)`: Stops when a `HandoffMessage` to the specified `target` (e.g., "user") occurs.
-   `SourceMatchTermination(agent_name)`: Stops after a specific agent responds.
-   `ExternalTermination()`: Allows stopping externally via `external_termination.set()`.
-   `StopMessageTermination()`: Stops when an agent explicitly returns a `StopMessage`.
-   `TextMessageTermination(agent_name)`: Stops when a specific agent produces a `TextMessage` (useful for single-agent loops).
-   `FunctionCallTermination(function_name)`: Stops when a specific function/tool call is executed (demonstrated with a custom implementation).

## Examples

-   **Basic Usage & Reset:**
    -   Shows `MaxMessageTermination(max_messages=3)` stopping a run.
    -   Demonstrates resuming the run by calling `run_stream()` again; the condition is automatically reset, allowing the conversation to continue for another 3 messages.
-   **Combining Conditions:**
    -   Uses `max_msg_termination | text_termination` to stop if *either* 10 messages are reached *or* "APPROVE" is mentioned.
    -   Mentions using `&` for AND logic (stop only if *both* conditions met).
-   **Custom Termination Condition:**
    -   Provides a full implementation of `FunctionCallTermination` by subclassing `TerminationCondition` and `Component`.
    -   It checks `ToolCallExecutionEvent` messages for a specific function name.
    -   Includes configuration (`FunctionCallTerminationConfig`) for serialization.
    -   Demonstrates using this custom condition to stop when a critic agent uses an `approve` tool (function).

## Next Step

The next section in the tutorial is "Managing State".
