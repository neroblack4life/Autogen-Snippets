# Code snippets from AgentChat Tutorial - Managing State Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/state.html)

import asyncio
import json
import os # For file operations

# Assuming necessary autogen imports are present
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.conditions import MaxMessageTermination
    from autogen_agentchat.messages import TextMessage
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_agentchat.ui import Console
    from autogen_core import CancellationToken
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    # For example output parsing
    from autogen_agentchat.base import TaskResult
    from autogen_core.models import RequestUsage

except ImportError as e:
    print(f\"Note: Some imports failed, likely due to missing packages: {e}\")
    # Define dummy classes/functions if needed
    class Dummy: pass
    AssistantAgent = Dummy
    MaxMessageTermination = Dummy
    TextMessage = Dummy
    RoundRobinGroupChat = Dummy
    Console = Dummy
    CancellationToken = Dummy
    OpenAIChatCompletionClient = Dummy
    TaskResult = Dummy
    RequestUsage = Dummy


# --- Saving and Loading Agents ---
print(\"--- Saving and Loading Agent State Example ---\")
async def run_agent_save_load_example():
    print(\"Setting up agent save/load example...\")
    agent_state = None # Define in outer scope
    new_assistant_agent = None
    try:
        model_client_agent_sl = OpenAIChatCompletionClient(model=\"gpt-4o-2024-08-06\")
        print(\"Model client created.\")

        assistant_agent = AssistantAgent(
            name=\"assistant_agent_sl\", # Use unique name
            system_message=\"You are a helpful assistant\",
            model_client=model_client_agent_sl,
        )
        print(f\"Created agent: {assistant_agent.name}\")

        print(\"\\nRunning agent to generate initial state...\")
        response1 = await assistant_agent.on_messages(
            [TextMessage(content=\"Write a 3 line poem on lake tangayika\", source=\"user\")], CancellationToken()
        )
        print(\"Agent Response 1:\")
        print(response1.chat_message)
        print(\"(Actual output depends on live model call)\")

        print(\"\\nSaving agent state...\")
        agent_state = await assistant_agent.save_state()
        print(\"Agent State Saved:\")
        # print(agent_state) # Can be large

        await model_client_agent_sl.close() # Close original client
        print(\"Original model client closed.\")

        # --- Load state into a new agent ---
        print(\"\\nCreating new agent and loading state...\")
        model_client_agent_sl_new = OpenAIChatCompletionClient(model=\"gpt-4o-2024-08-06\")
        new_assistant_agent = AssistantAgent(
            name=\"assistant_agent_sl\", # Same name usually desired when loading state
            system_message=\"You are a helpful assistant\",
            model_client=model_client_agent_sl_new,
        )
        await new_assistant_agent.load_state(agent_state)
        print(\"State loaded into new agent.\")

        print(\"\\nRunning new agent with loaded state...\")
        response2 = await new_assistant_agent.on_messages(
            [TextMessage(content=\"What was the last line of the previous poem you wrote\", source=\"user\")], CancellationToken()
        )
        print(\"Agent Response 2 (should have context):\")
        print(response2.chat_message)
        print(\"(Actual output depends on live model call)\")

        await model_client_agent_sl_new.close()
        print(\"New model client closed.\")

    except Exception as e:
        print(f\"Error during agent save/load example: {e}\")
        # Cleanup clients if they exist
        if 'model_client_agent_sl' in locals() and hasattr(model_client_agent_sl, 'close'):
             try: await model_client_agent_sl.close(); print(\"Original client closed after error.\")
             except: pass
        if 'model_client_agent_sl_new' in locals() and hasattr(model_client_agent_sl_new, 'close'):
             try: await model_client_agent_sl_new.close(); print(\"New client closed after error.\")
             except: pass

# Example execution
# asyncio.run(run_agent_save_load_example())
print(\"(Skipping actual execution of run_agent_save_load_example in this script)\")


# --- Saving and Loading Teams ---
print(\"\\n--- Saving and Loading Team State Example ---\")
async def run_team_save_load_example():
    print(\"Setting up team save/load example...\")
    agent_team = None # Define in outer scope
    team_state = None
    try:
        model_client_team_sl = OpenAIChatCompletionClient(model=\"gpt-4o-2024-08-06\")
        print(\"Model client created.\")

        # Define a team.
        assistant_agent_team = AssistantAgent(
            name=\"assistant_agent_team\", # Unique name
            system_message=\"You are a helpful assistant\",
            model_client=model_client_team_sl,
        )
        print(f\"Created agent: {assistant_agent_team.name}\")
        agent_team = RoundRobinGroupChat(
            [assistant_agent_team],
            termination_condition=MaxMessageTermination(max_messages=2)
        )
        print(\"Created team.\")

        # Run the team to generate state.
        print(\"\\nRunning team (run 1) to generate state...\")
        stream1 = agent_team.run_stream(task=\"Write a beautiful poem 3-line about lake tangayika\")
        await Console(stream1)
        print(\"\\n(Console output depends on live model calls)\")

        # Save the state.
        print(\"\\nSaving team state...\")
        team_state = await agent_team.save_state()
        print(\"Team state saved.\")
        # print(team_state) # Can be large

        # Reset the team (simulates losing state).
        print(\"\\nResetting team...\")
        await agent_team.reset()
        print(\"Team reset.\")

        # Run again (should have no context).
        print(\"\\nRunning team (run 2) after reset (expect no context)...\")
        stream2 = agent_team.run_stream(task=\"What was the last line of the poem you wrote?\")
        await Console(stream2)
        print(\"\\n(Console output depends on live model calls)\")

        # Load the state back.
        print(\"\\nLoading saved team state...\")
        await agent_team.load_state(team_state)
        print(\"Team state loaded.\")

        # Run again (should have context now).
        print(\"\\nRunning team (run 3) after loading state (expect context)...\")
        stream3 = agent_team.run_stream(task=\"What was the last line of the poem you wrote?\")
        await Console(stream3)
        print(\"\\n(Console output depends on live model calls)\")

        await model_client_team_sl.close()
        print(\"Model client closed.\")

    except Exception as e:
        print(f\"Error during team save/load example: {e}\")
        if 'model_client_team_sl' in locals() and hasattr(model_client_team_sl, 'close'):
            try: await model_client_team_sl.close(); print(\"Model client closed after error.\")
            except: pass


# Example execution
# asyncio.run(run_team_save_load_example())
print(\"(Skipping actual execution of run_team_save_load_example in this script)\")


# --- Persisting State (File Example) ---
print(\"\\n--- Persisting State (File) Example ---\")
async def run_persist_state_example():
    print(\"Setting up state persistence example...\")
    # Assume team_state exists from the previous example run
    # In a real script, you'd likely run the previous part first or load from file directly
    if 'team_state' not in locals() or team_state is None:
         print(\"Team state not found from previous step. Skipping persistence example.\")
         # You could optionally run the team generation part here if needed
         return

    # Define file path (ensure directory exists or handle creation)
    save_dir = \"coding\" # Relative to current working directory
    file_path = os.path.join(save_dir, \"team_state.json\")
    loaded_team_state = None
    new_agent_team = None

    try:
        # Ensure directory exists
        os.makedirs(save_dir, exist_ok=True)
        print(f\"Ensured directory '{save_dir}' exists.\")

        # Save state to disk
        print(f\"Saving team state to {file_path}...\")
        with open(file_path, \"w\") as f:
            json.dump(team_state, f, indent=2) # Added indent for readability
        print(\"Team state saved to file.\")

        # Load state from disk
        print(f\"\\nLoading team state from {file_path}...\")
        with open(file_path, \"r\") as f:
            loaded_team_state = json.load(f)
        print(\"Team state loaded from file.\")

        # Create a new team instance and load the state
        print(\"\\nCreating new team instance...\")
        # Need to recreate the agent(s) for the new team
        model_client_persist = OpenAIChatCompletionClient(model=\"gpt-4o-2024-08-06\")
        assistant_agent_persist = AssistantAgent(
             name=\"assistant_agent_team\", # Match name from saved state if important
             system_message=\"You are a helpful assistant\",
             model_client=model_client_persist,
        )
        new_agent_team = RoundRobinGroupChat(
             [assistant_agent_persist],
             termination_condition=MaxMessageTermination(max_messages=2)
        )
        print(\"New team instance created.\")

        print(\"Loading state into new team instance...\")
        await new_agent_team.load_state(loaded_team_state)
        print(\"State loaded into new team.\")

        # Run the new team (should have context)
        print(\"\\nRunning new team with loaded state (expect context)...\")
        stream_persist = new_agent_team.run_stream(task=\"What was the last line of the poem you wrote?\")
        await Console(stream_persist)
        print(\"\\n(Console output depends on live model calls)\")

        await model_client_persist.close()
        print(\"Model client closed.\")

        # Optional: Clean up the created file
        # os.remove(file_path)
        # print(f\"Cleaned up {file_path}\")

    except Exception as e:
        print(f\"Error during state persistence example: {e}\")
        if 'model_client_persist' in locals() and hasattr(model_client_persist, 'close'):
            try: await model_client_persist.close(); print(\"Model client closed after error.\")
            except: pass

# Example execution
# asyncio.run(run_persist_state_example())
print(\"(Skipping actual execution of run_persist_state_example in this script)\")
