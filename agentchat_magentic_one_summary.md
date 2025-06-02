# AgentChat - Magentic-One Summary

Magentic-One is a generalist multi-agent system for solving open-ended web and file-based tasks across a variety of domains. It represents a significant step forward for multi-agent systems, achieving competitive performance on a number of agentic benchmarks.

Originally implemented directly on `autogen-core`, Magentic-One has been ported to `autogen-agentchat` for a more modular and easier-to-use interface.

## Key Components

*   **MagenticOneGroupChat**: The orchestrator, now a standard AgentChat team.
*   **MultimodalWebSurfer, FileSurfer, MagenticOneCoderAgent**: Broadly available as AgentChat agents.
*   **MagenticOne**: A helper class bundling all components together with minimal configuration.

[![Magentic-One Example](https://microsoft.github.io/autogen/stable/_images/autogen-magentic-one-example.png)](https://microsoft.github.io/autogen/stable/_images/autogen-magentic-one-example.png)

*Magentic-One multi-agent team completing a complex task from the GAIA benchmark.*

[![Magentic-One Agents](https://microsoft.github.io/autogen/stable/_images/autogen-magentic-one-agents.png)](https://microsoft.github.io/autogen/stable/_images/autogen-magentic-one-agents.png)

## Security Precautions

*   Use Containers: Run all tasks in docker containers to isolate the agents and prevent direct system attacks.
*   Virtual Environment: Use a virtual environment to run the agents and prevent them from accessing sensitive data.
*   Monitor Logs: Closely monitor logs during and after execution to detect and mitigate risky behavior.
*   Human Oversight: Run the examples with a human in the loop to supervise the agents and prevent unintended consequences.
*   Limit Access: Restrict the agents’ access to the internet and other resources to prevent unauthorized actions.
*   Safeguard Data: Ensure that the agents do not have access to sensitive data or resources that could be compromised.

## Getting Started

1.  Install the required packages:

    ```bash
    pip install "autogen-agentchat" "autogen-ext[magentic-one,openai]"
    # If using the MultimodalWebSurfer, you also need to install playwright dependencies:
    playwright install --with-deps chromium
    ```
2.  Go through the AgentChat tutorial.
3.  Try swapping out a `autogen_agentchat.teams.SelectorGroupChat` with `MagenticOneGroupChat`.

## Architecture

Magentic-One work is based on a multi-agent architecture where a lead Orchestrator agent is responsible for high-level planning, directing other agents and tracking task progress.

*   **Orchestrator**: the lead agent responsible for task decomposition and planning.
*   **WebSurfer**: An LLM-based agent that is proficient in commanding and managing the state of a Chromium-based web browser.
*   **FileSurfer**: An LLM-based agent that commands a markdown-based file preview application to read local files of most types.
*   **Coder**: An LLM-based agent specialized through its system prompt for writing code, analyzing information collected from the other agents, or creating new artifacts.
*   **ComputerTerminal**: Provides the team with access to a console shell where the Coder’s programs can be executed, and where new programming libraries can be installed.

## Citation

```
@misc{fourney2024magenticonegeneralistmultiagentsolving,
  title={Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks},
  author={Adam Fourney and Gagan Bansal and Hussein Mozannar and Cheng Tan and Eduardo Salinas and Erkang and Zhu and Friederike Niedtner and Grace Proebsting and Griffin Bassman and Jack Gerrits and Jacob Alber and Peter Chang and Ricky Loynd and Robert West and Victor Dibia and Ahmed Awadallah and Ece Kamar and Rafah Hosn and Saleema Amershi},
  year={2024},
  eprint={2411.04468},
  archivePrefix={arXiv},
  primaryClass={cs.AI},
  url={https://arxiv.org/abs/2411.04468},
}
```

[Previous](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/swarm.html)

[Next](https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/memory.html)
