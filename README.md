# visa-knowledge

Structured knowledge base for Netherlands visa and residence permit routes.

## Structure

```
visa-knowledge/
├── schema/
│   └── route-schema.json   JSON Schema that every route file must satisfy
├── routes/
│   └── *.yaml              One file per route
├── docs/
│   └── *-factsheet.md      Per-route notes, open uncertainties, and research trail
├── validator.py            CLI tool to validate route files
└── README.md               This file
```

## Route YAML fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | Unique slug, kebab-case, e.g. `partner-married-mvv` |
| `name` | string | yes | Human-readable route name |
| `authority` | object | yes | Issuing authority: `name`, `country` (ISO-3166-1 alpha-2), `url` |
| `applicant_profile` | object | yes | `relationship_to_reference`, `reference_holder_status`, optional `age_minimum`, `nationality_restrictions`, `notes` |
| `eligibility.conditions` | array | yes | Each condition: `id`, `description`, optional `threshold`, `uncertainty` |
| `required_documents` | array | yes | Each doc: `id`, `name`, optional `description`, `mandatory`, `notes` |
| `fees` | array | yes | Each fee: `label`, `amount_eur`, optional `notes` |
| `processing_time` | object | yes | `legal_max_days`, optional `typical_days`, `notes` |
| `forms` | array | no | Each form: `id`, `name`, optional `url`, `notes` |
| `portal` | object | no | `name`, `url`, optional `notes` |
| `sources` | array | yes | Each source: `url`, `retrieved` (YYYY-MM-DD), `description` |

## Adding a new route

1. Create `routes/<new-route-id>.yaml` using an existing route as a template.
2. Fill in all required fields. Add at least one source with a retrieval date.
3. Run the validator to check the file is well-formed:
   ```bash
   pip install pyyaml jsonschema   # first time only
   python validator.py routes/<new-route-id>.yaml
   ```
4. Create a matching factsheet in `docs/<new-route-id>-factsheet.md` listing any open uncertainties, contradictions found in the source material, or items that need human verification.
5. Open a pull request. The PR description must list the sources used and the retrieval date.

## Validator

Validates all route files against `schema/route-schema.json`:

```bash
python validator.py                      # all routes
python validator.py routes/my-route.yaml  # single file
```

Requires Python 3.10+ and `pip install pyyaml jsonschema`.

## Routes

| ID | Name | Authority | Status |
|----|------|-----------|--------|
| [partner-married-mvv](routes/partner-married-mvv.yaml) | MVV + Residence Permit - Married or Registered Partner | IND (NL) | draft |

## Sources and freshness

Visa rules change. Every route YAML records a `retrieved` date per source. Before using any route for client advice, verify the key facts (fee, decision period, income threshold) against the current IND page.
