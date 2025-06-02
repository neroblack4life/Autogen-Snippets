# Code snippets from AgentChat Tutorial - Models Page
# (https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/tutorial/models.html)

import logging
import os
from autogen_core import EVENT_LOGGER_NAME
from autogen_core.models import UserMessage

# --- Logging Setup ---
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(EVENT_LOGGER_NAME)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.INFO) # Enable INFO level logging for model calls

# --- OpenAI ---
# Installation: pip install "autogen-ext[openai]"
from autogen_ext.models.openai import OpenAIChatCompletionClient

async def test_openai():
    print(\"--- Testing OpenAI Client ---\")
    openai_model_client = OpenAIChatCompletionClient(
        model=\"gpt-4o-2024-08-06\",
        # api_key=\"sk-...\", # Optional if OPENAI_API_KEY env var is set.
    )
    try:
        result = await openai_model_client.create([UserMessage(content=\"What is the capital of France?\", source=\"user\")])
        print(f\"OpenAI Result: {result}\")
    except Exception as e:
        print(f\"OpenAI Error: {e}\")
    finally:
        await openai_model_client.close()

# --- Azure OpenAI ---
# Installation: pip install "autogen-ext[openai,azure]"
from autogen_ext.auth.azure import AzureTokenProvider
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from azure.identity import DefaultAzureCredential # Requires azure-identity package

async def test_azure_openai():
    print(\"\\n--- Testing Azure OpenAI Client (AAD Auth) ---\")
    try:
        # Replace placeholders with your actual values
        azure_deployment = os.environ.get(\"AZURE_OPENAI_DEPLOYMENT\", \"{your-azure-deployment}\")
        model_name = os.environ.get(\"AZURE_OPENAI_MODEL\", \"{model-name, such as gpt-4o}\")
        api_version = os.environ.get(\"AZURE_OPENAI_API_VERSION\", \"2024-06-01\")
        azure_endpoint = os.environ.get(\"AZURE_OPENAI_ENDPOINT\", \"https://{your-custom-endpoint}.openai.azure.com/\")

        # Create the token provider
        token_provider = AzureTokenProvider(
            DefaultAzureCredential(),
            \"https://cognitiveservices.azure.com/.default\",
        )

        az_model_client = AzureOpenAIChatCompletionClient(
            azure_deployment=azure_deployment,
            model=model_name,
            api_version=api_version,
            azure_endpoint=azure_endpoint,
            azure_ad_token_provider=token_provider,
            # api_key=\"sk-...\", # For key-based authentication.
        )
        result = await az_model_client.create([UserMessage(content=\"What is the capital of France?\", source=\"user\")])
        print(f\"Azure OpenAI Result: {result}\")
        await az_model_client.close()
    except Exception as e:
        print(f\"Azure OpenAI Error: {e} (Ensure Azure credentials and deployment details are correct)\")


# --- Azure AI Foundry ---
# Installation: pip install "autogen-ext[azure]"
from autogen_ext.models.azure import AzureAIChatCompletionClient
from azure.core.credentials import AzureKeyCredential # Requires azure-core package

async def test_azure_ai_foundry():
    print(\"\\n--- Testing Azure AI Foundry Client (Phi-4 Example) ---\")
    github_token = os.environ.get(\"GITHUB_TOKEN\")
    if not github_token:
        print(\"GITHUB_TOKEN environment variable not set. Skipping Azure AI Foundry test.\")
        return

    try:
        client = AzureAIChatCompletionClient(
            model=\"Phi-4\",
            endpoint=\"https://models.inference.ai.azure.com\",
            credential=AzureKeyCredential(github_token),
            model_info={
                \"json_output\": False,
                \"function_calling\": False,
                \"vision\": False,
                \"family\": \"unknown\",
                \"structured_output\": False,
            },
        )
        result = await client.create([UserMessage(content=\"What is the capital of France?\", source=\"user\")])
        print(f\"Azure AI Foundry Result: {result}\")
        await client.close()
    except Exception as e:
        print(f\"Azure AI Foundry Error: {e}\")


# --- Anthropic (Experimental) ---
# Installation: pip install -U "autogen-ext[anthropic]"
from autogen_ext.models.anthropic import AnthropicChatCompletionClient

async def test_anthropic():
    print(\"\\n--- Testing Anthropic Client ---\")
    try:
        anthropic_client = AnthropicChatCompletionClient(model=\"claude-3-7-sonnet-20250219\") # Example model
        result = await anthropic_client.create([UserMessage(content=\"What is the capital of France?\", source=\"user\")])
        print(f\"Anthropic Result: {result}\")
        await anthropic_client.close()
    except Exception as e:
        print(f\"Anthropic Error: {e} (Ensure ANTHROPIC_API_KEY env var is set)\")


# --- Ollama (Experimental) ---
# Installation: pip install -U "autogen-ext[ollama]"
from autogen_ext.models.ollama import OllamaChatCompletionClient

async def test_ollama():
    print(\"\\n--- Testing Ollama Client ---\")
    try:
        # Assuming your Ollama server is running locally on port 11434.
        ollama_model_client = OllamaChatCompletionClient(model=\"llama3.2\") # Example model
        response = await ollama_model_client.create([UserMessage(content=\"What is the capital of France?\", source=\"user\")])
        print(f\"Ollama Result: {response}\")
        await ollama_model_client.close()
    except Exception as e:
        print(f\"Ollama Error: {e} (Ensure Ollama server is running)\")


# --- Gemini (Experimental - via OpenAI compatible API) ---
# Uses OpenAIChatCompletionClient
async def test_gemini():
    print(\"\\n--- Testing Gemini Client (via OpenAI Client) ---\")
    try:
        # Requires GEMINI_API_KEY env var or passed directly
        model_client = OpenAIChatCompletionClient(
            model=\"gemini-1.5-flash-8b\", # Example model
            # api_key=\"GEMINI_API_KEY\",
        )
        response = await model_client.create([UserMessage(content=\"What is the capital of France?\", source=\"user\")])
        print(f\"Gemini Result: {response}\")
        await model_client.close()
    except Exception as e:
        print(f\"Gemini Error: {e} (Ensure GEMINI_API_KEY env var is set)\")


# --- Semantic Kernel Adapter (Anthropic Example) ---
# Installation: pip install "autogen-ext[semantic-kernel-anthropic]"
from autogen_ext.models.semantic_kernel import SKChatCompletionAdapter
# Need semantic_kernel and relevant connector (e.g., semantic-kernel-connectors-ai-anthropic)
try:
    from semantic_kernel import Kernel
    from semantic_kernel.connectors.ai.anthropic import AnthropicChatCompletion, AnthropicChatPromptExecutionSettings
    from semantic_kernel.memory.null_memory import NullMemory
    SK_AVAILABLE = True
except ImportError:
    SK_AVAILABLE = False

async def test_sk_adapter_anthropic():
    print(\"\\n--- Testing Semantic Kernel Adapter (Anthropic) ---\")
    if not SK_AVAILABLE:
        print(\"Semantic Kernel or Anthropic connector not installed. Skipping test.\")
        return
    anthropic_api_key = os.environ.get(\"ANTHROPIC_API_KEY\")
    if not anthropic_api_key:
        print(\"ANTHROPIC_API_KEY environment variable not set. Skipping SK Anthropic test.\")
        return

    try:
        sk_client = AnthropicChatCompletion(
            ai_model_id=\"claude-3-5-sonnet-20241022\", # Example model
            api_key=anthropic_api_key,
            service_id=\"my-service-id\",
        )
        settings = AnthropicChatPromptExecutionSettings(
            temperature=0.2,
        )
        anthropic_model_client = SKChatCompletionAdapter(
            sk_client, kernel=Kernel(memory=NullMemory()), prompt_settings=settings
        )
        model_result = await anthropic_model_client.create(
            messages=[UserMessage(content=\"What is the capital of France?\", source=\"User\")]
        )
        print(f\"SK Adapter (Anthropic) Result: {model_result}\")
        await anthropic_model_client.close()
    except Exception as e:
        print(f\"SK Adapter (Anthropic) Error: {e}\")


# --- Main Execution (Optional: Uncomment to run tests) ---
# import asyncio
# async def run_all_tests():
#     await test_openai()
#     await test_azure_openai()
#     await test_azure_ai_foundry()
#     await test_anthropic()
#     await test_ollama()
#     await test_gemini()
#     await test_sk_adapter_anthropic()
#
# if __name__ == \"__main__\":
#     asyncio.run(run_all_tests())
