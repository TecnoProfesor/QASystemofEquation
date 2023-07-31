################
## x + y = 1
## x + y < 2
################
#initialization
import matplotlib.pyplot as plt
import numpy as np
import math

# importing Qiskit
from qiskit import IBMQ, Aer, transpile, execute
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.providers.ibmq import least_busy
from qiskit_textbook.problems import grover_problem_oracle

# import basic plot tools
from qiskit.visualization import plot_histogram

def oracle():
    # Compute auxiliaries
    ### to compute the solutions for x+y=1
    qc.cx(var_qubits[0], aux_qubits[0])
    qc.cx(var_qubits[1], aux_qubits[0])
    

    ### to compute the solutions for x+y<2
    qc.mct([[var_qubits[2]],[var_qubits[3]]],aux_qubits[1])
    qc.x(aux_qubits[1])

    # Flip 'out' qubit if all auxiliary qubits are satisfied
    qc.barrier()
    qc.mct(aux_qubits, out_qubit)
    qc.barrier()

    # Uncompute clauses to reset auxiliary-checking qubits to 0

    ### to uncompute the solutions for x+y=1
    qc.cx(var_qubits[0], aux_qubits[0])
    qc.cx(var_qubits[1], aux_qubits[0])

    ### to uncompute the solutions for x+y<2
    qc.mct([[var_qubits[2]],[var_qubits[3]]],aux_qubits[1])
    qc.x(aux_qubits[1])

def diffuser(nqubits):
    qc = QuantumCircuit(nqubits)
    # Apply transformation |s> -> |00..0> (H-gates)
    for qubit in range(nqubits):
        qc.h(qubit)
    # Apply transformation |00..0> -> |11..1> (X-gates)
    for qubit in range(nqubits):
        qc.x(qubit)
    # Do multi-controlled-Z gate
    qc.h(nqubits-1)
    qc.mct(list(range(nqubits-1)), nqubits-1)  # multi-controlled-toffoli
    qc.h(nqubits-1)
    # Apply transformation |11..1> -> |00..0>
    for qubit in range(nqubits):
        qc.x(qubit)
    # Apply transformation |00..0> -> |s>
    for qubit in range(nqubits):
        qc.h(qubit)
    # We will return the diffuser as a gate
    U_s = qc.to_gate()
    U_s.name = "U$_s$"
    return U_s


numberqubits = 4
var_qubits = QuantumRegister(numberqubits, name='v')
aux_qubits = QuantumRegister(2, name='a')
out_qubit = QuantumRegister(1, name='out')
cbits = ClassicalRegister(numberqubits, name='cbits')
qc = QuantumCircuit(var_qubits, aux_qubits, out_qubit, cbits)

# Initialize 'out0' in state |->
qc.initialize([1, -1]/np.sqrt(2), out_qubit)

# Initialize qubits in state |s>
qc.h(var_qubits)
qc.barrier()  # for visual separation

#### Fist iteration
oracle()
qc.barrier()  # for visual separation
qc.append(diffuser(numberqubits), [0,1,2,3])

#qc.h(var_qubits)
# Measure the variable qubits
qc.measure(var_qubits, cbits)

qc.draw(fold=-1)

# Simulate and plot results
qasm_simulator = Aer.get_backend('qasm_simulator')
transpiled_qc = transpile(qc, qasm_simulator)
results = qasm_simulator.run(transpiled_qc).result()
counts = results.get_counts()
plot_histogram(counts)




