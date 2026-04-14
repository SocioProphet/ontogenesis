"""Quantum adapter sketches for Epi‑Onto‑Learning.

This is intentionally lightweight: the ontology repo is NOT your training repo.
The goal is to provide an auditable reference implementation that can be
copied into the training stack.

- Aer simulator by default.
- Hardware providers must be opt-in and fully logged in reports.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Tuple, Optional

@dataclass
class QuantumResult:
    mean: float
    variance: float
    backend: str
    provider: str
    mitigation: Tuple[str, ...]
    notes: str = ""

class QuantumChargeProjector:
    def __init__(self, shots: int = 2000, backend: str = "aer", provider: str = "qiskit",
                 mitigation: Iterable[str] = ("m3","zne")) -> None:
        self.shots = shots
        self.backend = backend
        self.provider = provider
        self.mitigation = tuple(mitigation)

    def estimate(self, pauli_op: str, circuit: Any) -> QuantumResult:
        """Estimate ⟨pauli_op⟩ on the given circuit.

        In a production integration, this would:
        - compile to coupling map (e.g., heavy-hex)
        - run Qiskit primitives (Estimator/Sampler)
        - apply mitigation toggles (provider supports)
        """
        # Stub for this ontology repo.
        return QuantumResult(mean=0.0, variance=0.0, backend=self.backend, provider=self.provider,
                             mitigation=self.mitigation, notes="stub (no runtime integration)")
