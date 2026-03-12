import os
from typing import Any, Dict, List, Optional

from anthropic import Anthropic
from dotenv import load_dotenv
from dataclasses import dataclass

# Try to load from project root .env first, then current dir
# modern_software_dev_ny is the project root (week1 is inside it)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(project_root, ".env"))
# Also try local .env for overrides
load_dotenv()


@dataclass
class Message:
    content: str


@dataclass
class Response:
    message: Message


def _get_temperature(options: Optional[Dict[str, Any]]) -> Optional[float]:
    if not options:
        return None
    value = options.get("temperature")
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def chat(model: str, messages: List[Dict[str, str]], options: Optional[Dict[str, Any]] = None) -> Response:
    temperature = _get_temperature(options)
    
    # Use Kimi Code / Moonshot configuration
    api_key = os.getenv("KIMI_API_KEY") or os.getenv("MOONSHOT_API_KEY")
    if not api_key:
        raise ValueError("环境变量中缺少 KIMI_API_KEY 或 MOONSHOT_API_KEY")
        
    # Kimi Coding (Anthropic Compatible)
    # Base URL: https://api.kimi.com/coding/
    # Protocol: Anthropic Messages API
    
    base_url = os.getenv("KIMI_BASE_URL", "https://api.kimi.com/coding/")
    selected_model = os.getenv("KIMI_MODEL") or "kimi-for-coding" # Default model k2p5
    
    # Initialize Anthropic client
    # Note: Anthropic client automatically handles /v1/messages if needed, but for custom base_url
    # we should provide the root.
    
    client = Anthropic(
        api_key=api_key,
        base_url=base_url,
        timeout=120.0,  # 2 minutes timeout should be enough for most non-streaming tasks
    )
    
    # Convert OpenAI-style messages to Anthropic-style
    # 1. Extract system prompt if present
    system_prompt = None
    anthropic_messages = []
    
    for msg in messages:
        if msg["role"] == "system":
            system_prompt = msg["content"]
        else:
            anthropic_messages.append({"role": msg["role"], "content": msg["content"]})
            
    # Call Anthropic API
    kwargs = {
        "model": selected_model,
        "max_tokens": 8192, # Adjusted to reasonable size (was 32768 causing SDK error)
        "messages": anthropic_messages,
    }
    
    if system_prompt:
        kwargs["system"] = system_prompt
    if temperature is not None:
        kwargs["temperature"] = temperature
    if options and "thinking" in options:
        kwargs["thinking"] = options["thinking"]
        
    response = client.messages.create(**kwargs)

    content = response.content[0].text or ""
    return Response(message=Message(content=content))
