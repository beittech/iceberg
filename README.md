# Iceberg Codes

A Python library for quantum error detection, providing tools to compile, simulate, and decode quantum circuits using
Iceberg codes. This library integrates seamlessly with Qiskit, making it easy to detect and mitigate errors in quantum
circuits.

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

## Citation

If you use Iceberg Codes in your research, please cite the following papers:

```bibtex
@misc{ginsberg2025quantumerrordetectionearly,
    title = {Quantum Error Detection For Early Term Fault-Tolerant Quantum Algorithms},
    author = {Tom Ginsberg and Vyom Patel},
    year = {2025},
    eprint = {2503.10790},
    archivePrefix = {arXiv},
    primaryClass = {quant-ph},
    url = {https://arxiv.org/abs/2503.10790},
}

@article{Self_2024,
    title={Protecting expressive circuits with a quantum error detection code},
    volume={20},
    ISSN={1745-2481},
    url={http://dx.doi.org/10.1038/s41567-023-02282-2},
    DOI={10.1038/s41567-023-02282-2},
    number={2},
    journal={Nature Physics},
    publisher={Springer Science and Business Media LLC},
    author={Self, Chris N. and Benedetti, Marcello and Amaro, David},
    year={2024},
    month=jan, pages={219–224} }

```