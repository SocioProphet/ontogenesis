# Value Flows Governed Binding v0.4 (Minimal Executable Slice)

This is the minimized upstream landing slice for `SocioProphet/ontogenesis`.

It preserves the delegated-authority, process-scoped task-flow proof surface while reducing file sprawl for the first executable PR tranche.

Included:
- canonical schema map
- event envelope + payload schema map
- compact reference objects
- compact memberships dataset for runtime
- linear / assignment-override / divergence replay fixtures
- Rego policy and allow/deny testdata
- deterministic validation, replay, and expected-report checks
- repo-ready GitHub Actions workflow

This slice is intentionally narrower than the full sandbox bundle, but it remains machine-checkable and sufficient to prove:
- delegated offer
- delegated completion override
- delegated assignment override
- denial of unauthorized assignment override
- deterministic replay with expected hash checks
