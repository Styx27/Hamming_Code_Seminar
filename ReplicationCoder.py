import numpy as np
from collections import Counter

class ReplicationCoder:

    _repetitions = 3
    def __init__(self, repetitions):
        _repetitions = repetitions
    def encode(self, data):
        return np.repeat(data, self._repetitions)

    def decode(self, encoded_data):
        decoded_data = []
        for block in np.split(encoded_data, self._repetitions):
            vote_count = Counter(block)
            decoded_data.append(vote_count.most_common(2))

            



