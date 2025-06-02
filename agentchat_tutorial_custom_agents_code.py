# Code snippets from AgentChat Tutorial - Custom Agents Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/custom-agents.html)

import asyncio
import os
from typing import AsyncGenerator, List, Sequence, Callable

# Assuming necessary autogen imports are present
try:
    from autogen_agentchat.agents import BaseChatAgent, AssistantAgent # Added AssistantAgent
    from autogen_agentchat.base import Response
    from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, TextMessage
    from autogen_core import CancellationToken, Component
    from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination # Added TextMentionTermination
    from autogen_agentchat.teams import SelectorGroupChat, RoundRobinGroupChat # Added RoundRobinGroupChat
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    # For Gemini example
    from autogen_core.model_context import UnboundedChatCompletionContext
    from autogen_core.models import AssistantMessage, RequestUsage, UserMessage
    # For Component example
    from pydantic import BaseModel # Requires pydantic
    from typing_extensions import Self # Requires typing_extensions
    # For example output parsing
    from autogen_agentchat.base import TaskResult
except ImportError as e:
    print(f\"Note: Some imports failed, likely due to missing packages: {e}\")
    # Define dummy classes/functions if needed
    class Dummy: pass
    BaseChatAgent = Dummy
    AssistantAgent = Dummy
    Response = Dummy
    BaseAgentEvent = Dummy
    BaseChatMessage = Dummy
    TextMessage = Dummy
    CancellationToken = Dummy
    Component = object
    MaxMessageTermination = Dummy
    TextMentionTermination = Dummy
    SelectorGroupChat = Dummy
    RoundRobinGroupChat = Dummy
    Console = Dummy
    OpenAIChatCompletionClient = Dummy
    UnboundedChatCompletionContext = Dummy
    AssistantMessage = Dummy
    RequestUsage = Dummy
    UserMessage = Dummy
    BaseModel = object
    Self = None
    TaskResult = Dummy

# Try importing google-genai, fail gracefully
try:
    import google.genai as genai
    from google.genai import types as genai_types
    GEMINI_SDK_AVAILABLE = True
except ImportError:
    print(\"Note: google-genai SDK not found. Gemini examples will not fully function.\")
    GEMINI_SDK_AVAILABLE = False
    # Dummy classes for genai if needed for syntax
    class DummyGenAIClient:
        class DummyModels:
            def generate_content(self, *args, **kwargs):
                class DummyResponse:
                    text = \"Dummy Gemini Response\"
                    class DummyUsage:
                        prompt_token_count = 10
                        candidates_token_count = 5
                    usage_metadata = DummyUsage()
                return DummyResponse()
        models = DummyModels()
    genai = Dummy()
    genai.Client = lambda api_key: DummyGenAIClient()
    genai_types = Dummy()
    genai_types.GenerateContentConfig = lambda **kwargs: None


# --- Example 1: CountDownAgent ---
print(\"--- CountDownAgent Example ---\")
class CountDownAgent(BaseChatAgent):
    def __init__(self, name: str, count: int = 3):
        super().__init__(name, \"A simple agent that counts down.\")
        self._count = count

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        return (TextMessage,)

    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        response: Response | None = None
        async for message in self.on_messages_stream(messages, cancellation_token):
            if isinstance(message, Response):
                response = message
        assert response is not None, \"Stream did not yield a final Response\"
        return response

    async def on_messages_stream(
        self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken
    ) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | Response, None]:
        inner_messages: List[BaseAgentEvent | BaseChatMessage] = []
        for i in range(self._count, 0, -1):
            # Check for cancellation
            if cancellation_token.is_cancelled:
                print(\"Countdown cancelled.\")
                # Optionally yield a specific cancellation message or just stop
                return
            msg = TextMessage(content=f\"{i}...\", source=self.name)
            inner_messages.append(msg)
            yield msg
            await asyncio.sleep(0.1) # Small delay for demonstration

        yield Response(chat_message=TextMessage(content=\"Done!\", source=self.name), inner_messages=inner_messages)

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        print(f\"Resetting {self.name}\")
        pass # No state to reset in this simple example

async def run_countdown_agent() -> None:
    print(\"Running CountDownAgent...\")
    countdown_agent = CountDownAgent(\"countdown\", count=5)
    async for message in countdown_agent.on_messages_stream([], CancellationToken()):
        if isinstance(message, Response):
            print(f\"Final Response: {message.chat_message}\")
        else:
            print(f\"Stream Message: {message}\")

# Example execution
# asyncio.run(run_countdown_agent())
print(\"(Skipping actual execution of run_countdown_agent in this script)\")


# --- Example 2: ArithmeticAgent ---
print(\"\\n--- ArithmeticAgent Example ---\")
class ArithmeticAgent(BaseChatAgent):
    def __init__(self, name: str, description: str, operator_func: Callable[[int], int]) -> None:
        super().__init__(name, description=description)
        self._operator_func = operator_func
        self._message_history: List[BaseChatMessage] = []

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        return (TextMessage,)

    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        print(f\"Agent {self.name} received {len(messages)} new messages.\")
        self._message_history.extend(messages)
        if not self._message_history:
             # Should not happen if called correctly by a team, but handle defensively
             raise ValueError(f\"Agent {self.name} has no message history to process.\")

        # Parse the number from the *last* message in history
        last_message = self._message_history[-1]
        if not isinstance(last_message, TextMessage):
             raise TypeError(f\"Agent {self.name} expected last message to be TextMessage, got {type(last_message)}\")
        try:
             number = int(last_message.content)
             print(f\"Agent {self.name} processing number: {number}\")
        except ValueError:
             raise ValueError(f\"Agent {self.name} could not parse integer from content: '{last_message.content}'\")

        # Apply the operator function
        result = self._operator_func(number)
        print(f\"Agent {self.name} produced result: {result}\")

        # Create and store the response message
        response_message = TextMessage(content=str(result), source=self.name)
        self._message_history.append(response_message)

        return Response(chat_message=response_message)

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        print(f\"Resetting {self.name}\")
        self._message_history = [] # Clear history on reset

async def run_number_agents() -> None:
    print(\"Setting up ArithmeticAgent team...\")
    try:
        # Create agents
        add_agent = ArithmeticAgent(\"add_agent\", \"Adds 1 to the number.\", lambda x: x + 1)
        multiply_agent = ArithmeticAgent(\"multiply_agent\", \"Multiplies the number by 2.\", lambda x: x * 2)
        subtract_agent = ArithmeticAgent(\"subtract_agent\", \"Subtracts 1 from the number.\", lambda x: x - 1)
        divide_agent = ArithmeticAgent(\"divide_agent\", \"Divides the number by 2 and rounds down.\", lambda x: x // 2)
        identity_agent = ArithmeticAgent(\"identity_agent\", \"Returns the number as is.\", lambda x: x)
        print(\"Arithmetic agents created.\")

        termination_condition = MaxMessageTermination(10)
        print(\"Termination condition created.\")

        model_client_selector = OpenAIChatCompletionClient(model=\"gpt-4o\")
        print(\"Selector model client created.\")

        # Create selector group chat
        selector_group_chat = SelectorGroupChat(
            [add_agent, multiply_agent, subtract_agent, divide_agent, identity_agent],
            model_client=model_client_selector,
            termination_condition=termination_condition,
            allow_repeated_speaker=True,
            selector_prompt=(
                \"Available roles:\\n{roles}\\nTheir job descriptions:\\n{participants}\\n\"
                \"Current conversation history:\\n{history}\\n\"
                \"Please select the most appropriate role for the next message, and only return the role name.\"
            ),
        )
        print(\"SelectorGroupChat created.\")

        # Define task
        task: List[BaseChatMessage] = [
            TextMessage(content=\"Apply the operations to turn the given number into 25.\", source=\"user\"),
            TextMessage(content=\"10\", source=\"user\"),
        ]
        print(\"Task defined.\")

        # Run the team
        print(\"\\nRunning ArithmeticAgent team...\")
        stream = selector_group_chat.run_stream(task=task)
        await Console(stream)
        print(\"\\n(Console output depends on live model calls for selector)\")

        await model_client_selector.close()
        print(\"Selector model client closed.\")

    except Exception as e:
        print(f\"Error during ArithmeticAgent example: {e}\")
        if 'model_client_selector' in locals() and hasattr(model_client_selector, 'close'):
            try: await model_client_selector.close(); print(\"Selector client closed after error.\")
            except: pass

# Example execution
# asyncio.run(run_number_agents())
print(\"(Skipping actual execution of run_number_agents in this script)\")


# --- Using Custom Model Clients (GeminiAssistantAgent) ---
print(\"\\n--- GeminiAssistantAgent Example ---\")
# Requires: pip install google-genai
# Requires GEMINI_API_KEY environment variable

class GeminiAssistantAgent(BaseChatAgent):
    def __init__(
        self,
        name: str,
        description: str = \"An agent that provides assistance using Gemini.\",
        model: str = \"gemini-1.5-flash\", # Updated model name if needed
        api_key: str | None = None,
        system_message: str | None = \"You are a helpful assistant. Reply with TERMINATE when done.\",
    ):
        super().__init__(name=name, description=description)
        if not GEMINI_SDK_AVAILABLE:
            raise ImportError(\"google-genai SDK not found. Cannot create GeminiAssistantAgent.\")
        if api_key is None:
            api_key = os.environ.get(\"GEMINI_API_KEY\")
        if not api_key:
            raise ValueError(\"GEMINI_API_KEY environment variable or api_key argument must be set.\")

        self._model_context = UnboundedChatCompletionContext()
        # Configure the client upon initialization
        genai.configure(api_key=api_key)
        # Get the generative model
        self._model_client = genai.GenerativeModel(model)
        self._system_message = system_message
        self._model_name = model # Store model name if needed later

    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]:
        return (TextMessage,)

    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        final_response = None
        async for message in self.on_messages_stream(messages, cancellation_token):
            if isinstance(message, Response):
                final_response = message
        if final_response is None: raise AssertionError(\"Stream did not yield a final Response\")
        return final_response

    async def on_messages_stream(
        self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken
    ) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | Response, None]:
        # Add messages to context
        for msg in messages:
            await self._model_context.add_message(msg.to_model_message())

        # Format history for Gemini (needs specific format, e.g., list of Content objects)
        # This part needs careful adaptation based on how google-genai expects history
        gemini_history = []
        for msg in await self._model_context.get_messages():
             role = \"user\" if isinstance(msg, UserMessage) else \"model\"
             # Simple text content for now, might need adjustment for multimodal
             content_text = msg.content if isinstance(msg.content, str) else str(msg.content)
             gemini_history.append({'role': role, 'parts': [{'text': content_text}]})

        # Start a chat session if needed, or generate directly
        # Using generate_content directly might be simpler if context is passed each time
        try:
            print(f\"Sending to Gemini: History Length={len(gemini_history)}\")
            # Adjust based on whether system message is supported directly or needs to be part of history
            generation_config = genai_types.GenerationConfig(temperature=0.3) if GEMINI_SDK_AVAILABLE else None
            # Safety settings might be needed
            # safety_settings = [...]

            # Construct the prompt/history correctly for the SDK version
            # Assuming the last message in history is the user prompt for this turn
            prompt_parts = gemini_history[-1]['parts'] if gemini_history else [{'text': '...'}] # Handle empty history
            history_for_gen = gemini_history[:-1] # History excluding the last prompt

            response = await self._model_client.generate_content_async(
                contents=history_for_gen + [{'role': 'user', 'parts': prompt_parts}], # Example structure
                generation_config=generation_config,
                # safety_settings=safety_settings,
                # system_instruction=self._system_message # If supported
            )

            response_text = response.text
            # Attempt to get usage - might not be available or named differently
            prompt_tokens = getattr(response, 'usage_metadata', {}).get('prompt_token_count', 0)
            completion_tokens = getattr(response, 'usage_metadata', {}).get('candidates_token_count', 0)

        except Exception as e:
            print(f\"Error calling Gemini API: {e}\")
            response_text = f\"Error interacting with Gemini: {e}\"
            prompt_tokens = 0
            completion_tokens = 0

        usage = RequestUsage(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens)

        # Add response to context
        await self._model_context.add_message(AssistantMessage(content=response_text, source=self.name))

        # Yield final response
        yield Response(
            chat_message=TextMessage(content=response_text, source=self.name, models_usage=usage),
            inner_messages=[],
        )

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        print(f\"Resetting {self.name}\")
        await self._model_context.clear()

async def run_gemini_agent_standalone():
    if not GEMINI_SDK_AVAILABLE:
        print(\"Skipping Gemini standalone run as SDK is not available.\")
        return
    print(\"\\nRunning GeminiAssistantAgent standalone...\")
    try:
        gemini_assistant = GeminiAssistantAgent(\"gemini_assistant_standalone\")
        await Console(gemini_assistant.run_stream(task=\"What is the capital of New York?\"))
    except Exception as e:
        print(f\"Error running Gemini standalone: {e}\")

# Example execution
# asyncio.run(run_gemini_agent_standalone())
print(\"(Skipping actual execution of run_gemini_agent_standalone in this script)\")


async def run_gemini_in_team():
    if not GEMINI_SDK_AVAILABLE:
        print(\"Skipping Gemini team run as SDK is not available.\")
        return
    print(\"\\nRunning GeminiAssistantAgent in a team...\")
    team_gemini = None
    try:
        model_client_openai = OpenAIChatCompletionClient(model=\"gpt-4o-mini\")
        print(\"OpenAI client created for primary agent.\")

        primary_agent = AssistantAgent(
            \"primary\", model_client=model_client_openai, system_message=\"You are a helpful AI assistant.\"
        )
        print(f\"Created agent: {primary_agent.name}\")

        gemini_critic_agent = GeminiAssistantAgent(
            \"gemini_critic\",
            system_message=\"Provide constructive feedback. Respond with 'APPROVE' when feedback is addressed.\",
        )
        print(f\"Created agent: {gemini_critic_agent.name}\")

        termination = TextMentionTermination(\"APPROVE\") | MaxMessageTermination(10)
        print(\"Termination condition created.\")

        team_gemini = RoundRobinGroupChat([primary_agent, gemini_critic_agent], termination_condition=termination)
        print(\"Created team with Gemini critic.\")

        print(\"\\nRunning team with Gemini critic...\")
        await Console(team_gemini.run_stream(task=\"Write a Haiku poem with 4 lines about the fall season.\"))
        print(\"\\n(Console output depends on live model calls)\")

        await model_client_openai.close()
        print(\"OpenAI client closed.\")
        # Note: Gemini client used by GeminiAssistantAgent doesn't have an explicit close method in this structure

    except Exception as e:
        print(f\"Error running Gemini in team: {e}\")
        if 'model_client_openai' in locals() and hasattr(model_client_openai, 'close'):
            try: await model_client_openai.close(); print(\"OpenAI client closed after error.\")
            except: pass

# Example execution
# asyncio.run(run_gemini_in_team())
print(\"(Skipping actual execution of run_gemini_in_team in this script)\")


# --- Making Custom Agent Declarative (Gemini Example) ---
print(\"\\n--- Making Gemini Agent Declarative Example ---\")

class GeminiAssistantAgentConfig(BaseModel):
    name: str
    description: str = \"An agent that provides assistance using Gemini.\"
    model: str = \"gemini-1.5-flash\" # Default model
    system_message: str | None = \"You are a helpful assistant. Reply with TERMINATE when done.\"

# Redefine GeminiAssistantAgent inheriting from Component
class GeminiAssistantAgent(BaseChatAgent, Component[GeminiAssistantAgentConfig]): # type: ignore[no-redef] - Intentional redefinition
    component_config_schema = GeminiAssistantAgentConfig
    # Define provider for loading, replace __main__ with actual module path if packaged
    component_provider_override = \"__main__.GeminiAssistantAgent\"

    def __init__(
        self,
        name: str,
        description: str = \"An agent that provides assistance using Gemini.\",
        model: str = \"gemini-1.5-flash\",
        api_key: str | None = None, # Allow api_key to be passed or use env var
        system_message: str | None = \"You are a helpful assistant. Reply with TERMINATE when done.\",
    ):
        super().__init__(name=name, description=description)
        if not GEMINI_SDK_AVAILABLE:
            raise ImportError(\"google-genai SDK not found. Cannot create GeminiAssistantAgent.\")
        if api_key is None:
            api_key = os.environ.get(\"GEMINI_API_KEY\")
        if not api_key:
            raise ValueError(\"GEMINI_API_KEY environment variable or api_key argument must be set.\")

        self._model_context = UnboundedChatCompletionContext()
        genai.configure(api_key=api_key)
        self._model_client = genai.GenerativeModel(model)
        self._system_message = system_message
        self._model_name = model # Store model name for config

    # --- Keep other methods like produced_message_types, on_messages, on_messages_stream, on_reset ---
    # (Copy implementations from the previous GeminiAssistantAgent class definition)
    @property
    def produced_message_types(self) -> Sequence[type[BaseChatMessage]]: return (TextMessage,) # Simplified
    async def on_messages(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> Response:
        # Simplified - copy full implementation from above if needed
        final_response = None; async for msg in self.on_messages_stream(messages, cancellation_token): final_response = msg if isinstance(msg, Response) else final_response; return final_response
    async def on_messages_stream(self, messages: Sequence[BaseChatMessage], cancellation_token: CancellationToken) -> AsyncGenerator[BaseAgentEvent | BaseChatMessage | Response, None]:
        # Simplified - copy full implementation from above if needed
        yield Response(chat_message=TextMessage(content=\"Dummy Declarative Gemini Response\", source=self.name))
    async def on_reset(self, cancellation_token: CancellationToken) -> None: await self._model_context.clear()
    # --- End of copied methods ---

    @classmethod
    def _from_config(cls, config: GeminiAssistantAgentConfig) -> Self:
        # Assumes API key is available via environment variable when loading from config
        print(f\"Loading GeminiAssistantAgent '{config.name}' from config.\")
        return cls(
            name=config.name,
            description=config.description,
            model=config.model,
            system_message=config.system_message
            # api_key is implicitly handled by __init__ using env var
        )

    def _to_config(self) -> GeminiAssistantAgentConfig:
        print(f\"Saving config for GeminiAssistantAgent '{self.name}'.\")
        return GeminiAssistantAgentConfig(
            name=self.name,
            description=self.description,
            model=self._model_name, # Use stored model name
            system_message=self._system_message,
        )

def run_declarative_gemini_example():
    if not GEMINI_SDK_AVAILABLE:
        print(\"Skipping declarative Gemini run as SDK is not available.\")
        return
    print(\"\\nRunning declarative Gemini agent example...\")
    try:
        gemini_assistant_decl = GeminiAssistantAgent(\"gemini_assistant_decl\")
        print(\"Created declarative Gemini agent instance.\")

        # Dump config
        config = gemini_assistant_decl.dump_component()
        print(\"\\nDumped Component Config (JSON):\")
        print(config.model_dump_json(indent=2))

        # Load from config
        # Need to ensure the class is registered or provider is correct if not in __main__
        print(\"\\nLoading agent from config...\")
        # Use the class method directly for loading
        loaded_agent = GeminiAssistantAgent.load_component(config)
        print(\"Agent loaded from config:\")
        print(loaded_agent)
        print(f\"Loaded agent name: {loaded_agent.name}\")
        # Verify config matches (optional)
        # assert loaded_agent.name == gemini_assistant_decl.name
        # assert loaded_agent._model_name == gemini_assistant_decl._model_name

    except Exception as e:
        print(f\"Error during declarative Gemini example: {e}\")

# Example execution
# run_declarative_gemini_example() # This is synchronous
print(\"(Skipping actual execution of run_declarative_gemini_example in this script)\")
