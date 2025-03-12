from itertools import product
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, ReadoutError, pauli_error


def parametric_circuit_noise_model(p_single_qubit: float, p_two_qubit: float, p_measure: float) -> AerSimulator:
    """
    Creates a customizable Qiskit Aer noise model with distinct error probabilities for
    single-qubit gates, two-qubit gates, and measurement/reset operations.

    Parameters:
        p_single_qubit (float):
            Probability of single-qubit Pauli errors (X, Y, Z) occurring on single-qubit gates.

        p_two_qubit (float | None):
            Probability of two-qubit Pauli errors occurring on two-qubit gates (e.g., CX, RZZ).
            If set to None, two-qubit gates remain error-free.

        p_measure (float | None):
            Probability of measurement and reset errors. If None, measurement and reset
            operations remain error-free.

    Returns:
        AerSimulator:
            A Qiskit Aer simulator configured with the specified noise model.
    """
    noise_model = NoiseModel()

    # Two-Qubit Pauli Error
    if p_two_qubit is not None:
        two_qubits_errors = [
            ''.join(err) for err in product(['X', 'Y', 'Z', 'I'], repeat=2)
            if err != ('I', 'I')
        ]
        n_two_qubits_errors = len(two_qubits_errors)
        two_qubit_pauli_error = pauli_error(
            [(err, p_two_qubit / n_two_qubits_errors) for err in two_qubits_errors] +
            [('II', 1 - p_two_qubit)]
        )
        noise_model.add_all_qubit_quantum_error(two_qubit_pauli_error, ['cx', 'rzz'])

    # Single-Qubit Pauli Error
    single_qubit_errors = ['X', 'Y', 'Z']
    single_qubit_pauli_error = pauli_error(
        [(err, p_single_qubit / 3) for err in single_qubit_errors] +
        [('I', 1 - p_single_qubit)]
    )
    noise_model.add_all_qubit_quantum_error(single_qubit_pauli_error, ['u', 'h', 'x', 'y', 'z', 'id'])

    # Measurement Error
    if p_measure is not None:
        meas_error = ReadoutError([[1 - p_measure, p_measure], [p_measure, 1 - p_measure]])
        noise_model.add_all_qubit_readout_error(meas_error)

        reset_error = pauli_error(
            [(err, p_measure / 3) for err in single_qubit_errors] +
            [('I', 1 - p_measure)]
        )
        noise_model.add_all_qubit_quantum_error(reset_error, ['reset'])

    return AerSimulator(noise_model=noise_model)


def circuit_noise_model(p: float) -> AerSimulator:
    """
    Convenience function that sets an identical error rate for single-qubit gates,
    two-qubit gates, and measurement/reset operations.

    Parameters:
        p (float 0<=p<=1):
            The uniform probability applied to single-qubit, two-qubit, and measurement/reset errors.

    Returns:
        AerSimulator:
            A Qiskit Aer simulator configured with the specified uniform noise model.
    """
    return parametric_circuit_noise_model(p_single_qubit=p, p_two_qubit=p, p_measure=p)
