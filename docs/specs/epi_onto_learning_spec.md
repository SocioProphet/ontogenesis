# Epi‑Onto‑Learning — spec notes

Epi‑Onto‑Learning is where your learning plan becomes **auditable**:

- Each model block declares:
  - algebra (ℂ/ℍ/𝕆, Clifford, SPD, Grassmann, symplectic/Lagrangian)
  - group action (U(1), SU(2), G₂, …)
  - invariant form + integrator
  - Noether charges (diagnostics to conserve)
  - coercions between algebras with witnesses (e.g., octonion associator norm)
- Training emits diagnostic artifacts:
  - charge drift plots
  - invariance deltas
  - SR head fits + gate scores
- Publishing pipeline emits signed PDFs + sidecars.

## Optional quantum lane

Quantum offload is modeled as **opt-in** and must be fully recorded:
- provider/backend
- mitigation knobs
- qubit budget
- task metadata

The ontology repo includes a *reference* notebook and adapter skeleton.
Your production training repo should wire this into TritFabric and your CI.

