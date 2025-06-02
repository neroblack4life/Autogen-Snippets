Summary of AgentChat Tutorial - Teams Page (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html):

This page explains how to create and manage multi-agent teams in AgentChat.

Key Concepts & Features:
-   **Purpose of Teams:** Used for complex tasks requiring collaboration and diverse expertise. Recommended to start with a single agent and move to teams only when necessary after optimizing the single agent.
-   **Team Presets:**
    -   `RoundRobinGroupChat`: Agents share context and respond in round-robin order (covered on this page).
    -   `SelectorGroupChat`: Selects the next speaker using an LLM.
    -   `MagenticOneGroupChat`: Generalist system for web/file tasks.
-   **Creating a Team (`RoundRobinGroupChat`):**
    -   Example demonstrates a two-agent "reflection pattern" team (primary agent + critic agent).
    -   Requires defining agents (`AssistantAgent`), a model client (`OpenAIChatCompletionClient`), and a termination condition (`TextMentionTermination` triggered by "APPROVE" from the critic).
    -   Team is instantiated: `team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)`.
-   **Running a Team (`run`):**
    -   Use `await team.run(task=...)`.
    -   Runs agents in round-robin order until the termination condition is met.
    -   Returns a `TaskResult` object containing all messages and the `stop_reason`.
    -   Example shows a primary agent writing a poem and a critic providing feedback until it responds with "APPROVE".
-   **Observing a Team (`run_stream`):**
    -   Use `await team.run_stream(task=...)` or `async for message in team.run_stream(...)`.
    -   Yields messages as they are generated, with the final item being the `TaskResult`.
    -   Allows observing the conversation flow.
    -   `Console()` provides formatted output for streams. Example shows using `Console(team.run_stream(...))`.
-   **Resetting a Team (`reset`):**
    -   `await team.reset()` clears the state of the team and all its agents (by calling their `on_reset()` methods).
    -   Recommended when starting an unrelated task.
-   **Stopping a Team (ExternalTermination):**
    -   Allows stopping a team externally.
    -   Create `external_termination = ExternalTermination()`.
    -   Combine conditions: `termination_condition=external_termination | text_termination`.
    -   Run the team in a background task (`asyncio.create_task`).
    -   Call `external_termination.set()` to signal stop.
    -   The team stops after the current agent finishes its turn. `stop_reason` will indicate external termination.
-   **Resuming a Team:**
    -   Teams are stateful unless reset.
    -   Call `run()` or `run_stream()` again *without* a task argument to continue from where it left off.
    -   `RoundRobinGroupChat` continues with the next agent in sequence.
    -   Example shows resuming the poem task after external termination.
    -   Example also shows resuming with a *new* related task (translating the poem) while retaining context.
-   **Aborting a Team (CancellationToken):**
    -   Pass a `CancellationToken` to `run(..., cancellation_token=...)`.
    -   Call `cancellation_token.cancel()` to abort immediately.
    -   Raises an `asyncio.CancelledError` in the caller.
-   **Single-Agent Team:**
    -   Useful for running a single `AssistantAgent` in a loop until a condition is met (unlike the agent's own `run` method which is single-step).
    -   Example shows an agent with an `increment_number` tool running in a `RoundRobinGroupChat` with only itself.
    -   Uses `TextMessageTermination("looped_assistant")` to stop when the agent produces a final `TextMessage` instead of a tool call summary.
    -   Demonstrates the agent repeatedly calling the tool until the target number is reached.

The next step indicated in the tutorial is the "Human-in-the-Loop" section.
