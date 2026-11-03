"""Diagram, Oracle DDL, and student-facing review report."""
import re

def mermaid(model):
    """Render the validated candidate E-R model as Mermaid source text."""
    out = ['erDiagram']
    for e in model['entities']:
        out.append(f'    {e["name"]} {{')
        for a in e['attributes']:
            key = ' PK' if a['name'] in e['primary_key'] else ''
            out.append(f'        {a["type"]} {a["name"]}{key}')
        out.append('    }')
    # Translate conceptual cardinalities into Mermaid relationship markers.
    marks = {'one-to-many': '||--o{', 'many-to-one': '}o--||', 'one-to-one': '||--||', 'many-to-many': '}o--o{'}
    for r in model.get('relationships', []):
        label = re.sub(r'[^A-Za-z0-9_ ]', '', r.get('name', 'relates')) or 'relates'
        out.append(f'    {r["from"]} {marks[r["cardinality"]]} {r["to"]} : {label.replace(" ", "_")}')
    return '\n'.join(out) + '\n'

SQL_TYPES = {'string': 'VARCHAR2(255)', 'integer': 'NUMBER(10)', 'decimal': 'NUMBER(12,2)', 'date': 'DATE', 'timestamp': 'TIMESTAMP', 'boolean': 'NUMBER(1)'}

def oracle_ddl(tables):
    """Generate Oracle CREATE TABLE statements followed by foreign keys."""
    out = ['-- Candidate Oracle DDL; review keys, business rules, and optionality before use.', '']
    # CREATE all tables before adding FK constraints, supporting circular references.
    # Generate tables first so referenced tables exist before FK constraints.
    for t in tables:
        lines = []
        for c in t['columns']:
            nn = ' NOT NULL' if (not c.get('nullable', True) or c['name'] in t['primary_key']) else ''
            lines.append(f'    {c["name"]} {SQL_TYPES[c["type"]]}{nn}')
        lines.append(f'    CONSTRAINT pk_{t["name"]} PRIMARY KEY ({", ".join(t["primary_key"])})')
        out.append(f'CREATE TABLE {t["name"]} (\n' + ',\n'.join(lines) + '\n);\n')
    # Add foreign keys in a second pass to support cyclic references.
    for t in tables:
        for i, fk in enumerate(t['foreign_keys'], 1):
            out.append(f'ALTER TABLE {t["name"]} ADD CONSTRAINT fk_{t["name"]}_{i} '
                       f'FOREIGN KEY ({", ".join(fk["columns"])}) '
                       f'REFERENCES {fk["references"]} ({", ".join(fk["ref_columns"])});')
    return '\n'.join(out) + '\n'

def review_report(description, model, tables, warnings):
    """Create the human verification checklist and unresolved-design warnings."""
    out = ['# Student Design Verification Report', '', '## Original requirements', description.strip(), '',
           '## Assumptions (verify with stakeholder)']
    # Surface assumptions and questions instead of silently treating them as facts.
    out += [f'- {x}' for x in model.get('assumptions', [])] or ['- None recorded. This does not prove there are none.']
    out += ['', '## Clarification questions']
    out += [f'- {x}' for x in model.get('questions', [])] or ['- None generated. Check for missing questions.']
    out += ['', '## Mapping warnings']
    out += [f'- {x}' for x in warnings] or ['- No automatic warnings. Manual review is still required.']
    out += ['', '## Student verification checklist',
            '- [ ] All entities and attributes match the original requirements.',
            '- [ ] Cardinality and participation are supported by explicit business rules.',
            '- [ ] Every primary key is a genuine unique identifier.',
            '- [ ] Foreign keys, junction tables, and relationship attributes are correct.',
            '- [ ] For each claimed 3NF relation, list FDs and candidate keys and justify 3NF.',
            '- [ ] Test DDL in Oracle; do not treat successful execution as semantic proof.',
            '- [ ] Document at least three possible errors, limitations, or design decisions.',
            '', '## Important limitations',
            'The agent does not prove 3NF or infer functional dependencies reliably from prose.',
            'One-to-one relationships require manual mapping. Participation/optional constraints require manual review.',
            'Mermaid and SQL are candidate artifacts, not verified business designs.', '']
    return '\n'.join(out)
