"""
Shared utilities for LLM API calls.

This module provides helpers for calling OpenAI-compatible LLM endpoints
with structured response handling.
"""
import json
import requests
from django.conf import settings


class LLMError(Exception):
    """Raised when LLM API call fails or returns invalid data."""
    pass


def call_llm_json(system_prompt, user_prompt, temperature=0.2, max_tokens=1500, timeout=30):
    """
    Call the configured LLM endpoint and return parsed JSON response.

    Args:
        system_prompt (str): System message defining the AI's role and constraints
        user_prompt (str): User message with the actual request/data
        temperature (float): LLM temperature (0.0-1.0, lower = more deterministic)
        max_tokens (int): Maximum tokens in response
        timeout (int): Request timeout in seconds

    Returns:
        dict: Parsed JSON response from the LLM

    Raises:
        LLMError: If API call fails, response is invalid, or JSON parsing fails
    """
    if not settings.LLM_BASE_URL or not settings.LLM_API_KEY:
        raise LLMError("LLM_BASE_URL and LLM_API_KEY must be configured in settings")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        resp = requests.post(
            f"{settings.LLM_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.LLM_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()

        # Extract the assistant's reply
        reply = data["choices"][0]["message"]["content"].strip()

        # Parse as JSON — with fallback extraction for prose/fence wrapping
        try:
            return json.loads(reply)
        except json.JSONDecodeError:
            pass

        # Fallback: strip markdown fences and retry
        stripped = reply.strip()
        if stripped.startswith("```"):
            # Remove opening fence (e.g. ```json or ```)
            stripped = stripped.split("\n", 1)[-1]
            # Remove closing fence
            if stripped.rstrip().endswith("```"):
                stripped = stripped.rstrip()[:-3].rstrip()
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            pass

        # Fallback: locate first '{' and last '}' and parse that substring
        start = reply.find("{")
        end = reply.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(reply[start : end + 1])
            except json.JSONDecodeError:
                pass

        # All attempts failed — raise with diagnostic snippet
        snippet = reply[:250].replace("\n", " ")
        raise LLMError(
            f"invalid JSON from LLM — could not parse response. "
            f"First 250 chars: {snippet!r}"
        )

    except requests.exceptions.Timeout:
        raise LLMError("LLM API request timed out")
    except requests.exceptions.RequestException as e:
        raise LLMError(f"LLM API request failed: {e}") from e
    except (KeyError, IndexError) as e:
        raise LLMError(f"Unexpected LLM API response format: {e}") from e


def call_llm_text(system_prompt, user_prompt, temperature=0.2, max_tokens=350, timeout=25):
    """
    Call the configured LLM endpoint and return plain text response.

    This is a simpler version for non-JSON responses (e.g., the ai_assist chat widget).

    Args:
        system_prompt (str): System message defining the AI's role and constraints
        user_prompt (str): User message with the actual request/data
        temperature (float): LLM temperature (0.0-1.0, lower = more deterministic)
        max_tokens (int): Maximum tokens in response
        timeout (int): Request timeout in seconds

    Returns:
        str: Plain text response from the LLM

    Raises:
        LLMError: If API call fails or response is invalid
    """
    if not settings.LLM_BASE_URL or not settings.LLM_API_KEY:
        raise LLMError("LLM_BASE_URL and LLM_API_KEY must be configured in settings")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    try:
        resp = requests.post(
            f"{settings.LLM_BASE_URL}/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.LLM_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.LLM_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()

        # Extract and return the assistant's reply
        return data["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        raise LLMError("LLM API request timed out")
    except requests.exceptions.RequestException as e:
        raise LLMError(f"LLM API request failed: {e}") from e
    except (KeyError, IndexError) as e:
        raise LLMError(f"Unexpected LLM API response format: {e}") from e
