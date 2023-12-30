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
                    encoded_block = encoded_block.append(0)
                    current_base += 1
                else:
                    encoded_block = encoded_block.append(block[-1 * current_data_pos])
                    current_data_pos += 1

            # Reverse block since positions are counted backwards
            encoded_data.append(encoded_block[::-1])

        return encoded_data

    def hamming_decode(self, encoded_data):

        decoded_data = []
        blocks = self.__split_into_chunks(encoded_data, 7)

        for block in blocks:
            # Calculate syndrome bits
            syndrome = [
                block[0] ^ block[2] ^ block[4] ^ block[6],
                block[1] ^ block[2] ^ block[5] ^ block[6],
                block[3] ^ block[4] ^ block[5] ^ block[6]
            ]

            # Check for errors and correct if possible
            error_position = syndrome[0] + syndrome[1] * 2 + syndrome[2] * 4

            if error_position != 0:
                print("Error at position", error_position)
                # Correct the error
                block[error_position - 1] ^= 1

            # Extract the original data
            decoded_block = [block[0], block[1], block[3], block[6]]
            decoded_data = decoded_data + decoded_block

        return decoded_data
