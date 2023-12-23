from PIL import Image
import numpy as np

from HammingCoder import HammingCoder


def binary_symmetric_channel(array, flip_prob):
    # Create an empty array to store the output
    output_array = np.copy(array)

    # Apply the channel to each pixel
    for i in range(len(array)):
        if np.random.random() < flip_prob:
            # Flip the bit (invert pixel value)
            output_array[i] = 1 - array[i]

    return output_array

def flatten_image(image):
    # Flatten the 2D image array into a 1D array
    return [pixel for row in image for pixel in row]

def reshape_image(encoded_data, original_shape):
    # Reshape the 1D encoded data into the original 2D image shape
    return [encoded_data[i:i + original_shape[1]] for i in range(0, len(encoded_data), original_shape[1])]


if __name__ == '__main__':
    image = Image.open("bw_dino.png")  # Replace with the path to your image

    # Convert the image to grayscale
    gray_image = image.convert("L")

    # Convert the grayscale image to an array
    image_array = np.array(gray_image)

    # Threshold the image to get a binary representation
    threshold = 128  # threshold for pixel values
    binary_array = (image_array > threshold).astype(int)

    # Flatten into 1d array for easier handling
    flattened_array = flatten_image(binary_array)

    # Encode with the 4,7 Hamming code
    hamming_coder = HammingCoder()
    encoded_array = hamming_coder.hamming_encode(flattened_array)

    channel_array = binary_symmetric_channel(encoded_array, 0.1)

    decoded_array = hamming_coder.hamming_decode(channel_array)
    decoded_image = reshape_image(decoded_array, (len(image_array), len(image_array[0])))

    np_array = np.array(decoded_image * 255)
    image_array = np_array.astype(np.uint8)

    output_image = Image.fromarray(image_array)
    output_image.save("bw_dino_3.png")
    # Print the binary array
    print(binary_array)
