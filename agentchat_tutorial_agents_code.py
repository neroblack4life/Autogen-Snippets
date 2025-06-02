# Code snippets from AgentChat Tutorial - Agents Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/agents.html)

import asyncio # Added import
from io import BytesIO
import PIL # Requires Pillow: pip install Pillow
import requests # Requires requests: pip install requests
import pandas as pd # Requires pandas: pip install pandas

# Assuming necessary autogen imports are present from previous steps or installed
try:
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.messages import StructuredMessage, TextMessage, MultiModalMessage
    from autogen_agentchat.ui import Console
    from autogen_core import CancellationToken, Image
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    from autogen_core.tools import FunctionTool
    from autogen_ext.tools.mcp import StdioServerParams, mcp_server_tools
    from autogen_ext.tools.langchain import LangChainToolAdapter
    from autogen_core.model_context import BufferedChatCompletionContext
    from pydantic import BaseModel # Requires pydantic: pip install pydantic
    from typing import Literal
    # For langchain example
    from langchain_experimental.tools.python.tool import PythonAstREPLTool # Requires langchain-experimental
except ImportError as e:
    print(f\"Note: Some imports failed, likely due to missing packages: {e}\")
    # Define dummy classes/functions if needed for the script to be syntactically valid
    class Dummy: pass
    AssistantAgent = Dummy
    TextMessage = Dummy
    MultiModalMessage = Dummy
    StructuredMessage = Dummy
    Console = Dummy
    CancellationToken = Dummy
    Image = Dummy
    OpenAIChatCompletionClient = Dummy
    FunctionTool = Dummy
    StdioServerParams = Dummy
    mcp_server_tools = None # Cannot easily dummy async function
    LangChainToolAdapter = Dummy
    BufferedChatCompletionContext = Dummy
    BaseModel = object # Use object to allow subclassing
    Literal = None
    PythonAstREPLTool = Dummy


# --- Assistant Agent Initialization ---
print(\"--- Assistant Agent Initialization Example ---\")
# Define a tool that searches the web for information.
async def web_search(query: str) -> str:
    \"\"\"Find information on the web\"\"\"
    # Replace with actual web search implementation if desired
    print(f\"[Tool Call] web_search(query='{query}')\")
    return \"AutoGen is a programming framework for building multi-agent applications.\"

# Create an agent that uses the OpenAI GPT-4o model.
try:
    model_client = OpenAIChatCompletionClient(
        model=\"gpt-4o\",
        # api_key=\"YOUR_API_KEY\", # Set OPENAI_API_KEY env var or pass key here
    )
except Exception as e:
    print(f\"Failed to create OpenAI client: {e}. Using dummy client.\")
    class DummyClient:
        async def close(self): pass
    model_client = DummyClient()


agent = AssistantAgent(
    name=\"assistant\",
    model_client=model_client,
    tools=[web_search],
    system_message=\"Use tools to solve tasks.\",
)
print(f\"Created agent: {agent.name}\")

# --- Getting Responses (on_messages) ---
print(\"\\n--- Getting Responses (on_messages) Example ---\")
async def assistant_run() -> None:
    print(\"Running agent.on_messages...\")
    try:
        response = await agent.on_messages(
            [TextMessage(content=\"Find information on AutoGen\", source=\"user\")],
            cancellation_token=CancellationToken(),
        )
        print(\"Inner Messages (Thought Process):\")
        # The actual output depends on the model interaction
        # print(response.inner_messages)
        print(\"Final Chat Message:\")
        # print(response.chat_message)
        print(\"(Actual output depends on live model call)\")
    except Exception as e:
        print(f\"Error during agent.on_messages: {e}\")

# Example execution (requires running event loop)
# asyncio.run(assistant_run())
print(\"(Skipping actual execution of assistant_run in this script)\")


# --- Multi-Modal Input ---
print(\"\\n--- Multi-Modal Input Example ---\")
try:
    # Create a multi-modal message with random image and text.
    pil_image_multi = PIL.Image.open(BytesIO(requests.get(\"https://picsum.photos/300/200\").content))
    img_multi = Image(pil_image_multi)
    multi_modal_message = MultiModalMessage(content=[\"Can you describe the content of this image?\", img_multi], source=\"user\")
    print(\"Created MultiModalMessage.\")
    # img_multi # Display image if in suitable environment

    async def run_multimodal():
        print(\"Running agent.on_messages with MultiModalMessage...\")
        try:
            response_multi = await agent.on_messages([multi_modal_message], CancellationToken())
            print(\"Multi-Modal Response Chat Message:\")
            # print(response_multi.chat_message)
            print(\"(Actual output depends on live model call)\")
        except Exception as e:
            print(f\"Error during multi-modal agent.on_messages: {e}\")

    # Example execution
    # asyncio.run(run_multimodal())
    print(\"(Skipping actual execution of run_multimodal in this script)\")

except Exception as e:
    print(f\"Error creating multi-modal message: {e}\")


# --- Streaming Messages (on_messages_stream) ---
print(\"\\n--- Streaming Messages Example ---\")
async def assistant_run_stream() -> None:
    print(\"Running agent.on_messages_stream with Console...\")
    try:
        # Option 2: use Console to print all messages as they appear.
        await Console(
            agent.on_messages_stream(
                [TextMessage(content=\"Find information on AutoGen\", source=\"user\")],
                cancellation_token=CancellationToken(),
            ),
            output_stats=True,  # Enable stats printing.
        )
        print(\"(Actual output depends on live model call)\")
    except Exception as e:
        print(f\"Error during agent.on_messages_stream: {e}\")

# Example execution
# asyncio.run(assistant_run_stream())
print(\"(Skipping actual execution of assistant_run_stream in this script)\")


# --- Using Tools: Function Tool ---
print(\"\\n--- Function Tool Example ---\")
# Define a tool using a Python function.
async def web_search_func(query: str) -> str:
    \"\"\"Find information on the web\"\"\"
    print(f\"[Tool Call] web_search_func(query='{query}')\")
    return \"AutoGen is a programming framework for building multi-agent applications.\"

# This step is automatically performed inside the AssistantAgent if the tool is a Python function.
web_search_function_tool = FunctionTool(web_search_func, description=\"Find information on the web\")
# The schema is provided to the model during AssistantAgent's on_messages call.
print(\"Generated Schema for web_search_func:\")
print(web_search_function_tool.schema)


# --- Using Tools: MCP Tools ---
print(\"\\n--- MCP Tools Example ---\")
async def run_mcp_tool_example():
    print(\"Setting up MCP tool example...\")
    if mcp_server_tools is None:
        print(\"mcp_server_tools not available (import failed?). Skipping MCP example.\")
        return
    try:
        # Get the fetch tool from mcp-server-fetch (requires mcp-server-fetch installed and runnable via uvx)
        # Replace 'uvx' if needed, or provide full path
        fetch_mcp_server = StdioServerParams(command=\"uvx\", args=[\"mcp-server-fetch\"])
        print(\"Attempting to get tools from MCP server...\")
        tools = await mcp_server_tools(fetch_mcp_server)
        print(f\"Got tools from MCP server: {[t.name for t in tools]}\")

        # Create an agent that can use the fetch tool.
        mcp_agent = AssistantAgent(name=\"fetcher\", model_client=model_client, tools=tools, reflect_on_tool_use=True)

        # Let the agent fetch the content of a URL and summarize it.
        print(\"Running MCP agent to summarize Wikipedia page...\")
        result = await mcp_agent.run(task=\"Summarize the content of https://en.wikipedia.org/wiki/Seattle\")
        if result.messages and isinstance(result.messages[-1], TextMessage):
             print(\"MCP Agent Summary:\")
             # print(result.messages[-1].content) # Print actual summary
             print(\"(Actual output depends on live model and tool call)\")
        else:
             print(\"MCP Agent did not produce expected TextMessage result.\")
             print(f\"Result: {result}\")

    except FileNotFoundError:
        print(\"Error: 'uvx mcp-server-fetch' command not found. Ensure it's installed and in PATH.\")
    except Exception as e:
        print(f\"Error during MCP tool example: {e}\")

# Example execution
# asyncio.run(run_mcp_tool_example())
print(\"(Skipping actual execution of run_mcp_tool_example in this script)\")


# --- Using Tools: Langchain Tools ---
print(\"\\n--- Langchain Tools Example ---\")
async def run_langchain_tool_example():
    print(\"Setting up Langchain tool example...\")
    try:
        # Requires pandas and langchain-experimental
        df = pd.read_csv(\"https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv\")
        print(\"Loaded Titanic dataset into DataFrame.\")
        tool = LangChainToolAdapter(PythonAstREPLTool(locals={\"df\": df}))
        print(\"Created LangChainToolAdapter for PythonAstREPLTool.\")

        lc_agent = AssistantAgent(
            \"assistant_lc\", tools=[tool], model_client=model_client, system_message=\"Use the `df` variable to access the dataset.\"
        )
        print(\"Created agent with Langchain tool.\")

        print(\"Running agent with Langchain tool via Console...\")
        await Console(
            lc_agent.on_messages_stream(
                [TextMessage(content=\"What's the average age of the passengers?\", source=\"user\")], CancellationToken()
            ),
            output_stats=True,
        )
        print(\"(Actual output depends on live model and tool call)\")

    except ImportError:
        print(\"Error: Missing pandas or langchain-experimental. Skipping Langchain example.\")
        print(\"Install with: pip install pandas langchain-experimental\")
    except Exception as e:
        print(f\"Error during Langchain tool example: {e}\")

# Example execution
# asyncio.run(run_langchain_tool_example())
print(\"(Skipping actual execution of run_langchain_tool_example in this script)\")


# --- Parallel Tool Calls (Disabling) ---
print(\"\\n--- Parallel Tool Calls (Disabling) Example ---\")
try:
    model_client_no_parallel_tool_call = OpenAIChatCompletionClient(
        model=\"gpt-4o\",
        parallel_tool_calls=False, # Disable parallel calls
    )
    agent_no_parallel_tool_call = AssistantAgent(
        name=\"assistant_no_parallel\",
        model_client=model_client_no_parallel_tool_call,
        tools=[web_search], # Example tool
        system_message=\"Use tools to solve tasks.\",
    )
    print(\"Created agent with parallel_tool_calls=False\")
except Exception as e:
    print(f\"Error creating non-parallel client/agent: {e}\")


# --- Structured Output ---
print(\"\\n--- Structured Output Example ---\")
# The response format for the agent as a Pydantic base model.
class AgentResponse(BaseModel):
    thoughts: str
    response: Literal[\"happy\", \"sad\", \"neutral\"]

async def run_structured_output_example():
    print(\"Setting up structured output agent...\")
    try:
        structured_agent = AssistantAgent(
            \"assistant_structured\",
            model_client=model_client,
            system_message=\"Categorize the input as happy, sad, or neutral following the JSON format.\",
            # Define the output content type of the agent.
            output_content_type=AgentResponse,
        )
        print(\"Created agent with structured output type.\")

        print(\"Running agent for structured output via Console...\")
        result = await Console(structured_agent.run_stream(task=\"I am happy.\"))
        print(\"(Actual output depends on live model call)\")

        # Check the last message in the result, validate its type, and print the thoughts and response.
        if result.messages and isinstance(result.messages[-1], StructuredMessage):
             if isinstance(result.messages[-1].content, AgentResponse):
                 print(\"Structured Output Validation:\")
                 print(\"Thought: \", result.messages[-1].content.thoughts)
                 print(\"Response: \", result.messages[-1].content.response)
             else:
                 print(\"Error: Last message content is not of type AgentResponse\")
        else:
             print(\"Error: Last message is not a StructuredMessage\")

    except Exception as e:
        print(f\"Error during structured output example: {e}\")

# Example execution
# asyncio.run(run_structured_output_example())
print(\"(Skipping actual execution of run_structured_output_example in this script)\")


# --- Streaming Tokens ---
print(\"\\n--- Streaming Tokens Example ---\")
async def run_token_streaming_example():
    print(\"Setting up token streaming agent...\")
    try:
        streaming_assistant = AssistantAgent(
            name=\"assistant_streaming\",
            model_client=model_client,
            system_message=\"You are a helpful assistant.\",
            model_client_stream=True,  # Enable streaming tokens.
        )
        print(\"Created agent with token streaming enabled.\")

        print(\"\\nStreaming via on_messages_stream:\")
        async for message in streaming_assistant.on_messages_stream(
            [TextMessage(content=\"Name two cities in South America\", source=\"user\")],
            cancellation_token=CancellationToken(),
        ):
            # print(message) # Print each chunk/event
            pass # Avoid excessive printing in combined script
        print(\"(Finished streaming on_messages_stream - actual output depends on live model call)\")

        print(\"\\nStreaming via run_stream:\")
        async for message in streaming_assistant.run_stream(task=\"Name two cities in North America.\"):
            # print(message) # Print each chunk/event
            pass # Avoid excessive printing in combined script
        print(\"(Finished streaming run_stream - actual output depends on live model call)\")

    except Exception as e:
        print(f\"Error during token streaming example: {e}\")

# Example execution
# asyncio.run(run_token_streaming_example())
print(\"(Skipping actual execution of run_token_streaming_example in this script)\")


# --- Using Model Context (Buffered) ---
print(\"\\n--- Model Context (Buffered) Example ---\")
try:
    # Create an agent that uses only the last 5 messages in the context to generate responses.
    agent_buffered = AssistantAgent(
        name=\"assistant_buffered\",
        model_client=model_client,
        tools=[web_search], # Example tool
        system_message=\"Use tools to solve tasks.\",
        model_context=BufferedChatCompletionContext(buffer_size=5),  # Only use the last 5 messages
    )
    print(\"Created agent with BufferedChatCompletionContext(buffer_size=5)\")
except Exception as e:
    print(f\"Error creating buffered context agent: {e}\")


# --- Close Model Client ---
# Important to close client when done, especially if it holds resources
async def close_client():
    print(\"\\nClosing model client...\")
    await model_client.close()
    print(\"Model client closed.\")

# Example execution
# asyncio.run(close_client())
print(\"(Skipping actual execution of close_client in this script)\")
