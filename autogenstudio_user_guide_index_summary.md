# AutoGen Studio User Guide Index Summary

## Overview

AutoGen Studio is a low-code interface built to help you rapidly prototype AI agents, enhance them with tools, compose them into teams and interact with them to accomplish tasks. It is built on AutoGen AgentChat - a high-level API for building multi-agent applications.

[See a video tutorial on AutoGen Studio v0.4 (02/25) - https://youtu.be/oum6EI7wohM](https://youtu.be/oum6EI7wohM)

Code for AutoGen Studio is on [GitHub at microsoft/autogen](https://github.com/microsoft/autogen)

[![PyPi](https://badge.fury.io/py/autogenstudio.svg)](https://pypi.org/project/autogenstudio/)
[![Downloads](https://static.pepy.tech/badge/autogenstudio/week)](https://pepy.tech/project/autogenstudio)
[![YouTube Tutorial](https://img.youtube.com/vi/oum6EI7wohM/maxresdefault.jpg)](https://youtu.be/oum6EI7wohM)

## Capabilities - What Can You Do with AutoGen Studio?

AutoGen Studio offers four main interfaces to help you build and manage multi-agent systems:

*   **Team Builder**: A visual interface for creating agent teams through declarative specification (JSON) or drag-and-drop. Supports configuration of all core components: teams, agents, tools, models, and termination conditions. Fully compatible with AgentChat’s component definitions.
*   **Playground**: Interactive environment for testing and running agent teams. Features include: Live message streaming between agents, Visual representation of message flow through a control transition graph, Interactive sessions with teams using UserProxyAgent, Full run control with the ability to pause or stop execution.
*   **Gallery**: Central hub for discovering and importing community-created components. Enables easy integration of third-party components.
*   **Deployment**: Export and run teams in python code. Setup and test endpoints based on a team configuration. Run teams in a docker container.

## Roadmap

Review project roadmap and issues [here](https://github.com/microsoft/autogen).

## Contribution Guide

We welcome contributions to AutoGen Studio. We recommend the following general steps to contribute to the project:

1.  Review the overall AutoGen project contribution guide
2.  Please review the AutoGen Studio roadmap to get a sense of the current priorities for the project. Help is appreciated especially with Studio issues tagged with help-wanted
3.  Please use the tag proj-studio tag for any issues, questions, and PRs related to Studio
4.  Please initiate a discussion on the roadmap issue or a new issue to discuss your proposed contribution.
5.  Submit a pull request with your contribution!

If you are modifying AutoGen Studio, it has its own devcontainer. See instructions in .devcontainer/README.md to use it

## A Note on Security

AutoGen Studio is a research prototype and is not meant to be used in a production environment. Some baseline practices are encouraged e.g., using Docker code execution environment for your agents.

However, other considerations such as rigorous tests related to jailbreaking, ensuring LLMs only have access to the right keys of data given the end user’s permissions, and other security features are not implemented in AutoGen Studio.

If you are building a production application, please use the AutoGen framework and implement the necessary security features.

## Acknowledgements and Citation

AutoGen Studio is based on the AutoGen project. It was adapted from a research prototype built in October 2023 (original credits: Victor Dibia, Gagan Bansal, Adam Fourney, Piali Choudhury, Saleema Amershi, Ahmed Awadallah, Chi Wang).

If you use AutoGen Studio in your research, please cite the following paper:

```
@inproceedings{autogenstudio,
  title={AUTOGEN STUDIO: A No-Code Developer Tool for Building and Debugging Multi-Agent Systems},
  author={Dibia, Victor and Chen, Jingya and Bansal, Gagan and Syed, Suff and Fourney, Adam and Zhu, Erkang and Wang, Chi and Amershi, Saleema},
  booktitle={Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: System Demonstrations},
  pages={72--79},
  year={2024}
}
```

## Next Steps

To begin, follow the installation instructions to install AutoGen Studio.

[Previous](https://microsoft.github.io/autogen/stable/user-guide/extensions-user-guide/index.html)

[Next](https://microsoft.github.io/autogen/stable/user-guide/autogenstudio-user-guide/installation.html)
