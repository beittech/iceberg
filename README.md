# Iceberg Codes

A Python library for quantum error detection, providing tools to compile, simulate, and decode quantum circuits using Iceberg codes. This library integrates seamlessly with Qiskit, making it easy to detect and mitigate errors in quantum circuits.

## Installation

You can install Iceberg Codes directly from GitHub using pip:

```bash
pip install git+https://github.com/beittech/iceberg.git
```

## Usage

Here's a quick example demonstrating basic usage:

```python
from qiskit import transpile
from qiskit.circuit.library import quantum_volume
import iceberg_codes as ice
from qiskit_aer import AerSimulator

# Generate a quantum volume circuit
qc = quantum_volume(k := 4, 2, seed=42)
qc.append(qc.inverse(), qc.qubits)

# Compile the circuit with Iceberg error detection
qc_compiled = transpile(ice.compile(qc, syndrome_rate=16), basis_gates=['x', 'z', 'rz', 'rx', 'rzz'])

# Simulate and decode results
sim = AerSimulator()
counts = sim.run(qc_compiled, shots=2048)
decoded_result = ice.decode(counts, k=k)

print(decoded_result.probabilities_dict())
```

## Tutorial

A complete interactive tutorial is available in the `tutorials` directory.

## Requirements

- Qiskit
- Qiskit Aer
- NumPy

## License

This project is licensed under the MIT License.

