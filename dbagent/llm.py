"""OpenAI Responses API adapter using only the Python standard library."""
import json
import os
import urllib.request
import urllib.error
from .model import validate_model


# The prompt specifies a restricted JSON contract for the downstream mapper.
# It cannot guarantee that the inferred business rules are correct.
INSTRUCTIONS = '''You are a database requirements analyst. Convert requirements into JSON with keys entities, relationships, assumptions, questions. Each entity has name, attributes (array of {name,type,nullable}), primary_key (array of names). Types: string, integer, decimal, date, timestamp, boolean. Each relationship has from, to, cardinality (one-to-many, many-to-one, one-to-one, many-to-many), optional_from (boolean), optional_to (boolean), name (string). Cardinality describes the number of TO instances per FROM instance: one-to-many means one FROM may relate to many TO; many-to-one means many FROM relate to one TO. Do not create separate associative entities for many-to-many; deterministic mapper does that. Include only relationships supported by requirements; put uncertainty in questions, and assumptions in assumptions. Use singular PascalCase entity names, snake_case attributes, and *_id keys. Avoid unsupported assumptions; explicitly ask clarifying questions. Return only a valid JSON object, no markdown.'''

def extract_requirements(description, model='gpt-4.1-mini', api_key=None):
    """Request candidate design JSON from OpenAI, then validate its structure."""
    # Read secrets from the environment; never hard-code credentials.
    key = api_key or os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY is not set. Use --demo or --model-file for offline mode.')
    # Ask the Responses API for JSON output and disable response storage.
    payload = {'model': model, 'instructions': INSTRUCTIONS, 'input': description,
               'text': {'format': {'type': 'json_object'}}, 'store': False}
    request = urllib.request.Request('https://api.openai.com/v1/responses',
        data=json.dumps(payload).encode(), headers={'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'}, method='POST')
    # Translate HTTP failures into actionable command-line errors.
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            result = json.load(response)
    except urllib.error.HTTPError as ex:
        detail = ex.read().decode('utf-8', errors='replace')[:800]
        raise RuntimeError(f'API request failed ({ex.code}): {detail}') from ex
    # Extract assistant text from the Responses API output envelope.
    chunks = []
    for item in result.get('output', []):
        if item.get('type') == 'message':
            for c in item.get('content', []):
                if c.get('type') == 'output_text':
                    chunks.append(c.get('text', ''))
    if not chunks:
        raise RuntimeError('Model returned no output text')
    try:
        # Structural validation is not the same as semantic correctness.
        return validate_model(json.loads(''.join(chunks)))
    except (ValueError, json.JSONDecodeError) as ex:
        raise RuntimeError(f'LLM returned invalid design JSON: {ex}') from ex
