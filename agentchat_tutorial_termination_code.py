# Code snippets from AgentChat Tutorial - Termination Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/termination.html)

import asyncio
from typing import Sequence

# Assuming necessary autogen imports are present
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
    from autogen_agentchat.teams import RoundRobinGroupChat
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    # For custom condition example
    from autogen_agentchat.base import TerminatedException, TerminationCondition
    from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, StopMessage, ToolCallExecutionEvent
    from autogen_core import Component
    from pydantic import BaseModel # Requires pydantic
    from typing_extensions import Self # Requires typing_extensions
    # For example output parsing
    from autogen_agentchat.base import TaskResult
    from autogen_agentchat.messages import TextMessage
    from autogen_core.models import RequestUsage
    from autogen_core.tool_runtime import FunctionCall, FunctionExecutionResult
    from autogen_agentchat.messages import ToolCallRequestEvent, ToolCallSummaryMessage

except ImportError as e:
    print(f\"Note: Some imports failed, likely due to missing packages: {e}\")
    # Define dummy classes/functions if needed
    class Dummy: pass
    AssistantAgent = Dummy
    MaxMessageTermination = Dummy
    TextMentionTermination = Dummy
    RoundRobinGroupChat = Dummy
    Console = Dummy
    OpenAIChatCompletionClient = Dummy
    TerminatedException = Exception
    TerminationCondition = object
    BaseAgentEvent = Dummy
    BaseChatMessage = Dummy
    StopMessage = Dummy
    ToolCallExecutionEvent = Dummy
    Component = object
    BaseModel = object
    Self = None
    TaskResult = Dummy
    TextMessage = Dummy
    RequestUsage = Dummy
    FunctionCall = Dummy
    FunctionExecutionResult = Dummy
    ToolCallRequestEvent = Dummy
    ToolCallSummaryMessage = Dummy


# --- Basic Usage & Reset Example ---
print(\"--- Basic Usage & Reset Example ---\")
async def run_basic_termination_example():
    print(\"Setting up basic termination example...\")
    round_robin_team = None # Define in outer scope
    try:
        model_client_basic = OpenAIChatCompletionClient(
            model=\"gpt-4o\",
            temperature=1,
            # api_key=\"sk-...\",
        )
        print(\"Model client created.\")

        primary_agent = AssistantAgent(
            \"primary\", model_client=model_client_basic, system_message=\"You are a helpful AI assistant.\"
        )
        critic_agent = AssistantAgent(
            \"critic\", model_client=model_client_basic,
            system_message=\"Provide constructive feedback for every message. Respond with 'APPROVE' to when your feedbacks are addressed.\"
        )
        print(f\"Created agents: {primary_agent.name}, {critic_agent.name}\")

        max_msg_termination = MaxMessageTermination(max_messages=3)
        print(\"Created MaxMessageTermination(max_messages=3).\")

        round_robin_team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=max_msg_termination)
        print(\"Created team.\")

        print(\"\\nRunning team (first run, expect stop after 3 messages)...\")
        await Console(round_robin_team.run_stream(task=\"Write a unique, Haiku about the weather in Paris\"))
        print(\"\\n(Console output depends on live model calls)\")

        print(\"\\nResuming team (second run, expect stop after 3 more messages)...\")
        # The termination condition resets automatically between runs
        await Console(round_robin_team.run_stream())
        print(\"\\n(Console output depends on live model calls)\")

        await model_client_basic.close()
        print(\"Model client closed.\")

    except Exception as e:
        print(f\"Error during basic termination example: {e}\")
        if 'model_client_basic' in locals() and hasattr(model_client_basic, 'close'):
            try: await model_client_basic.close(); print(\"Model client closed after error.\")
            except: pass # Ignore errors during cleanup

# Example execution
# asyncio.run(run_basic_termination_example())
print(\"(Skipping actual execution of run_basic_termination_example in this script)\")


# --- Combining Termination Conditions (OR) ---
print(\"\\n--- Combining Conditions (OR) Example ---\")
async def run_combined_or_termination_example():
    print(\"Setting up combined (OR) termination example...\")
    round_robin_team_or = None
    try:
        # Recreate client and agents if needed, or reuse from previous example if run sequentially
        # Assuming model_client_basic, primary_agent, critic_agent exist from previous block
        if 'model_client_basic' not in locals() or 'primary_agent' not in locals() or 'critic_agent' not in locals():
             print(\"Required components not found, recreating...\")
             # Simplified recreation for brevity
             model_client_basic = OpenAIChatCompletionClient(model=\"gpt-4o\", temperature=1)
             primary_agent = AssistantAgent(\"primary\", model_client=model_client_basic, system_message=\"...\")
             critic_agent = AssistantAgent(\"critic\", model_client=model_client_basic, system_message=\"...\")


        max_msg_termination_or = MaxMessageTermination(max_messages=10)
        text_termination_or = TextMentionTermination(\"APPROVE\")
        combined_termination_or = max_msg_termination_or | text_termination_or # OR operator
        print(\"Created combined OR termination condition (max_messages=10 | 'APPROVE').\")

        round_robin_team_or = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=combined_termination_or)
        print(\"Created team with combined OR condition.\")

        print(\"\\nRunning team with combined OR condition...\")
        await Console(round_robin_team_or.run_stream(task=\"Write a unique, Haiku about the weather in Paris\"))
        print(\"\\n(Console output depends on live model calls - should stop on 'APPROVE' or after 10 messages)\")

        # Close client if it was recreated here
        # await model_client_basic.close()

    except Exception as e:
        print(f\"Error during combined OR termination example: {e}\")
        # Add cleanup if client was recreated

# Example execution
# asyncio.run(run_combined_or_termination_example())
print(\"(Skipping actual execution of run_combined_or_termination_example in this script)\")


# --- Combining Termination Conditions (AND) ---
print(\"\\n--- Combining Conditions (AND) Example ---")
# combined_termination_and = max_msg_termination & text_termination
print(\"(See code comments for AND combination logic: max_msg_termination & text_termination)\")


# --- Custom Termination Condition (FunctionCallTermination) ---
print(\"\\n--- Custom Termination Condition Example ---")

# Define the custom condition class
class FunctionCallTerminationConfig(BaseModel):
    function_name: str

class FunctionCallTermination(TerminationCondition, Component[FunctionCallTerminationConfig]):
    component_config_schema = FunctionCallTerminationConfig
    def __init__(self, function_name: str) -> None:
        self._terminated = False
        self._function_name = function_name
    @property
    def terminated(self) -> bool: return self._terminated
    async def __call__(self, messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> StopMessage | None:
        if self._terminated: raise TerminatedException(\"Termination condition has already been reached\")
        for message in messages:
            if isinstance(message, ToolCallExecutionEvent):
                for execution in message.content:
                    if execution.name == self._function_name:
                        self._terminated = True
                        return StopMessage(content=f\"Function '{self._function_name}' was executed.\", source=\"FunctionCallTermination\")
        return None
    async def reset(self) -> None: self._terminated = False
    def _to_config(self) -> FunctionCallTerminationConfig: return FunctionCallTerminationConfig(function_name=self._function_name)
    @classmethod
    def _from_config(cls, config: FunctionCallTerminationConfig) -> Self: return cls(function_name=config.function_name)

print(\"Defined custom FunctionCallTermination class.\")

# Define the tool function
def approve() -> None:
    \"\"\"Approve the message when all feedbacks have been addressed.\"\"\"
    print(\"[Tool Call] approve() called.\")
    pass

print(\"Defined approve() tool function.\")

async def run_custom_termination_example():
    print(\"Setting up custom termination example...\")
    round_robin_team_custom = None
    try:
        model_client_custom = OpenAIChatCompletionClient(
            model=\"gpt-4o\", # Needs tool use capability
            temperature=1,
            # api_key=\"sk-...\",
        )
        print(\"Model client created.\")

        # Create agents, critic has the 'approve' tool
        primary_agent_custom = AssistantAgent(
            \"primary\", model_client=model_client_custom, system_message=\"You are a helpful AI assistant.\"
        )
        critic_agent_custom = AssistantAgent(
            \"critic\", model_client=model_client_custom, tools=[approve],
            system_message=\"Provide constructive feedback. Use the approve tool to approve when all feedbacks are addressed.\"
        )
        print(f\"Created agents: {primary_agent_custom.name}, {critic_agent_custom.name} (with approve tool)\")

        # Create the custom termination condition
        function_call_termination = FunctionCallTermination(function_name=\"approve\")
        print(\"Created FunctionCallTermination condition for 'approve'.\")

        # Create the team
        round_robin_team_custom = RoundRobinGroupChat(
            [primary_agent_custom, critic_agent_custom],
            termination_condition=function_call_termination
        )
        print(\"Created team with custom termination condition.\")

        print(\"\\nRunning team with custom termination condition...\")
        await Console(round_robin_team_custom.run_stream(task=\"Write a unique, Haiku about the weather in Paris\"))
        print(\"\\n(Console output depends on live model calls - should stop when approve() is called)\")

        await model_client_custom.close()
        print(\"Model client closed.\")

    except Exception as e:
        print(f\"Error during custom termination example: {e}\")
        if 'model_client_custom' in locals() and hasattr(model_client_custom, 'close'):
            try: await model_client_custom.close(); print(\"Model client closed after error.\")
            except: pass

# Example execution
# asyncio.run(run_custom_termination_example())
print(\"(Skipping actual execution of run_custom_termination_example in this script)\")

# --- Close Main Model Client (if reused) ---
# Ensure the main client used across examples is closed if it exists and wasn't closed yet
async def close_reused_client():
    if 'model_client_basic' in globals() and hasattr(model_client_basic, 'close'):
         # Check if already closed or doesn't need closing (e.g., dummy)
         # This check is basic; real applications might need better state tracking
         if getattr(model_client_basic, '_closed', False) is False:
             print(\"\\nClosing potentially reused model client...\")
             try:
                 await model_client_basic.close()
                 print(\"Reused model client closed.\")
             except Exception as e:
                 print(f\"Error closing reused model client: {e}\")

# Example execution
# asyncio.run(close_reused_client())
print(\"(Skipping actual execution of close_reused_client in this script)\")
