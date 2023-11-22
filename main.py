
from PIL import Image
import numpy as np
import random

def binary_symmetric_channel(array, flip_prob):
    # Create an empty array to store the output
    output_array = np.copy(array)

    # Apply the channel to each pixel
    for i in range(array.shape[0]):
        for j in range(array.shape[1]):
            if np.random.random() < flip_prob:
                # Flip the bit (invert pixel value)
                output_array[i, j] = 1 - array[i, j]

    return output_array


if __name__ == '__main__':
    image = Image.open("bw_dino.png")  # Replace with the path to your image

    # Convert the image to grayscale
    gray_image = image.convert("L")

    # Convert the grayscale image to a NumPy array
    image_array = np.array(gray_image)

    # Threshold the image to get a binary representation
    threshold = 128  # Adjust this threshold as needed
    binary_array = (image_array > threshold).astype(int)

    binary_array = binary_symmetric_channel(binary_array, 0.1)

    image_array = (binary_array * 255).astype(np.uint8)

    output_image = Image.fromarray(image_array)
    output_image.save("bw_dino_2.png")
    # Print the binary array
    print(binary_array)
