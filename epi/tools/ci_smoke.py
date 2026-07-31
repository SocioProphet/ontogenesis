#!/usr/bin/env python3
from qiskit import QuantumCircuit
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer.primitives import Estimator

qc = QuantumCircuit(2); qc.h(0); qc.cx(0,1)
op = SparsePauliOp.from_list([("ZZ", 1.0)])
val = Estimator(run_options={'shots':1024}).run([(qc, op)]).result().values[0]
print("[ci] Estimator <ZZ> ~", val)
