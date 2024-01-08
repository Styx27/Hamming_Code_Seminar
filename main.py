from PIL import Image
import numpy as np

from HammingCoder import HammingCoder
from ReplicationCoder import ReplicationCoder

channel_flip_prob = 0.01
filename = "letter_A"  # filename without format


def binary_symmetric_channel(array, flip_prob):
    # Create an empty array to store the output
    output_array = np.copy(array)

    # Apply the channel to each pixel
    for i in range(len(array)):
        if np.random.random() < flip_prob:
            # Flip the bit (invert pixel value)
            output_array[i] = 1 - array[i]

    return output_array


def reformat_array(array, shape):
    np_array = np.array(array)
    np_array = np_array.reshape(shape)
    return np.array(np_array * 255, dtype=np.uint8)


if __name__ == '__main__':
    image = Image.open(filename + ".png")

    # Convert the image to grayscale
    gray_image = image.convert("L")

    # Convert the grayscale image to an array
    image_array = np.array(gray_image)
    threshold = 128  # threshold for pixel values
    binary_array = (image_array > threshold).astype(int)  # Conversion into binary array

    # Flatten into 1d array for easier handling
    flattened_binary_array = binary_array.flatten()

    # Baseline without encoding

    channel_array_baseline = binary_symmetric_channel(flattened_binary_array, channel_flip_prob)

    output_image_baseline = Image.fromarray(reformat_array(channel_array_baseline, binary_array.shape))
    output_image_baseline.save(filename + "_baseline.png")

    # Encode with the Hamming code

    hamming_coder = HammingCoder(4)  # Insert 1, 4, 11, 26, 57, 120
    encoded_array_hamming = hamming_coder.hamming_encode(flattened_binary_array)
    channel_array_hamming = binary_symmetric_channel(encoded_array_hamming, channel_flip_prob)
    decoded_array_hamming = hamming_coder.hamming_decode(channel_array_hamming)

    output_image_hamming = Image.fromarray(reformat_array(decoded_array_hamming, binary_array.shape))
    output_image_hamming.save(filename + "_hamming.png")

    # Replication Coding
    replication_coder = ReplicationCoder(3)

    encoded_array_replication = replication_coder.encode(flattened_binary_array)
    channel_array_replication = binary_symmetric_channel(encoded_array_replication, channel_flip_prob)
    decoded_array_replication = replication_coder.decode(channel_array_replication)

    output_image_replication = Image.fromarray(reformat_array(decoded_array_replication, binary_array.shape))
    output_image_replication.save(filename + "_repetition.png")
