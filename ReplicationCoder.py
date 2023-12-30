import numpy as np


class ReplicationCoder:
    _repetitions = 3

    def __init__(self, repetitions):
        _repetitions = repetitions

    def encode(self, data):
        return np.repeat(data, self._repetitions)

    def decode(self, encoded_data):
        decoded_data = []
        for block in np.split(encoded_data, int(len(encoded_data)/self._repetitions)):
            if sum(block < 1):
                decoded_data.append(1)
            else:
                decoded_data.append(0)

        return decoded_data
