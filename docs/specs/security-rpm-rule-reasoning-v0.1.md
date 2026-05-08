# Security RPM Rule Reasoning v0.1

## Status

Draft. This specification defines the first SocioProphet bridge from abstract visual reasoning systems such as RAVEN, WReN, CoPINet, LEN, MXGNet, I-RAVEN/SRAN, PrAE, and NVSA into UDM-compatible security-event reasoning.

The goal is not to import those systems as opaque model dependencies. The goal is to preserve their useful discipline: structured scenes, role-bound attributes, candidate comparison, rule-family induction, distractor resistance, multiplex graph relations, probabilistic abduction/execution, vector-symbolic binding, cleanup memory, and fair generalization testing.

## Problem

Security telemetry is usually reduced too early:

```text
raw logs / packets / payloads -> embeddings -> anomaly score
```

This loses the critical structure that makes the evidence meaningful. A byte, character, token, field, packet, TLS handshake, HTTP method, user identifier, or UDM event type can be content, identity, control, policy, or evidence depending on its role in a stream.

This spec defines a disciplined alternative:

```text
typed elements
+ role-bound UDM-compatible structures
+ CRPO preimage receipts
+ augmented sequential patterns
+ beacon instances
+ vector-symbolic rule detection/execution
+ ontology-linked parser mappings
+ policy-constrained SecurityResult emission
```

## Conceptual mapping

| Abstract reasoning term | Security-event equivalent |
| --- | --- |
| RAVEN panel | Event, packet, protocol frame, log record, or payload span |
| RAVEN object | Token, entity, process, file, endpoint, character, or protocol field |
| Attribute | UDM field, protocol field, control attribute, or preimage property |
| Context panels | Observed event window |
| Candidate panels | Candidate next event, verdict, policy action, or explanation |
| Rule detection | Infer stream, beacon, or control-transition rule family |
| Rule execution | Predict expected continuation or admissible action |
| Answer selection | Choose SecurityResult, policy action, or anomaly status |

## Layered instance model

Every observed element should be represented at multiple layers:

1. `RawPreimage`: byte offset, packet offset, stream offset, file offset, source artifact hash.
2. `DecodedSymbol`: character, protocol token, parsed field name, enum, or value.
3. `TypedElement`: content token, identifier token, control token, state-transition token, execution token, policy token, evidence token, or fingerprint token.
4. `RoleBinding`: UDM-compatible binding such as `principal.ip`, `target.port`, `network.http.method`, `tls.client.ja3`, `process.command_line`, or `security_result.action`.
5. `LocalRelation`: process-executes-file, user-accesses-resource, client-connects-target, TLS-upgrade-occurs, DNS-answer-resolves-domain.
6. `SequentialRelation`: before, after, repeats-every, rotates, upgrades, authenticates, fails, retries, fans-out, or converges.
7. `RuleInstance`: heartbeat, suspicious beacon, software update, STARTTLS transition, process-launch-to-network, DNS-to-HTTP follow-through.
8. `ControlImplication`: allow, block, quarantine, challenge, alert, inspect, redact, local-only retention, or require-human-approval.

## UDM-compatible role binding

The canonical scene slots are UDM-compatible event roles:

```text
metadata
principal
src
target
observer
intermediary
about
network
security_result
extensions
additional
```

These roles prevent field ambiguity. For example, an IP address is not meaningful enough on its own. `principal.ip` and `target.ip` have different operational implications.

## Vector-symbolic representation

A security event vector is a bundle of bound role-value pairs:

```text
EventVec =
  bind(EVENT_TYPE, NETWORK_HTTP)
+ bind(PRINCIPAL_IP, 10.0.0.5)
+ bind(TARGET_HOST, example.internal)
+ bind(HTTP_METHOD, POST)
+ bind(USER_AGENT_BUCKET, rare_ua_17)
+ bind(TLS_JA3, ja3_hash_x)
+ bind(TIME_BUCKET, t_001)
+ bind(OBSERVER, intercept_proxy)
```

A sequence vector binds event vectors to positions and deltas:

```text
SeqVec =
  bind(POS_1, PROCESS_LAUNCH_EVENT)
+ bind(POS_2, NETWORK_CONNECTION_EVENT)
+ bind(POS_3, NETWORK_HTTP_EVENT)
+ bind(DELTA_2_3, 60s_jittered)
+ bind(CONTROL_STATE, TLS_ESTABLISHED)
```

A beacon vector binds repeated control-signal properties:

```text
BeaconVec =
  bind(PERIODICITY, 60s_jittered)
+ bind(STABLE_PRINCIPAL, host_or_process)
+ bind(STABLE_FINGERPRINT, ja3_or_user_agent)
+ bind(TARGET_ROTATION, low_or_high)
+ bind(PAYLOAD_SIZE_CLASS, small_repeated)
+ bind(CONTROL_PURPOSE, heartbeat_or_c2_unknown)
```

These vector forms are not a replacement for RDF/JSON-LD/UDM-style structure. They are a fast reasoning projection with mandatory preimage and lossiness metadata.

## Rule families

The initial rule-family registry is:

- `constant`: a value persists across a row, window, or session.
- `progression`: a value changes monotonically or according to an ordered sequence.
- `arithmetic`: counts, bytes, timing, or risk values combine predictably.
- `logical_and_or_xor`: boolean or set-level composition.
- `consistent_union`: elements share stable set membership.
- `rotation`: targets, domains, ports, certificates, or endpoints rotate by schedule.
- `periodicity`: events repeat at stable or jittered interval.
- `state_transition`: plaintext to STARTTLS to TLS, unauthenticated to authenticated, process launch to network connect.
- `role_inversion`: source/target or principal/target roles flip unexpectedly.
- `fan_out_fan_in`: one principal to many targets or many sources to one target.
- `prevalence_shift`: rare field appears in common context or common field appears in rare context.

## Beacon semantics

A beacon is a structured repeated control signal, not merely periodic traffic.

Benign security beacon pattern:

```text
metadata.event_type in {STATUS_HEARTBEAT, STATUS_UPDATE}
principal.asset_id or observer present
product/vendor identity present
purpose is liveness, version, or fingerprint update
expected interval for product family
no suspicious target, credential material, or protocol anomaly
```

Suspicious beacon pattern:

```text
metadata.event_type in {NETWORK_CONNECTION, NETWORK_HTTP, NETWORK_DNS}
periodicity stable or jittered
stable principal/process/fingerprint
target, domain, or certificate may rotate
payload size is small and repeated
rare or suspicious JA3, JA3S, user-agent, domain, or endpoint
```

The same sequential form can be benign or malicious. The distinction must be made by role-bound context, provenance, target identity, purpose, and SecurityResult evidence.

## Control-bearing elements

The following must be classified before crossing a prompt, terminal, workflow, parser, or network-action boundary:

- ASCII control characters.
- Unicode bidi controls and zero-width controls.
- Terminal escape sequences.
- Protocol commands such as `STARTTLS`, `CONNECT`, `HELO`, `EHLO`, and database TLS-upgrade markers.
- TLS handshake and certificate state transitions.
- JA3, JA3S, JARM-like, certificate, user-agent, and tracker fingerprints.
- UDM `metadata.event_type` and `security_result.action`.
- Agent/workflow command tokens.

## Parser uncertainty

Parsers and protocol dissectors may emit probability mass functions when uncertain:

```json
{
  "event_type": {"NETWORK_HTTP": 0.72, "NETWORK_CONNECTION": 0.21, "GENERIC_EVENT": 0.07},
  "application_protocol": {"HTTPS": 0.65, "GRPC": 0.22, "UNKNOWN": 0.13},
  "security_category": {"NETWORK_COMMAND_AND_CONTROL": 0.41, "NETWORK_SUSPICIOUS": 0.37, "UNKNOWN_CATEGORY": 0.22}
}
```

Rule detection must operate over uncertainty rather than silently collapsing uncertain events into crisp labels too early.

## Ontology linking

Unknown vendor fields, protocol fields, and tabular columns should be mapped through an ontology-linking candidate record:

```text
raw field / column / protocol token
-> label + examples + neighboring fields
-> candidate UDM/Ontogenesis field mappings
-> confidence + preimage examples
-> human or policy validation
-> parser mapping promotion
```

This supports zero-shot or few-shot onboarding of new protocols and vendor logs without erasing evidence.

## Required receipts

Each `SecurityRPMInstance`, `SequencePatternInstance`, or `BeaconPatternInstance` must carry:

- Source event IDs or preimage references.
- Parser/dissector version.
- Symbol dictionary version.
- Rule-family version.
- Cleanup-memory version, if vector-symbolic cleanup is used.
- Lossiness profile.
- Policy scope.
- Linkability/high-entropy field classification.

## Repository placement

- `ontogenesis`: ontology, rule-family vocabulary, SHACL gates, and canonical docs.
- `semantic-serdes`: JSON schemas and fixtures for RPM, beacon, sequence, and ontology-linking records.
- `sherlock-search`: indexes for windows, beacon instances, control tokens, and feature coverage.
- `policy-fabric`: gates for control-token classification, beacon identity misuse, and high-entropy export scope.
- `TriTRPC`: Path N/T/H transport profiles for network streams, TLS state, and host/human-linked telemetry.

## Non-goals

- This spec does not vendor any third-party model implementation.
- This spec does not copy the full Google UDM field list.
- This spec does not make ML outputs authoritative.
- This spec does not allow raw decrypted traffic or high-entropy fingerprint fields to leave a lab/project boundary by default.

## Acceptance criteria

1. A benign `STATUS_HEARTBEAT` can be modeled as a beacon without being treated as C2.
2. A suspicious periodic `NETWORK_HTTP`/`NETWORK_DNS` stream can emit a candidate `NETWORK_COMMAND_AND_CONTROL` SecurityResult.
3. A STARTTLS/TLS-upgrade stream can be represented as an ordered control-state transition.
4. Every rule instance can point back to source events and preimage receipts.
5. Every high-entropy aliasing field has an explicit linkability scope.
6. Every unknown protocol or parser field can be represented as an ontology-linking candidate rather than discarded.
