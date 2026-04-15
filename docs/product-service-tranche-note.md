# Product-service tranche note

This tranche introduces a first product/service refinement layer on top of the merged cybernetic-self, party/identity, org/legal, and business-core surfaces.

Added in this tranche:
- `Domains/product-service.ttl`
- `shapes/product-service.shacl.ttl`
- `examples/product-service-demo.ttl`
- `tests/product-service-integrity.rq`

What this tranche covers:
- service and product offerings
- plans and SKUs
- capabilities and features
- entitlements, SLAs, price books, meters, and quota policy
- provisioned service instances bound to party, contract, and provider entity

Required integration in this tranche:
- register `Domains/product-service.ttl` in the module map and registry
- fold product-service gates into `shapes/ontogenesis.shacl.ttl`
- keep the validator and SPARQL invariants on the canonical path already established by the prior tranche
