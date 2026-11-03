"""Validate the JSON intermediate representation before generating SQL."""

import json
import re


# Whitelist SQL identifier characters to avoid unsafe generated identifiers.
IDENT = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
TYPES = {'string', 'integer', 'decimal', 'date', 'timestamp', 'boolean'}

def validate_model(data):
    """Reject malformed entities, keys, data types, and relationships."""
    if not isinstance(data, dict):
        raise ValueError('Model must be a JSON object')
    entities = data.get('entities')
    relationships = data.get('relationships', [])
    if not isinstance(entities, list) or not entities:
        raise ValueError('At least one entity required')
    if not isinstance(relationships, list):
        raise ValueError('relationships must be an array')
    # Entity names must be unique even when capitalization differs.
    names = set()
    for e in entities:
        name = e.get('name')
        if not isinstance(name, str) or not IDENT.fullmatch(name) or name.lower() in names:
            raise ValueError(f'Invalid or duplicate entity name: {name}')
        names.add(name.lower())
        attrs = e.get('attributes')
        pk = e.get('primary_key')
        if not isinstance(attrs, list) or not attrs or not isinstance(pk, list) or not pk:
            raise ValueError(f'{name}: attributes and primary_key required')
        # Check every attribute and ensure primary keys refer to real attributes.
        attr_names = set()
        for a in attrs:
            n = a.get('name')
            if not isinstance(n, str) or not IDENT.fullmatch(n) or n.lower() in attr_names:
                raise ValueError(f'{name}: invalid/duplicate attribute {n}')
            if a.get('type') not in TYPES:
                raise ValueError(f'{name}.{n}: unsupported type')
            if not isinstance(a.get('nullable', True), bool):
                raise ValueError(f'{name}.{n}: nullable must be boolean')
            attr_names.add(n.lower())
        if any(k.lower() not in attr_names for k in pk) or len(set(k.lower() for k in pk)) != len(pk):
            raise ValueError(f'{name}: invalid primary key')
    # Relationship endpoints must reference declared entities.
    allowed = {'one-to-many', 'many-to-one', 'one-to-one', 'many-to-many'}
    for r in relationships:
        if r.get('from') not in [e['name'] for e in entities] or r.get('to') not in [e['name'] for e in entities]:
            raise ValueError(f'Unknown relationship entity: {r}')
        if r.get('cardinality') not in allowed:
            raise ValueError(f'Unsupported cardinality: {r}')
        if not isinstance(r.get('optional_from', False), bool) or not isinstance(r.get('optional_to', False), bool):
            raise ValueError('optional flags must be boolean')
        if r.get('from') == r.get('to'):
            raise ValueError('Self relationships require manual mapping in this version')
    for field in ('assumptions', 'questions'):
        if not isinstance(data.get(field, []), list):
            raise ValueError(f'{field} must be an array')
    return data

def load_model(path):
    """Load a local JSON design and apply the same checks as live LLM mode."""
    with open(path, encoding='utf-8') as f:
        return validate_model(json.load(f))
