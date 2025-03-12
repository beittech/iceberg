from qiskit import qpy, qasm3, QuantumCircuit


def load_qpy(qpy_path: str) -> QuantumCircuit:
    """
    Load a quantum circuit from a QPY file.

    Parameters:
        qpy_path (str):
            The path to the QPY file to load.

    Returns:
        QuantumCircuit:
            The loaded quantum circuit object.
    """
    with open(qpy_path, 'rb') as f:
        return qpy.load(f)[0]


def load_qasm(qasm_path: str) -> QuantumCircuit:
    """
    Load a quantum circuit from a QASM file.

    Parameters:
        qasm_path (str):
            The path to the QASM file to load.

    Returns:
        QuantumCircuit:
            The loaded quantum circuit object.
    """
    return qasm3.load(qasm_path)
