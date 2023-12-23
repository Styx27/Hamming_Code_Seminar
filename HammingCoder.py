class HammingCoder:
    def __init__(self):
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

        blocks = self.__split_into_chunks(data, 4)

        for block in blocks:
            # Calculate parity bits
            parity_bits = [0, 0, 0]
            parity_bits[0] = block[0] ^ block[1] ^ block[3]
            parity_bits[1] = block[0] ^ block[2] ^ block[3]
            parity_bits[2] = block[1] ^ block[2] ^ block[3]

            # Create the encoded message
            encoded_block = [block[0], block[1], parity_bits[0], block[2], parity_bits[1], parity_bits[2], block[3]]
            encoded_data = encoded_data + encoded_block

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
