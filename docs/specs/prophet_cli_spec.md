# Prophet CLI ontology — spec notes

This repo **models** Prophet CLI as data you can reason over:

- planes
- commands
- spaces affected (SYSTEM/USER/INCEPTION/REGION/MACRO)
- dynamic registration (ServiceDescriptor, CapabilityDescriptor/CapD)
- “carriers” (schemaRef + leafRef)
- 3×3 build recipes (local/region/macro)

## Why this matters

Once your CLI surface is modeled:
- you can **reason** about whether an operation is safe in a given space,
- enforce **policy gates** (SHACL) before a command is allowed,
- generate docs/UX and keep them consistent with reality,
- validate CapDs before promoting them into SYSTEM space,
- unify runtime discovery across offline and cloud environments.

## What to extend next (expected)

- Add explicit Command instances per plane (verb+noun), with:
  - required options/flags
  - outputs (carriers)
  - required IO claims
  - required secrets
- Add Route and SyncSpec instances for known endpoints (mesh + boundary)

