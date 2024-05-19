from mpi4py import MPI
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Define image processing functions
def process_image(image, operation):
    if operation == 'edge_detection':
        result = cv2.Canny(image, 100, 200)
    elif operation == 'color_inversion':
        result = cv2.bitwise_not(image)
    elif operation == 'grayscale':
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif operation == 'blur':
        result = cv2.GaussianBlur(image, (15, 15), 0)
    elif operation == 'threshold':
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, result = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    elif operation == 'dilate':
        kernel = np.ones((5, 5), np.uint8)
        result = cv2.dilate(image, kernel, iterations=1)
    elif operation == 'erode':
        kernel = np.ones((5, 5), np.uint8)
        result = cv2.erode(image, kernel, iterations=1)
    # Add more operations as needed
    return result

def save_image(result, output_path):
    cv2.imwrite(output_path, result)

def plot_image(result):
    if len(result.shape) == 2:  # Grayscale image
        plt.imshow(result, cmap='gray')
    else:  # Color image
        plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title('Processed Image')
    plt.axis('off')
    plt.show()

def worker(image_paths, operation, output_dir, plot_results):
    for i, image_path in enumerate(image_paths):
        if i % size == rank:  # Distribute work among ranks
            print(f"Rank {rank} starting processing on {image_path}")
            image = cv2.imread(image_path)
            if image is not None:
                result = process_image(image, operation)
                if plot_results:
                    plot_image(result)
                else:
                    output_path = os.path.join(output_dir, f'processed_image_{rank}_{i}.jpg')
                    save_image(result, output_path)
                    print(f"Image processed by rank {rank} and saved to {output_path}")
            print(f"Rank {rank} completed processing on {image_path}")

if __name__ == '__main__':
    # Parameters
    image_dir_or_file = 'Test_img.jpeg'
    output_dir = '/Users/malakelbakry/Downloads/Distributed Project'
    operation = 'edge_detection'  # Choose your operation here
    plot_results = False  # Set to True if you want to plot results instead of saving

    # Check if the path is a directory or a single file
    if os.path.isdir(image_dir_or_file):
        # Gather all image paths in the directory
        image_paths = [os.path.join(image_dir_or_file, fname) for fname in os.listdir(image_dir_or_file) if fname.endswith(('.jpg', '.jpeg', '.png'))]
    else:
        # Use the single file path
        image_paths = [image_dir_or_file]

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the worker function
    worker(image_paths, operation, output_dir, plot_results)
