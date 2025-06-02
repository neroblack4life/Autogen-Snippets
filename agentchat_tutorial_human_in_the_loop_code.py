# Code snippets from AgentChat Tutorial - Human-in-the-Loop Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/human-in-the-loop.html)

import asyncio

# Assuming necessary autogen imports are present from previous steps or installed
try:
    from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
    from autogen_agentchat.conditions import TextMentionTermination, HandoffTermination
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_agentchat.base import Handoff # For Handoff example
    # For FastAPI example context
    from autogen_agentchat.messages import TextMessage
    from autogen_core import CancellationToken
    # For example output parsing
    from autogen_agentchat.base import TaskResult
    from autogen_core.models import RequestUsage
    from autogen_agentchat.events import UserInputRequestedEvent
    from autogen_core.tool_runtime import FunctionCall, FunctionExecutionResult
    from autogen_agentchat.messages import ToolCallRequestEvent, ToolCallExecutionEvent, HandoffMessage

except ImportError as e:
    print(f\"Note: Some imports failed, likely due to missing packages: {e}\")
    # Define dummy classes/functions if needed
    class Dummy: pass
    AssistantAgent = Dummy
    UserProxyAgent = Dummy
    TextMentionTermination = Dummy
    HandoffTermination = Dummy
    RoundRobinGroupChat = Dummy
    Console = Dummy
    OpenAIChatCompletionClient = Dummy
    Handoff = Dummy
    TextMessage = Dummy
    CancellationToken = Dummy
    TaskResult = Dummy
    RequestUsage = Dummy
    UserInputRequestedEvent = Dummy
    FunctionCall = Dummy
    FunctionExecutionResult = Dummy
    ToolCallRequestEvent = Dummy
    ToolCallExecutionEvent = Dummy
    HandoffMessage = Dummy


# --- Providing Feedback During a Run (UserProxyAgent) ---
print(\"--- UserProxyAgent Example ---\")
async def run_user_proxy_example():
    print(\"Setting up UserProxyAgent example...\")
    try:
        # Create the agents.
        model_client_proxy = OpenAIChatCompletionClient(model=\"gpt-4o-mini\") # Using mini for potentially faster/cheaper run
        assistant = AssistantAgent(\"assistant\", model_client=model_client_proxy)
        # NOTE: Using input() will block execution in non-interactive environments.
        # Replace with a suitable function or mock for automated runs.
        # For this script, we'll mock it to avoid blocking.
        def mock_input(prompt: str) -> str:
            print(f\"[User Input Prompt]: {prompt}\")
            print(\"[Mock Input]: APPROVE\") # Simulate user approving
            return \"APPROVE\"
        user_proxy = UserProxyAgent(\"user_proxy\", input_func=mock_input)

        # Create the termination condition.
        termination = TextMentionTermination(\"APPROVE\")

        # Create the team.
        team_with_proxy = RoundRobinGroupChat([assistant, user_proxy], termination_condition=termination)
        print(\"Created team with UserProxyAgent.\")

        # Run the conversation and stream to the console.
        print(\"Running team with UserProxyAgent...\")
        stream = team_with_proxy.run_stream(task=\"Write a 4-line poem about the ocean.\")
        await Console(stream)
        print(\"\\n(Console output depends on live model calls and mock input)\")
        await model_client_proxy.close()
        print(\"Model client closed.\")

    except Exception as e:
        print(f\"Error during UserProxyAgent example: {e}\")

# Example execution
# asyncio.run(run_user_proxy_example())
print(\"(Skipping actual execution of run_user_proxy_example in this script)\")


# --- Custom Input Function (Conceptual FastAPI Example) ---
# This is conceptual and requires a running FastAPI app (`app`) and WebSocket connection (`websocket`)
# @app.websocket(\"/ws/chat\")
# async def chat(websocket: WebSocket):
#     await websocket.accept()
#
#     async def _user_input(prompt: str, cancellation_token: CancellationToken | None) -> str:
#         print(f\"[WebSocket Prompt to User]: {prompt}\") # Simulate sending prompt
#         # In a real app, you'd send the prompt over the websocket and wait for a response
#         # data = await websocket.receive_json() # Wait for user message from websocket.
#         # For demonstration, simulate receiving a response:
#         data = {\"content\": \"User feedback via WebSocket\", \"source\": \"User\", \"type\": \"TextMessage\"}
#         print(f\"[WebSocket Received Data]: {data}\")
#         message = TextMessage.model_validate(data) # Assume user message is a TextMessage.
#         return message.content
#
#     # Create user proxy with custom input function
#     # custom_user_proxy = UserProxyAgent(\"websocket_user\", input_func=_user_input)
#     # Run the team with the custom_user_proxy
#     # ... (rest of team setup and run logic)
print(\"\\n--- Custom Input Function (Conceptual FastAPI) ---")
print(\"(See code comments for conceptual structure)\")


# --- Providing Feedback Between Runs: Using Max Turns ---
print(\"\\n--- Max Turns Example ---\")
async def run_max_turns_example():
    print(\"Setting up max_turns example...\")
    try:
        model_client_max_turns = OpenAIChatCompletionClient(model=\"gpt-4o-mini\")
        assistant_max_turns = AssistantAgent(\"assistant\", model_client=model_client_max_turns)
        print(\"Created assistant agent.\")

        # Create the team setting a maximum number of turns to 1.
        team_max_turns = RoundRobinGroupChat([assistant_max_turns], max_turns=1)
        print(\"Created team with max_turns=1.\")

        task = \"Write a 4-line poem about the ocean.\"
        turn_count = 0
        max_interactive_turns = 2 # Limit interaction for this script

        # Simulate interactive loop
        while turn_count < max_interactive_turns:
            turn_count += 1
            print(f\"\\n--- Interactive Turn {turn_count} ---")
            print(f\"Running team with task: '{task}'\")
            # Run the conversation and stream to the console.
            stream = team_max_turns.run_stream(task=task)
            await Console(stream)
            print(\"(Console output depends on live model calls)\")

            # Get the user response (mocked)
            # task = input(\"Enter your feedback (type 'exit' to leave): \")
            if turn_count < max_interactive_turns:
                 mock_feedback = f\"Mock feedback for turn {turn_count + 1}\"
                 print(f\"[User Input Prompt]: Enter your feedback (type 'exit' to leave):\")
                 print(f\"[Mock Input]: {mock_feedback}\")
                 task = mock_feedback
            else:
                 print(\"[Mock Input]: exit\")
                 task = \"exit\"

            if task.lower().strip() == \"exit\":
                print(\"Exiting interactive loop.\")
                break
            # Task for the next iteration is the user feedback

        await model_client_max_turns.close()
        print(\"Model client closed.\")

    except Exception as e:
        print(f\"Error during max_turns example: {e}\")

# Example execution
# asyncio.run(run_max_turns_example())
print(\"(Skipping actual execution of run_max_turns_example in this script)\")


# --- Providing Feedback Between Runs: Using HandoffTermination ---
print(\"\\n--- HandoffTermination Example ---\")
async def run_handoff_example():
    print(\"Setting up HandoffTermination example...\")
    lazy_agent_team = None # Define in outer scope
    try:
        # Create an OpenAI model client.
        model_client_handoff = OpenAIChatCompletionClient(
            model=\"gpt-4o\", # Needs tool use capability
            # api_key=\"sk-...\",
        )
        print(\"Model client created.\")

        # Create a lazy assistant agent that always hands off to the user.
        lazy_agent = AssistantAgent(
            \"lazy_assistant\",
            model_client=model_client_handoff,
            handoffs=[Handoff(target=\"user\", message=\"Transfer to user.\")],
            system_message=\"If you cannot complete the task, transfer to user. Otherwise, when finished, respond with 'TERMINATE'.\",
        )
        print(f\"Created agent: {lazy_agent.name}\")

        # Define termination conditions.
        handoff_termination = HandoffTermination(target=\"user\")
        text_termination_handoff = TextMentionTermination(\"TERMINATE\")
        print(\"Created termination conditions.\")

        # Create a single-agent team.
        lazy_agent_team = RoundRobinGroupChat(
            [lazy_agent],
            termination_condition=handoff_termination | text_termination_handoff
        )
        print(\"Created single-agent team with handoff.\")

        # Run the team (expecting handoff).
        task1 = \"What is the weather in New York?\"
        print(f\"\\nRunning team with task: '{task1}' (expecting handoff)...")
        await Console(lazy_agent_team.run_stream(task=task1), output_stats=True)
        print(\"(Console output depends on live model calls)\")

        # Resume the team providing the needed info.
        task2 = \"The weather in New York is sunny.\"
        print(f\"\\nResuming team with task: '{task2}' (providing info)...\")
        await Console(lazy_agent_team.run_stream(task=task2))
        print(\"(Console output depends on live model calls)\")

        await model_client_handoff.close()
        print(\"Model client closed.\")

    except Exception as e:
        print(f\"Error during HandoffTermination example: {e}\")
        # Ensure client is closed even if error occurs mid-way
        if 'model_client_handoff' in locals() and hasattr(model_client_handoff, 'close'):
            try:
                await model_client_handoff.close()
                print(\"Model client closed after error.\")
            except Exception as close_e:
                print(f\"Error closing model client after error: {close_e}\")

# Example execution
# asyncio.run(run_handoff_example())
print(\"(Skipping actual execution of run_handoff_example in this script)\")
