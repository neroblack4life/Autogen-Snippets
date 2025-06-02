# Summary of AgentChat Tutorial - Human-in-the-Loop Page

(Source: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)

This page explains how users or applications can interact with and provide feedback to an AgentChat team.

## Interaction Methods

There are two primary ways to provide feedback:

1.  **During a Run (via `UserProxyAgent`):**
    *   Include a `UserProxyAgent` instance in the team.
    *   The team calls this agent when it needs user input (determined by team type, e.g., round-robin order or selector logic).
    *   The `UserProxyAgent` blocks team execution until feedback is received (e.g., via console `input()` or a custom function).
    *   **Use Case:** Recommended for short interactions requiring immediate feedback (e.g., approval clicks, critical alerts). Blocking nature makes it unsuitable for long waits as it destabilizes the team state for saving/resuming.
    *   **Example:** A `RoundRobinGroupChat` with an `AssistantAgent` and a `UserProxyAgent` (using `input()` for console feedback) is shown. The user types "APPROVE" to terminate.
    *   **Custom Input:** Shows a conceptual FastAPI example where `UserProxyAgent` uses a custom `_user_input` function waiting for a message from a WebSocket. Links to full FastAPI, ChainLit, and Streamlit samples are provided.

2.  **Between Runs (After Termination):**
    *   The team runs until a termination condition is met.
    *   The application/user provides feedback as input to the *next* `run()` or `run_stream()` call.
    *   **Use Case:** Suitable for persisted sessions with asynchronous communication. The application can save the team state after a run, wait for feedback, load the state, and resume with the feedback. (Refers to "Managing State" page for saving/loading).
    *   **Implementation:**
        *   **Using `max_turns`:** Set `max_turns` (e.g., `max_turns=1`) in team constructors (`RoundRobinGroupChat`, `SelectorGroupChat`, `Swarm`). The team stops after `n` turns, allowing feedback before resuming. The turn count resets on resume, but history is preserved. Example shows a loop getting user feedback via `input()` after each turn.
        *   **Using Termination Conditions:** Use conditions like `TextMentionTermination` or `HandoffTermination`. `HandoffTermination` stops the team when an agent sends a `HandoffMessage`. Example shows a "lazy_agent" using `handoffs=[Handoff(target="user", ...)]` to transfer control when it can't complete a task (like getting weather without a tool). The team stops with `stop_reason='Handoff to user...'`. The user then provides the needed info in the next `run_stream(task=...)` call, allowing the team to resume and complete.
        *   **Note on Swarm:** Mentions that resuming a Swarm team after a user handoff requires setting the task to a `HandoffMessage` targeting the next agent.

## Next Step

The next section in the tutorial is "Termination".
