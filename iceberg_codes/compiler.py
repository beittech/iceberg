import base64
from io import BytesIO
import requests
from qiskit import QuantumCircuit, qpy

ENDPOINT = "https://api.codeqraft.xyz/compile"


def compile(qc: QuantumCircuit, syndrome_rate: int = 16) -> QuantumCircuit:
    """
    Compiles a given quantum circuit using Iceberg's remote compilation API, introducing periodic syndrome
    measurements to enable quantum error detection.

    The compilation process encodes error detection routines into the circuit at intervals determined by the
    specified syndrome rate, resulting in a compiled quantum circuit optimized for execution on quantum hardware.

    Parameters:
        qc (QuantumCircuit):
            The input quantum circuit to compile.

        syndrome_rate (int, optional):
            The frequency (in gate layers) at which syndrome measurements are inserted for error detection.
            Lower values provide more frequent error checks, potentially improving error mitigation but
            increasing circuit depth and complexity. Default is 16.

    Returns:
        QuantumCircuit:
            A new quantum circuit object, representing the compiled circuit with embedded error detection.

    Raises:
        ValueError:
            If the compilation API returns an unsuccessful response or encounters an error during compilation.
    """

    buf = BytesIO()
    qpy.dump(qc, buf)
    qpy_bytes = buf.getvalue()
    qpy_b64 = base64.b64encode(qpy_bytes).decode('utf-8')

    payload = {
        "qpy_base64": qpy_b64,
        "syndrome_rate": syndrome_rate
    }

    response = requests.post(ENDPOINT, json=payload)
    if response.status_code != 200:
        raise ValueError(response.text)

    data = response.json()
    compiled_bytes = base64.b64decode(data["qpy_base64"])
    buf = BytesIO(compiled_bytes)
    return qpy.load(buf)[0]
