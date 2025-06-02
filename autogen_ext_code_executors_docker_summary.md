# autogen_ext.code_executors.docker.DockerCommandLineCodeExecutor Summary

## Overview

The `DockerCommandLineCodeExecutor` class executes code through a command line environment in a Docker container.

**Note:** This class requires the `docker` extra for the `autogen-ext` package:

```bash
pip install "autogen-ext[docker]"
```

The executor saves each code block in a file in the working directory and then executes the code file in the container. It supports Python and shell scripts.

*   For Python code, use the language “python” for the code block.
*   For shell scripts, use the language “bash”, “shell”, “sh”, “pwsh”, “powershell”, or “ps1” for the code block.

## Parameters

*   `image` (str, optional): Docker image to use for code execution. Defaults to “python:3-slim”.
*   `container_name` (Optional[str], optional): Name of the Docker container which is created. If None, will autogenerate a name. Defaults to None.
*   `timeout` (int, optional): The timeout for code execution. Defaults to 60.
*   `work_dir` (Union[Path, str], optional): The working directory for the code execution. Defaults to temporary directory.
*   `bind_dir` (Union[Path, str], optional): The directory that will be bound to the code executor container. Useful for cases where you want to spawn the container from within a container. Defaults to None.
*   `auto_remove` (bool, optional): If true, will automatically remove the Docker container when it is stopped. Defaults to True.
*   `stop_container` (bool, optional): If true, will automatically stop the container when stop is called, when the context manager exits or when the Python process exits with atext. Defaults to True.
*   `functions` (List[Union[FunctionWithRequirements[Any, A], Callable[..., Any]]]): A list of functions that are available to the code executor. Default is an empty list.
*   `functions_module` (str, optional): The name of the module that will be created to store the functions. Defaults to “functions”.
*   `extra_volumes` (Optional[Dict[str, Dict[str, str]]], optional): A dictionary of extra volumes (beyond the work_dir) to mount to the container; key is host source path and value ‘bind’ is the container path. See Defaults to None. Example: `extra_volumes = {'/home/user1/': {'bind': '/mnt/vol2', 'mode': 'rw'}, '/var/www': {'bind': '/mnt/vol1', 'mode': 'ro'}}`
*   `extra_hosts` (Optional[Dict[str, str]], optional): A dictionary of host mappings to add to the container. (See Docker docs on extra_hosts) Defaults to None. Example: `extra_hosts = {"kubernetes.docker.internal": "host-gateway"}`
*   `init_command` (Optional[str], optional): A shell command to run before each shell operation execution. Defaults to None. Example: `init_command="kubectl config use-context docker-hub"`

**Note:** Using the current directory (“.”) as working directory is deprecated.

[Previous](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.code_executors.local.html)

[Next](https://microsoft.github.io/autogen/stable/reference/python/autogen_ext.code_executors.jupyter.html)
