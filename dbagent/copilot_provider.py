"""GitHub Copilot SDK adapter for the same JSON design contract as OpenAI.

Requires Python 3.11+, github-copilot-sdk, Copilot CLI and an authorized
GitHub Copilot account. Model usage is subject to account quotas.
"""
import asyncio
import json
from .llm import INSTRUCTIONS
from .model import validate_model


def _parse_json(content):
    """Accept a JSON object, or a fenced JSON block returned by the model."""
    text = (content or "").strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            text = "\n".join(lines[1:-1]).strip()
    try:
        return validate_model(json.loads(text))
    except (ValueError, TypeError) as exc:
        raise RuntimeError("Copilot did not return a valid design JSON object: " + str(exc)) from exc


async def _query(description, model=None):
    """Use a restricted Copilot session without granting custom tools."""
    try:
        from copilot import CopilotClient
    except ImportError as exc:
        raise RuntimeError("Install github-copilot-sdk using Python 3.11+.") from exc
    options = {"available_tools": []}
    if model:
        options["model"] = model
    async with CopilotClient() as client:
        session = await client.create_session(**options)
        response = await session.send_and_wait(
            "Follow the JSON contract below strictly. Return only JSON.\n"
            + INSTRUCTIONS + "\n\nDATABASE REQUIREMENTS:\n" + description
        )
        if response is None or not getattr(response, "data", None):
            raise RuntimeError("Copilot returned no assistant response")
        return _parse_json(response.data.content)


def extract_requirements_copilot(description, model=None):
    """Synchronous wrapper used by the command-line application."""
    return asyncio.run(_query(description, model=model))
