Summary of AgentChat Installation Page (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/installation.html):

This page provides instructions for installing the AgentChat package.

Key Steps:
1.  **Virtual Environment (Optional but Recommended):** Suggests using a virtual environment (`venv` or `conda`) to isolate dependencies. Provides commands for creating and activating a `venv` environment on different operating systems (Windows vs. others).
2.  **Install AgentChat:** The core package is installed using pip:
    `pip install -U "autogen-agentchat"`
    Requires Python 3.10 or later.
3.  **Install OpenAI Model Client (Optional):** To use OpenAI or Azure OpenAI models, specific extensions need to be installed:
    -   For general OpenAI/Azure OpenAI usage: `pip install "autogen-ext[openai]"`
    -   For Azure OpenAI with AAD authentication: `pip install "autogen-ext[azure]"`

The next step indicated is the "Quickstart" guide.
