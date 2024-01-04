from functools import reduce


class HammingCoder:
    redundant_bits_count = 0
    message_size = 0

    def __init__(self, message_size):
        self.message_size = message_size
        # Calculate redundant bits positions
        for i in range(message_size):
            if 2 ** i >= message_size + i + 1:
                self.redundant_bits_count = i
                break
        self.padding = 0

    def __split_into_chunks(self, data, chunk_size):
        # Pad the data with zeros to make its length divisible by chunk_size
        padding = (chunk_size - len(data) % chunk_size) % chunk_size
        if padding != 0:
            padded_data = data + [0] * padding
        else:
            padded_data = data

        self.padding = padding

        # Split the padded data into chunks
        return [padded_data[i:i + chunk_size] for i in range(0, len(padded_data), chunk_size)]

    def remove_padding(self, data):
        # Remove the padding added during the __split_into_chunks method
        return data[:-self.padding] if self.padding > 0 else data

    def hamming_encode(self, data):

        encoded_data = []

        blocks = self.__split_into_chunks(data, self.message_size)

        for block in blocks:
            encoded_block = []
            # Position parity bits
            current_base = 0
            current_data_pos = 0
            for i in range(1, self.message_size + self.redundant_bits_count + 1):
                if i == 2 ** current_base:
                    encoded_block.append(0)
                    current_base += 1
                else:
                    encoded_block.append(block[current_data_pos])
                    current_data_pos += 1

            # Calculate Value of parity bits

            for i in range(self.redundant_bits_count):
                parity_position = 2 ** i  # 1-indexed position
                count = 0
                for bit_position in range(1, len(encoded_block) + 1):
                    if bit_position & parity_position != 0:
                        if encoded_block[bit_position - 1] == 1:
                            count += 1

                # Even Parity
                if count % 2 == 0:
                    encoded_block[parity_position - 1] = 0
                else:
                    encoded_block[parity_position - 1] = 1

            encoded_data = encoded_data + encoded_block

        return encoded_data

    def hamming_decode(self, encoded_data):

        decoded_data = []
        blocks = self.__split_into_chunks(encoded_data, self.message_size + self.redundant_bits_count)
        for block in blocks:
            decoded_block = list(block)

            # Do parity checks again
            syndrome = []
            for i in reversed(range(self.redundant_bits_count)):
                parity_pos = 2 ** i
                count = 0
                for bit_position in range(1, len(block) + 1):
                    if parity_pos & bit_position != 0:
                        if block[bit_position - 1] == 1:
                            count += 1

                if count % 2 == 0:
                    syndrome.append(0)
                else:
                    syndrome.append(1)

            # Convert bits to integer
            error_position = int("".join(str(x) for x in syndrome), 2)

            # Fix error if there is one
            if error_position != 0:
                decoded_block[error_position - 1] = 1 - decoded_block[error_position - 1]

            decoded_block2 = []
            # Remove parity bits
            exponent = 0
            for position in range(1, len(decoded_block) + 1):
                if 2 ** exponent == position:
                    exponent += 1
                else:
                    decoded_block2.append(decoded_block[position - 1])

            decoded_data = decoded_data + decoded_block2

        return decoded_data
