# Code snippets from AgentChat Tutorial - Teams Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/teams.html)

import asyncio

# Assuming necessary autogen imports are present from previous steps or installed
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.base import TaskResult # Base class, might not be directly used in snippets but good context
    from autogen_agentchat.conditions import ExternalTermination, TextMentionTermination, TextMessageTermination
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_agentchat.ui import Console
    from autogen_core import CancellationToken
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    # For single-agent example output
    from autogen_agentchat.messages import TextMessage, ToolCallRequestEvent, ToolCallExecutionEvent, ToolCallSummaryMessage
    from autogen_core.models import RequestUsage # For example output parsing
    from autogen_core.tool_runtime import FunctionCall, FunctionExecutionResult # For example output parsing

except ImportError as e:
    print(f\"Note: Some imports failed, likely due to missing packages: {e}\")
    # Define dummy classes/functions if needed for the script to be syntactically valid
    class Dummy: pass
    AssistantAgent = Dummy
    TaskResult = Dummy
    ExternalTermination = Dummy
    TextMentionTermination = Dummy
    TextMessageTermination = Dummy
    RoundRobinGroupChat = Dummy
    Console = Dummy
    CancellationToken = Dummy
    OpenAIChatCompletionClient = Dummy
    TextMessage = Dummy
    ToolCallRequestEvent = Dummy
    ToolCallExecutionEvent = Dummy
    ToolCallSummaryMessage = Dummy
    RequestUsage = Dummy
    FunctionCall = Dummy
    FunctionExecutionResult = Dummy


# --- Creating a Team (RoundRobinGroupChat) ---
print(\"--- Creating a Team Example ---\")
try:
    # Create an OpenAI model client.
    model_client = OpenAIChatCompletionClient(
        model=\"gpt-4o-2024-08-06\",
        # api_key=\"sk-...\", # Optional if OPENAI_API_KEY env var is set.
    )
    print(\"Model client created.\")

    # Create the primary agent.
    primary_agent = AssistantAgent(
        \"primary\",
        model_client=model_client,
        system_message=\"You are a helpful AI assistant.\",
    )
    print(f\"Created agent: {primary_agent.name}\")

    # Create the critic agent.
    critic_agent = AssistantAgent(
        \"critic\",
        model_client=model_client,
        system_message=\"Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.\",
    )
    print(f\"Created agent: {critic_agent.name}\")

    # Define a termination condition that stops the task if the critic approves.
    text_termination = TextMentionTermination(\"APPROVE\")
    print(\"Created TextMentionTermination condition.\")

    # Create a team with the primary and critic agents.
    team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination)
    print(f\"Created RoundRobinGroupChat team with agents: {[a.name for a in team.agents]}\")

except Exception as e:
    print(f\"Error during team creation: {e}\")
    team = None # Ensure team is None if creation failed


# --- Running a Team ---
print(\"\\n--- Running a Team Example ---\")
async def run_team_example():
    if not team:
        print(\"Team creation failed. Skipping run example.\")
        return
    print(\"Running team.run()...\")
    try:
        # Use `asyncio.run(...)` when running in a script.
        result = await team.run(task=\"Write a short poem about the fall season.\")
        print(\"Team run finished. Result:\")
        # print(result) # Print the full TaskResult object
        print(f\"Stop Reason: {result.stop_reason}\")
        print(f\"Number of messages: {len(result.messages)}\")
        print(\"(Actual output depends on live model calls)\")
    except Exception as e:
        print(f\"Error during team.run: {e}\")

# Example execution
# asyncio.run(run_team_example())
print(\"(Skipping actual execution of run_team_example in this script)\")


# --- Observing a Team (run_stream) ---
print(\"\\n--- Observing a Team (run_stream) Example 1 ---")
async def observe_team_stream_manual():
    if not team:
        print(\"Team creation failed. Skipping observe example.\")
        return
    print(\"Running team.run_stream() and manually printing messages...\")
    try:
        await team.reset()  # Reset the team for a new task.
        print(\"Team reset.\")
        async for message in team.run_stream(task=\"Write a short poem about the fall season.\"):
            if isinstance(message, TaskResult):
                print(\"\\n--- End of Stream ---")
                print(f\"Stop Reason: {message.stop_reason}\")
                print(f\"Final TaskResult: {message}\")
            else:
                # Print basic info about the message
                print(f\"Stream Message: Type={type(message).__name__}, Source={getattr(message, 'source', 'N/A')}, Content Snippet='{str(getattr(message, 'content', 'N/A'))[:50]}...'\" )
        print(\"(Actual output depends on live model calls)\")
    except Exception as e:
        print(f\"Error during team.run_stream (manual print): {e}\")

# Example execution
# asyncio.run(observe_team_stream_manual())
print(\"(Skipping actual execution of observe_team_stream_manual in this script)\")


print(\"\\n--- Observing a Team (run_stream) Example 2 (Console) ---")
async def observe_team_stream_console():
    if not team:
        print(\"Team creation failed. Skipping observe example.\")
        return
    print(\"Running team.run_stream() with Console...\")
    try:
        await team.reset()  # Reset the team for a new task.
        print(\"Team reset.\")
        await Console(team.run_stream(task=\"Write a short poem about the fall season.\"))  # Stream the messages to the console.
        print(\"\\n(Console output depends on live model calls)\")
    except Exception as e:
        print(f\"Error during team.run_stream (Console): {e}\")

# Example execution
# asyncio.run(observe_team_stream_console())
print(\"(Skipping actual execution of observe_team_stream_console in this script)\")


# --- Resetting a Team ---
print(\"\\n--- Resetting a Team Example ---\")
async def reset_team_example():
    if not team:
        print(\"Team creation failed. Skipping reset example.\")
        return
    try:
        print(\"Resetting team...\")
        await team.reset()
        print(\"Team has been reset.\")
    except Exception as e:
        print(f\"Error during team.reset: {e}\")

# Example execution
# asyncio.run(reset_team_example())
print(\"(Skipping actual execution of reset_team_example in this script)\")


# --- Stopping a Team (ExternalTermination) ---
print(\"\\n--- Stopping a Team Example ---\")
async def stop_team_example():
    if not team or not primary_agent or not critic_agent or not text_termination:
         print(\"Team/Agent creation failed or condition missing. Skipping stop example.\")
         return
    print(\"Setting up team with ExternalTermination...\")
    try:
        # Create a new team with an external termination condition.
        external_termination = ExternalTermination()
        stoppable_team = RoundRobinGroupChat(
            [primary_agent, critic_agent],
            termination_condition=external_termination | text_termination,  # Use the bitwise OR operator
        )
        print(\"Created stoppable team.\")

        # Run the team in a background task.
        print(\"Starting team run in background task...\")
        run_task = asyncio.create_task(Console(stoppable_team.run_stream(task=\"Write a short poem about the fall season.\")))

        # Wait for some time.
        print(\"Waiting briefly...\")
        await asyncio.sleep(2) # Increased sleep time slightly

        # Stop the team.
        print(\"Setting external termination...\")
        external_termination.set()

        # Wait for the team to finish.
        print(\"Waiting for background task to complete...\")
        await run_task
        print(\"Team run completed after external termination request.\")
        print(\"(Actual output depends on live model calls and timing)\")

    except Exception as e:
        print(f\"Error during external termination example: {e}\")

# Example execution
# asyncio.run(stop_team_example())
print(\"(Skipping actual execution of stop_team_example in this script)\")


# --- Resuming a Team ---
print(\"\\n--- Resuming a Team Example ---")
# Assuming 'stoppable_team' might exist from the previous example, or recreate 'team' if needed
# For simplicity, let's assume 'team' exists and might have state from a previous run.
async def resume_team_example():
    if not team:
        print(\"Team creation failed. Skipping resume example.\")
        return
    print(\"Attempting to resume team without new task (requires prior state)...\")
    try:
        # Ensure team has some state to resume from (e.g., run it partially first if needed)
        # For this script, we'll just call resume, it might not do much without prior state.
        await Console(team.run_stream())  # Resume the team to continue the last task.
        print(\"\\n(Console output depends on prior team state and live model calls)\")

        print(\"\\nAttempting to resume team with a new related task...\")
        # The new task is to translate the same poem to Chinese Tang-style poetry.
        await Console(team.run_stream(task=\"将这首诗用中文唐诗风格写一遍。\"))
        print(\"\\n(Console output depends on prior team state and live model calls)\")
    except Exception as e:
        print(f\"Error during team resume example: {e}\")

# Example execution
# asyncio.run(resume_team_example())
print(\"(Skipping actual execution of resume_team_example in this script)\")


# --- Aborting a Team (CancellationToken) ---
print(\"\\n--- Aborting a Team Example ---")
async def abort_team_example():
    if not team:
        print(\"Team creation failed. Skipping abort example.\")
        return
    print(\"Setting up team run with CancellationToken...\")
    try:
        # Create a cancellation token.
        cancellation_token = CancellationToken()

        # Use another coroutine to run the team.
        print(\"Starting team run in background task...\")
        run_abort_task = asyncio.create_task(
            team.run(
                task=\"Translate the poem to Spanish.\",
                cancellation_token=cancellation_token,
            )
        )

        # Wait briefly then cancel
        await asyncio.sleep(0.5)
        print(\"Cancelling the task via CancellationToken...\")
        cancellation_token.cancel()

        try:
            result = await run_abort_task  # This should raise a CancelledError.
            print(f\"Task completed unexpectedly with result: {result}\")
        except asyncio.CancelledError:
            print(\"Task was successfully cancelled as expected.\")
        except Exception as e_inner:
            print(f\"Unexpected error waiting for cancelled task: {e_inner}\")

    except Exception as e:
        print(f\"Error during cancellation token example setup: {e}\")

# Example execution
# asyncio.run(abort_team_example())
print(\"(Skipping actual execution of abort_team_example in this script)\")


# --- Single-Agent Team ---
print(\"\\n--- Single-Agent Team Example ---")
async def single_agent_team_example():
    print(\"Setting up single-agent team...\")
    try:
        single_agent_model_client = OpenAIChatCompletionClient(
            model=\"gpt-4o\",
            # api_key=\"sk-...\",
            parallel_tool_calls=False, # Disabled for this example
        )
        print(\"Single-agent model client created.\")

        # Create a tool for incrementing a number.
        def increment_number(number: int) -> int:
            \"\"\"Increment a number by 1.\"\"\"
            print(f\"[Tool Call] increment_number(number={number})\")
            return number + 1

        # Create a tool agent that uses the increment_number function.
        looped_assistant = AssistantAgent(
            \"looped_assistant\",
            model_client=single_agent_model_client,
            tools=[increment_number],
            system_message=\"You are a helpful AI assistant, use the tool to increment the number.\",
        )
        print(f\"Created agent: {looped_assistant.name}\")

        # Termination condition that stops the task if the agent responds with a text message.
        termination_condition_single = TextMessageTermination(agent_name=\"looped_assistant\")
        print(\"Created TextMessageTermination condition.\")

        # Create a team with the looped assistant agent and the termination condition.
        single_agent_team = RoundRobinGroupChat(
            [looped_assistant],
            termination_condition=termination_condition_single,
        )
        print(\"Created single-agent RoundRobinGroupChat team.\")

        # Run the team with a task and print the messages to the console.
        print(\"Running single-agent team...\")
        async for message in single_agent_team.run_stream(task=\"Increment the number 5 to 10.\"):
             print(f\"Single-Agent Stream: Type={type(message).__name__}, Source={getattr(message, 'source', 'N/A')}, Content Snippet='{str(getattr(message, 'content', 'N/A'))[:80]}...'\" )
        print(\"\\n(Actual output depends on live model calls)\")

        await single_agent_model_client.close()
        print(\"Single-agent model client closed.\")

    except Exception as e:
        print(f\"Error during single-agent team example: {e}\")

# Example execution
# asyncio.run(single_agent_team_example())
print(\"(Skipping actual execution of single_agent_team_example in this script)\")


# --- Close Main Model Client ---
# Ensure the main client used in multi-agent examples is closed if it was created
async def close_main_client():
    if 'model_client' in globals() and hasattr(model_client, 'close'):
         print(\"\\nClosing main model client...\")
         try:
            await model_client.close()
            print(\"Main model client closed.\")
         except Exception as e:
            print(f\"Error closing main model client: {e}\")

# Example execution
# asyncio.run(close_main_client())
print(\"(Skipping actual execution of close_main_client in this script)\")
