import numpy as np
import qiskit_aer


class DecoderError(Exception):
    """Exception raised when decoding fails due to invalid syndromes or other critical errors."""
    pass


class DecodedResults:
    """
    Encapsulates decoded quantum measurement results and related statistics.

    Attributes:
        counts (dict[str, int]):
            Dictionary mapping decoded bitstrings to their occurrence counts.
        invalid (int):
            Number of measurement outcomes discarded due to failing syndrome checks.
        valid_count (int):
            Total number of measurement outcomes that passed syndrome checks.
        shots (int):
            Total number of measurement outcomes (valid + invalid).
        survival_rate (float):
            Ratio of valid outcomes to total shots.
    """

    def __init__(self, counts: dict[str, int], invalid: int):
        """
        Initializes the DecodedResults instance.

        Parameters:
            counts (dict[str, int]):
                Dictionary of decoded bitstring counts.
            invalid (int):
                Number of discarded (invalid) measurement results.
        """
        self.counts = counts
        self.invalid = invalid
        self.valid_count = sum(counts.values())
        self.shots = invalid + sum(counts.values())
        self.survival_rate = self.valid_count / self.shots
        self._probabilities_dict = {k: v / self.valid_count for k, v in self.counts.items()}

    def __str__(self):
        counts = '{' + ', '.join([f'{a}: {b}' for a, b in list(self.counts.items())[:3]]) + ', ...}'
        return (f'DecodedResults(shots={self.shots}, '
                f'survival_rate={self.survival_rate}, '
                f'invalid={self.invalid}, '
                f'counts={counts})')

    def probabilities_dict(self):
        """
        Returns the probability distribution of the decoded measurement results.

        Returns:
            dict[str, float]:
                Mapping of decoded bitstrings to their probabilities.
        """
        return self._probabilities_dict


class IcebergDecoder:
    """
    Decodes quantum circuit measurement results using the Iceberg error-detecting code.

    Attributes:
        k (int): Number of logical data qubits.
        n (int): Total number of physical qubits (k + k % 2 + 2).
    """

    def __init__(self, k):
        """
        Initializes the IcebergDecoder instance.

        Parameters:
            k (int): Number of logical data qubits.
        """
        self.k = k + k % 2
        self.n = k + 2
        tf = np.concatenate(
            [np.zeros((k, 1), dtype=bool), (1 - np.eye(k, dtype=bool)), np.ones((k, 1), dtype=bool)], -1
        )
        self._decoder_transform = np.concat((tf[0][None, ...], tf[1:][::-1]))

    def __call__(self, counts: dict[str, int]) -> DecodedResults:
        """
        Decodes measurement results from a quantum circuit run, filtering out invalid results
        based on syndrome checks and applying the decoder transform.

        Parameters:
            counts (dict[str, int]):
                A dictionary mapping measurement bitstrings to their corresponding counts.

        Returns:
            DecodedResults:
                An object containing decoded results and statistics.

        Raises:
            DecoderError:
                If no valid measurement outcomes pass syndrome checks.
        """
        invalid = 0
        count_vals = []
        states = []
        for k, v in counts.items():
            regs = k.split()
            flags = np.array(regs[:-1], dtype=int)
            data = np.array(list(regs[-1]), dtype=int)
            syndrome_check_passed = np.all(flags == 0) and ((data.sum() % 2) == 0)
            if syndrome_check_passed:
                count_vals.append(v)
                states.append(data)
            else:
                invalid += v

        if len(states) == 0:
            raise DecoderError('Syndrome checks failed for all shots! Consider (1) reducing your '
                               'circuit complexity and/or (2) increasing the number of samples')

        states = np.array(states)

        decoded = (states @ self._decoder_transform.T) % 2

        decoded_counts = {}
        for s, c in zip(decoded, count_vals):
            s = ''.join(map(str, s))
            decoded_counts[s] = decoded_counts.get(s, 0) + c

        return DecodedResults(decoded_counts, invalid)


def decode(counts: dict[str, int] | qiskit_aer.jobs.aerjob.AerJob, k: int) -> DecodedResults:
    """
    Decodes measurement counts from either a dictionary or an AerJob object.

    This function acts as a convenient wrapper around the IcebergDecoder class, automatically
    handling extraction of counts from Aer simulator jobs if necessary.

    Parameters:
        counts (dict[str, int] | qiskit_aer.jobs.aerjob.AerJob):
            Measurement counts from a quantum circuit execution or a completed Aer simulator job.
        k (int):
            Number of logical data qubits.

    Returns:
        DecodedResults:
            Object containing decoded outcomes and statistics.
    """
    dec = IcebergDecoder(k)
    if isinstance(counts, qiskit_aer.jobs.aerjob.AerJob):
        counts = counts.result().get_counts()
    return dec(counts)
