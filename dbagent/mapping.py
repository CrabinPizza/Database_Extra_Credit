"""Deterministic educational E-R to relational mapping."""
from copy import deepcopy
from .model import validate_model

def map_relations(model):
    """Convert supported E-R relationships into tables and FK metadata."""
    validate_model(model)
    # Each entity becomes one table; deep copies avoid mutating the input model.
    tables = {e['name']: {'name': e['name'], 'columns': deepcopy(e['attributes']), 'primary_key': list(e['primary_key']), 'foreign_keys': []} for e in model['entities']}
    warnings = []
    for r in model.get('relationships', []):
        left, right, kind = r['from'], r['to'], r['cardinality']
        # A 1:1 mapping requires explicit participation and uniqueness decisions.
        if kind == 'one-to-one':
            warnings.append(f'{left} - {right}: one-to-one requires business-rule review; no FK automatically added')
            continue
        # An M:N relationship becomes a junction table with a composite PK.
        if kind == 'many-to-many':
            join = f'{left}_{right}'
            if join in tables:
                raise ValueError(f'Junction table name conflict: {join}')
            columns, pk, fks = [], [], []
            # Copy the primary-key columns from both participating entities.
            for source in (left, right):
                t = tables[source]
                new_names = []
                for k in t['primary_key']:
                    original = next(c for c in t['columns'] if c['name'] == k)
                    new = f'{source.lower()}_{k}'
                    if any(c['name'] == new for c in columns):
                        raise ValueError('Junction column name collision')
                    columns.append({'name': new, 'type': original['type'], 'nullable': False})
                    pk.append(new)
                    new_names.append(new)
                fks.append({'columns': new_names, 'references': source, 'ref_columns': list(t['primary_key'])})
            tables[join] = {'name': join, 'columns': columns, 'primary_key': pk, 'foreign_keys': fks}
            continue
        # A 1:N relationship places the parent's key on the child table.
        parent, child = (left, right) if kind == 'one-to-many' else (right, left)
        pt, ct = tables[parent], tables[child]
        new_names = []
        # Reuse existing compatible FK columns or create new nullable ones.
        for key in pt['primary_key']:
            col = next(c for c in pt['columns'] if c['name'] == key)
            new_name = f'{parent.lower()}_{key}'
            if any(c['name'] == new_name for c in ct['columns']):
                warnings.append(f'{child}.{new_name} already exists; verify its intended foreign-key semantics')
                existing = next(c for c in ct['columns'] if c['name'] == new_name)
                if existing['type'] != col['type']:
                    raise ValueError(f'FK type mismatch: {child}.{new_name}')
            else:
                ct['columns'].append({'name': new_name, 'type': col['type'], 'nullable': True})
            new_names.append(new_name)
        fk = {'columns': new_names, 'references': parent, 'ref_columns': list(pt['primary_key'])}
        if fk not in ct['foreign_keys']:
            ct['foreign_keys'].append(fk)
        # Optionality cannot be safely inferred from this simplified schema.
        warnings.append(f'{child} -> {parent}: confirm FK optionality and participation; generated FK is nullable')
    return list(tables.values()), warnings
