import numpy as np
from abc import ABCMeta, abstractmethod

class IErrorDetector (metaclass=ABCMeta) :

    @abstractmethod
    def encode(self, array):
        pass

    @abstractmethod
    def decode(self, array):
        pass

class ParityDetector(IErrorDetector) :

    def encode(self, array) :
        output_array = np.ndarray()
        for i in range(array.shape[0]):
            output_line = np.copy(array[i])
            parity_bit = 0;
            if sum(array[i]) % 2 != 0:
                parity_bit = 1;
            output_line = output_line + parity_bit
            output_array = output_array + output_line


    def decode(self, array):
        return array