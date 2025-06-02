# autogen_ext.tools.langchain.LangChainToolAdapter Summary

## Overview

The `LangChainToolAdapter` class allows you to wrap a LangChain tool and make it available to AutoGen.

**Note:** This class requires the `langchain` extra for the `autogen-ext` package.

```bash
pip install -U "autogen-ext[langchain]"
```

## Parameters

*   `langchain_tool` (`LangChainTool`): A LangChain tool to wrap

## Examples

### Pandas DataFrame Interaction

This example demonstrates how to use the `PythonAstREPLTool` from the `langchain_experimental` package to create a tool that allows you to interact with a Pandas DataFrame.

```python
import asyncio
import pandas as pd
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from autogen_ext.tools.langchain import LangChainToolAdapter
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken


async def main() -> None:
    df = pd.read_csv("https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv")  # type: ignore
    tool = LangChainToolAdapter(PythonAstREPLTool(locals={"df": df}))
    model_client = OpenAIChatCompletionClient(model="gpt-4o")
    agent = AssistantAgent(
        "assistant",
        tools=[tool],
        model_client=model_client,
        system_message="Use the `df` variable to access the dataset.",
    )
    await Console(
        agent.on_messages_stream(
            [TextMessage(content="What's the average age of the passengers?", source="user")], CancellationToken()
        )
    )


asyncio.run(main())
```

### SQLite Database Interaction

This example demonstrates how to use the `SQLDatabaseToolkit` from the `langchain_community` package to interact with an SQLite database. It uses the `RoundRobinGroupChat` to iterate the single agent over multiple steps.

```python
import asyncio
import sqlite3

import requests
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
from sqlalchemy import Engine, create_engine
from sqlalchemy.pool import StaticPool


def get_engine_for_chinook_db() -> Engine:
    url = "https://raw.githubusercontent.com/lerocha/chinook-database/master/ChinookDatabase/DataSources/Chinook_Sqlite.sql"
    response = requests.get(url)
    sql_script = response.text
    connection = sqlite3.connect(":memory:", check_same_thread=False)
    connection.executescript(sql_script)
    return create_engine(
        "sqlite://",
        creator=lambda: connection,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )


async def main() -> None:
    # Create the engine and database wrapper.
    engine = get_engine_for_chinook_db()
    db = SQLDatabase(engine)

    # Create the toolkit.
    llm = ChatOpenAI(temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    # Create the LangChain tool adapter for every tool in the toolkit.
    tools = [LangChainToolAdapter(tool) for tool in toolkit.get_tools()]

    # Create the chat completion client.
    model_client = OpenAIChatCompletionClient(model="gpt-4o")

    # Create the assistant agent.
    agent = AssistantAgent(
        "assistant",
        model_client=model_client,
        tools=tools,  # type: ignore
        model_client_stream=True,
        system_message="Respond with 'TERMINATE' if the task is completed.",
    )

    # Create termination condition.
    termination = TextMentionTermination("TERMINATE")

    # Create a round-robin group chat to iterate the single agent over multiple steps.
    chat = RoundRobinGroupChat([agent], termination_condition=termination)

    # Run the chat.
    await Console(chat.run_stream(task="Show some tables in the database"))


if __name__ == "__main__":
    asyncio.run(main())
```

[Previous](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.http.html)

[Next](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.tools.mcp.html)
