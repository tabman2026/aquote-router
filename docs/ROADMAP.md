# Roadmap

## v0.2.x

- Stabilize API reference, CLI reference, K-line guide, return fields, and data
  source documentation.
- Keep `diagnose --json` useful for local support.
- Keep source policy and audit trail tests aligned with implementation.

## v0.3.x

- Improve adapter contract tests.
- Add more structured source health diagnostics.
- Expand examples that remain safe for offline test environments.

## v0.4.x

- Review optional adapters only when field normalization tests exist.
- Use the v0.4.0 adapter candidate review entry for efinance, baostock, and
  mootdx research:
  [review](ADAPTER_CANDIDATE_REVIEW_V040.md),
  [field mapping draft](ADAPTER_FIELD_MAPPING_DRAFT_V040.md),
  [unit rules draft](ADAPTER_UNIT_RULES_DRAFT_V040.md), and
  [source policy draft](SOURCE_POLICY_DRAFT_V040.md). These documents do not
  mean the current version supports those data sources.
- Improve packaging and release verification.

## v1.0.0

- Freeze public model fields, error codes, source policy schema, and audit schema.
- Document compatibility guarantees.

This roadmap is about data access infrastructure and maintenance quality only.
