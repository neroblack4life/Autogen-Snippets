# Autogen Homepage Summary

## Overview

AutoGen is a framework for building AI agents and applications. It provides different components for various use cases:

## Components

### Magentic-One CLI

A console-based multi-agent assistant for web and file-based tasks. Built on AgentChat.

```bash
pip install -U magentic-one-cli
m1 "Find flights from Seattle to Paris and format the result in a table"
```

[![PyPi](https://img.shields.io/badge/PyPi-magentic--one--cli-blue?logo=pypi)](https://pypi.org/project/magentic-one-cli/)

[Get Started](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/magentic-one.html)

### Studio

An app for prototyping and managing agents without writing code. Built on AgentChat.

```bash
pip install -U autogenstudio
autogenstudio ui --port 8080 --appdir ./myapp
```

[![PyPi](https://img.shields.io/badge/PyPi-autogenstudio-blue?logo=pypi)](https://pypi.org/project/autogenstudio/)

[Get Started](https://microsoft.github.io/autogen/stable/user-guide/autogenstudio-user-guide/index.html)

### AgentChat

A programming framework for building conversational single and multi-agent applications. Built on Core. Requires Python 3.10+.

```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def main() -> None:
    agent = AssistantAgent("assistant", OpenAIChatCompletionClient(model="gpt-4o"))
    print(await agent.run(task="Say 'Hello World!'"))

asyncio.run(main())
```

[![PyPi](https://img.shields.io/badge/PyPi-autogen--agentchat-blue?logo=pypi)](https://pypi.org/project/autogen-agentchat/)

Start here if you are building conversational agents. [Migrating from AutoGen 0.2?.](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/migration-guide.html)

[Get Started](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/quickstart.html)

### Core

An event-driven programming framework for building scalable multi-agent AI systems. Example scenarios:

*   Deterministic and dynamic agentic workflows for business processes.
*   Research on multi-agent collaboration.
*   Distributed agents for multi-language applications.

[![PyPi](https://img.shields.io/badge/PyPi-autogen--core-blue?logo=pypi)](https://pypi.org/project/autogen-core/)

Start here if you are building workflows or distributed agent systems.

[Get Started](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/quickstart.html)

### Extensions

Implementations of Core and AgentChat components that interface with external services or other libraries. You can find and use community extensions or create your own. Examples of built-in extensions:

*   LangChainToolAdapter for using LangChain tools.
*   OpenAIAssistantAgent for using Assistant API.
*   DockerCommandLineCodeExecutor for running model-generated code in a Docker container.
*   GrpcWorkerAgentRuntime for distributed agents.

[![PyPi](https://img.shields.io/badge/PyPi-autogen--ext-blue?logo=pypi)](https://pypi.org/project/autogen-ext/)

[Discover Community Extensions](https://microsoft.github.io/autogen/stable/user-guide/extensions-user-guide/discover.html)
[Create New Extension](https://microsoft.github.io/autogen/stable/user-guide/extensions-user-guide/create-your-own.html)

[Next](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/index.html)
