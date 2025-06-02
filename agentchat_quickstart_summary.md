# AgentChat Quickstart Summary

This guide provides a quickstart for building applications using preset agents in AgentChat.

## Installation

Install the AgentChat and Extension packages:

```bash
pip install -U "autogen-agentchat" "autogen-ext[openai,azure]"
```

## Example: Single Agent with Tool Use

This example creates a single agent that can use tools.

1.  **Import necessary modules:**

    ```python
    from autogen_agentchat.agents import AssistantAgent
    from autogen_agentchat.ui import Console
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    ```
2.  **Define a model client:**

    ```python
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o",
        # api_key="YOUR_API_KEY",
    )
    ```

    You can use other model clients as well. To use Azure OpenAI models, follow the instructions [here](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html).
3.  **Define a tool function:**

    ```python
    async def get_weather(city: str) -> str:
        """Get the weather for a given city."""
        return f"The weather in {city} is 73 degrees and Sunny."
    ```
4.  **Define an AssistantAgent:**

    ```python
    agent = AssistantAgent(
        name="weather_agent",
        model_client=model_client,
        tools=[get_weather],
        system_message="You are a helpful assistant.",
        reflect_on_tool_use=True,
        model_client_stream=True,  # Enable streaming tokens from the model client.
    )
    ```
5.  **Run the agent:**

    ```python
    async def main() -> None:
        await Console(agent.run_stream(task="What is the weather in New York?"))
        # Close the connection to the model client.
        await model_client.close()

    # NOTE: if running this inside a Python script you'll need to use asyncio.run(main()).
    await main()
    ```

## Example Output

```
---------- user ----------
What is the weather in New York?
---------- weather_agent ----------
[FunctionCall(id='call_bE5CYAwB7OlOdNAyPjwOkej1', arguments='{"city":"New York"}', name='get_weather')]
---------- weather_agent ----------
[FunctionExecutionResult(content='The weather in New York is 73 degrees and Sunny.', call_id='call_bE5CYAwB7OlOdNAyPjwOkej1', is_error=False)]
---------- weather_agent ----------
The current weather in New York is 73 degrees and sunny.
```

## What’s Next?

Follow the [tutorial](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/index.html) for a walkthrough on other features of AgentChat.

[Previous](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/installation.html)

[Next](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/migration-guide.html)
