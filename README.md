# Iceberg Analysis Library

This library allows users to:

- Send a Qiskit circuit to a backend compiler API.
- Simulate the compiled circuit using a circuit-level noise model.
- Decode the simulation results with post-selection using the Iceberg decoder.

## Installation

```bash
pip install iceberg
```

## Example Usage
```python
from qiskit import QuantumCircuit
from qiskit.circuit.random import random_circuit
from iceberg.compiler import compile_circuit_api
from iceberg.noise import circuit_level_noise_model
from iceberg.simulation import simulate_circuit, plot_results
from iceberg.decoder import decode_counts

# Create a test circuit
k = 4
qc = QuantumCircuit(k)
rc = random_circuit(k, depth=5, seed=42)
qc.compose(rc, inplace=True)

# Compile the circuit (using QASM format in this example)
compiled_qc = compile_circuit_api(qc, syndrome_rate=16, input_format="qasm")

# Create a noise simulator with error rate 0.001
simulator = circuit_level_noise_model(0.001)

# Simulate the compiled circuit
counts = simulate_circuit(simulator, compiled_qc, shots=1024)

# Decode the simulation results with post-selection
decoded_counts = decode_counts(counts, k)

# Plot the results
plot_results(decoded_counts)
```# iceberg
