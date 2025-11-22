# config/llm_config.py

from typing import Any, Dict, List


def get_config_list() -> List[Dict[str, Any]]:
    """
    Configuration list for models served by Ollama.
    """
    return [
        {
            # Must match the model name as shown by `ollama list`
            "model": "deepseek-coder-v2:16b",

            # Tell AutoGen to use the Ollama client instead of OpenAI
            "api_type": "ollama",

            # Where Ollama is running (default)
            "client_host": "http://localhost:11434",

            # Optional tweaks
            "stream": False,
        }
    ]


def get_llm_config() -> Dict[str, Any]:
    """
    Shared llm_config for all agents.
    This is what you'll pass to ConversableAgent / AssistantAgent.
    """
    return {
        "config_list": get_config_list(),
        "temperature": 0.2,
        "timeout": 120,
        "max_tokens": 4096,
    }

