"""Generate text (e.g., a poem) using Inworld's Llama-3.3-70B-Instruct endpoint.

Minimal usage:
    python create_poem2.py "Your prompt here"

Or import the `create_poem2` function:
    from create_poem2 import create_poem2
    text = create_poem2("Write a short poem about the ocean")
"""

from __future__ import annotations
import json
import sys
from typing import Any, Dict
import requests

# Endpoint
_URL = "https://api.inworld.ai/llm/v1alpha/completions:completeText"

# Inworld API key
KEY = 'NmowRmNFUkQwQ2VWWDI4SmlGTzg4blQ4NFJVSWY3dmg6d1kycjdmRnJUUlppN1F5d1MyaXhsYVE2NTRFZlUxWklsTHpkZzgxQ3VrdGpCOWx4ZmNLRUg5bzNmSWNSaXR1Rg=='

_HEADERS = {
    "Authorization": f"Basic {KEY}",
    "Content-Type": "application/json",
}

# Base payload with the selected model
_BASE_PAYLOAD: Dict[str, Any] = {
    "servingId": {
        "modelId": {
            "serviceProvider": "SERVICE_PROVIDER_TENSTORRENT",
            "model": "tenstorrent/Llama-3.3-70B-Instruct",
        },
        "userId": "user",
    },
}

def create_poem2(prompt: str) -> str:
    """Send *prompt* to the Inworld LLM endpoint and return the generated text."""
    payload = {
        **_BASE_PAYLOAD,
        "prompt": {"text": prompt},
    }

    # Debug: print headers
    print("Request headers:", _HEADERS)

    response = requests.post(_URL, json=payload, headers=_HEADERS, timeout=60)

    # If the request failed, print details for debugging
    if response.status_code != 200:
        print("Received non-200 response (status", response.status_code, ")")
        try:
            print("Response body:", json.dumps(response.json(), indent=2))
        except Exception:
            print("Response body (raw):", response.text)
        response.raise_for_status()

    data = response.json()
    return json.dumps(data, indent=2)


# ---------------------------------------------------------------------------
# CLI / debug usage
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Combine all CLI args into a single prompt string
    if len(sys.argv) < 2:
        print("Usage: python create_poem2.py <prompt text>")
        sys.exit(1)

    prompt_text = " ".join(sys.argv[1:])
    result_text = create_poem2(prompt_text)
    print(result_text)
