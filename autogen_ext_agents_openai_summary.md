# autogen_ext.agents.openai.OpenAIAssistantAgent Summary

## Overview

The `OpenAIAssistantAgent` class is an agent implementation that uses the OpenAI Assistant API to generate responses.

**Installation:**

```bash
pip install "autogen-ext[openai]"
# pip install "autogen-ext[openai,azure]"  # For Azure OpenAI Assistant
```

This agent leverages the Assistant API to create AI assistants with capabilities like:

*   Code interpretation and execution
*   File handling and search
*   Custom function calling
*   Multi-turn conversations

The agent maintains a thread of conversation and can use various tools including:

*   Code interpreter: For executing code and working with files
*   File search: For searching through uploaded documents
*   Custom functions: For extending capabilities with user-defined tools

## Key Features:

*   Supports multiple file formats including code, documents, images
*   Can handle up to 128 tools per assistant
*   Maintains conversation context in threads
*   Supports file uploads for code interpreter and search
*   Vector store integration for efficient file search
*   Automatic file parsing and embedding

You can use an existing thread or assistant by providing the `thread_id` or `assistant_id` parameters.

## Parameters:

*   `name` (str): Name of the assistant
*   `description` (str): Description of the assistant’s purpose
*   `client` (`AsyncOpenAI` | `AsyncAzureOpenAI`): OpenAI client or Azure OpenAI client instance
*   `model` (str): Model to use (e.g. “gpt-4o”)
*   `instructions` (str): System instructions for the assistant
*   `tools` (Optional[Iterable[Union[Literal["code_interpreter", "file_search"], Tool | Callable[[...], Any] | Callable[[...], Awaitable[Any]]]]]): Tools the assistant can use
*   `assistant_id` (Optional[str]): ID of existing assistant to use
*   `thread_id` (Optional[str]): ID of existing thread to use
*   `metadata` (Optional[Dict[str, str]]): Additional metadata for the assistant.
*   `response_format` (Optional[AssistantResponseFormatOptionParam]): Response format settings
*   `temperature` (Optional[float]): Temperature for response generation
*   `tool_resources` (Optional[ToolResources]): Additional tool configuration
*   `top_p` (Optional[float]): Top p sampling parameter

## Examples

### Analyze Data in a CSV File

```python
from openai import AsyncOpenAI
from autogen_core import CancellationToken
import asyncio
from autogen_ext.agents.openai import OpenAIAssistantAgent
from autogen_agentchat.messages import TextMessage


async def example():
    cancellation_token = CancellationToken()

    # Create an OpenAI client
    client = AsyncOpenAI(api_key="your-api-key", base_url="your-base-url")

    # Create an assistant with code interpreter
    assistant = OpenAIAssistantAgent(
        name="Python Helper",
        description="Helps with Python programming",
        client=client,
        model="gpt-4o",
        instructions="You are a helpful Python programming assistant.",
        tools=["code_interpreter"],
    )

    # Upload files for the assistant to use
    await assistant.on_upload_for_code_interpreter("data.csv", cancellation_token)

    # Get response from the assistant
    response = await assistant.on_messages(
        [TextMessage(source="user", content="Analyze the data in data.csv")], cancellation_token
    )

    print(response)

    # Clean up resources
    await assistant.delete_uploaded_files(cancellation_token)
    await assistant.delete_assistant(cancellation_token)


asyncio.run(example())
```

### Azure OpenAI Assistant with AAD Authentication

```python
from openai import AsyncAzureOpenAI
import asyncio
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from autogen_core import CancellationToken
from autogen_ext.agents.openai import OpenAIAssistantAgent
from autogen_agentchat.messages import TextMessage


async def example():
    cancellation_token = CancellationToken()

    # Create an Azure OpenAI client
    token_provider = get_bearer_token_provider(DefaultAzureCredential())
    client = AsyncAzureOpenAI(
        azure_deployment="YOUR_AZURE_DEPLOYMENT",
        api_version="YOUR_API_VERSION",
        azure_endpoint="YOUR_AZURE_ENDPOINT",
        azure_ad_token_provider=token_provider,
    )

    # Create an assistant with code interpreter
    assistant = OpenAIAssistantAgent(
        name="Python Helper",
        description="Helps with Python programming",
        client=client,
        model="gpt-4o",
        instructions="You are a helpful Python programming assistant.",
        tools=["code_interpreter"],
    )

    # Get response from the assistant
    response = await assistant.on_messages([TextMessage(source="user", content="Hello.")], cancellation_token)

    print(response)

    # Clean up resources
    await assistant.delete_assistant(cancellation_token)


asyncio.run(example())
```

[Previous](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.agents.magentic_one.html)

[Next](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.agents.web_surfer.html)
