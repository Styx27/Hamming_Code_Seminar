from PIL import Image
import numpy as np

from HammingCoder import HammingCoder
from ReplicationCoder import ReplicationCoder

channel_flip_prob = 0.1


def binary_symmetric_channel(array, flip_prob):
    # Create an empty array to store the output
    output_array = np.copy(array)

    # Apply the channel to each pixel
    for i in range(len(array)):
        if np.random.random() < flip_prob:
            # Flip the bit (invert pixel value)
            output_array[i] = 1 - array[i]

    return output_array



if __name__ == '__main__':
    image = Image.open("bw_dino.png")  # Replace with the path to your image

    # Convert the image to grayscale
    gray_image = image.convert("L")

    # Convert the grayscale image to an array
    image_array = np.array(gray_image)

    threshold = 128  # threshold for pixel values
    binary_array = (image_array > threshold).astype(int) #Conversion into binary array

    # Flatten into 1d array for easier handling
    flattened_binary_array = binary_array.flatten()



    #Baseline without encoding

    channel_array_baseline = binary_symmetric_channel(flattened_binary_array, channel_flip_prob)

    output_image_baseline = Image.fromarray(channel_array_baseline.reshape(binary_array.shape))
    output_image_baseline.save("bw_dino_baseline.png")



    # Encode with the 4,7 Hamming code

    hamming_coder = HammingCoder(4)
    encoded_array_hamming = hamming_coder.hamming_encode(flattened_binary_array)
    channel_array_hamming = binary_symmetric_channel(encoded_array_hamming, channel_flip_prob)
    decoded_array_hamming = hamming_coder.hamming_decode(channel_array_hamming)

    output_image_hamming = Image.fromarray(decoded_array_hamming.reshape(binary_array.shape))
    output_image_hamming.save("bw_dino_hamming.png")


    replication_coder = ReplicationCoder(3)
    #encoded_array = hamming_coder.hamming_encode(flattened_array)
    encoded_array = replication_coder.encode(flattened_array)

    channel_array = binary_symmetric_channel(encoded_array, 0)

    #decoded_array = hamming_coder.hamming_decode(channel_array)
    decoded_array = replication_coder.decode(channel_array)
    decoded_np_array = np.array(decoded_array)
    decoded_image = decoded_np_array.reshape(binary_array.shape)
    decoded_image = np.logical_not(decoded_image).astype(int)
    np_array = np.array(decoded_image * 255)
    image_array = np_array.astype(np.uint8)

    output_image = Image.fromarray(image_array)
    output_image.save("bw_dino_replication.png")
    # Print the binary array
    print(binary_array)
