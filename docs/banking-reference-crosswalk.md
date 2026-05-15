# Banking Reference Crosswalk

## Purpose

This note records the first external banking reference anchors for the Ontogenesis banking tranche.

The current banking ontology modules are seed artifacts for the SocioProphet banking twin.
They are **not** a claim of full external standard conformance.

## FIBO alignment intent

Use FIBO as the primary ontology reference point for:

- legal entity semantics
- obligations and contracts
- financial instruments and facilities
- party and role semantics
- reporting and risk terminology normalization

## BIAN alignment intent

Use BIAN as the primary operational/service-domain reference point for:

- banking service-domain decomposition
- service boundary naming
- semantic API alignment
- business capability framing

## Working rule

Use FIBO primarily for concept and ontology alignment.
Use BIAN primarily for service-domain and operating-boundary alignment.
When the two overlap, prefer explicit mapping notes rather than silent conflation.

## Conformance boundary

This tranche records FIBO and BIAN as alignment anchors only.
It does not assert conformance to any specific FIBO release, BIAN release, certification profile, API specification, or service-domain implementation.

A future conformance-bearing tranche must name the exact external release or profile being targeted and include traceable mapping assertions.

## Immediate next step

The next tranche should annotate candidate overlaps with:

- relevant FIBO areas for ontology classes and properties
- relevant BIAN service-domain references for runtime/service surfaces
- explicit mapping status such as candidate, reviewed, accepted, or rejected
