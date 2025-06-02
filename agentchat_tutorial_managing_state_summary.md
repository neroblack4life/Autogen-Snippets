# Summary of AgentChat Tutorial - Managing State Page

(Source: https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html)

This page explains how to save and load the state of AgentChat agents and teams, enabling persistence across sessions, which is crucial for applications like web services.

## Saving and Loading Agents

-   **Saving State:** Use `agent_state = await agent.save_state()` on an `AssistantAgent` (or potentially other agent types).
    -   For `AssistantAgent`, the state primarily consists of the `model_context` (e.g., conversation history stored in `llm_messages`).
    -   The returned `agent_state` is a dictionary (serializable).
-   **Loading State:** Use `await new_agent.load_state(agent_state)` on a *newly instantiated* agent.
    -   The example shows creating a new agent, loading the saved state, and then asking a follow-up question based on the loaded history, which the agent correctly answers.
-   **Custom Agents:** Default `save_state`/`load_state` implementations save/load an empty state. Custom agents should override these methods to handle their specific state.

## Saving and Loading Teams

-   **Saving State:** Use `team_state = await team.save_state()` on the team object (e.g., `RoundRobinGroupChat`).
    -   This saves the state of the team itself *and* the states of all agents within it.
    -   The returned `team_state` is a dictionary containing agent states keyed appropriately (e.g., `agent_states['assistant_agent/team_id']`).
-   **Loading State:** Use `await new_team.load_state(team_state)` on a *newly instantiated* team (with the same agent configuration).
    -   The example demonstrates:
        1.  Running a team, saving its state.
        2.  Resetting the team (`await team.reset()`) and showing it lost context.
        3.  Loading the saved state (`await team.load_state(team_state)`) and showing it regained context.

## Persisting State (File or Database)

-   The `agent_state` and `team_state` dictionaries are JSON-serializable.
-   **Example (File):**
    -   Shows saving `team_state` to a JSON file (`json.dump(team_state, f)`).
    -   Shows loading `team_state` from the file (`team_state = json.load(f)`).
    -   Demonstrates creating a *new* team instance, loading the state from the file, and successfully resuming the conversation context.

## Next Step

The next section in the tutorial is "Custom Agents".
