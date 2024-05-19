from mpi4py import MPI
import boto3
import cv2
import json
import time
import os
import matplotlib.pyplot as plt

sqs = boto3.client('sqs', region_name='us-east-1')
queue_url = 'https://sqs.us-east-1.amazonaws.com/654654278566/MyQueueDistributedProject'

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

def process_image(image_path, operation):
    # Load the image
    image = cv2.imread(image_path)
    
    # Perform the specified operation
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
    
    return result

def save_image(result, output_path):
    cv2.imwrite(output_path, result)

def plot_image(result):
    plt.imshow(result, cmap='gray')
    plt.title('Processed Image')
    plt.axis('off')
    plt.show()

def worker(operation, output_dir, plot_results):
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,  # Adjust as needed
            WaitTimeSeconds=10
        )

        messages = response.get('Messages', [])
        if not messages:
            continue

        for message in messages:
            body = json.loads(message['Body'])
            image_url = body['imageUrl']
            operation = body['operation']

            if image_url.startswith('s3://'):
                # Download the image from S3
                s3 = boto3.client('s3')
                bucket_name, key = image_url[5:].split('/', 1)
                local_image_path = '/tmp/' + key.split('/')[-1]
                s3.download_file(bucket_name, key, local_image_path)
                image_path = local_image_path
            else:
                image_path = image_url  # Assume it's a local path

            print(f"Rank {rank} starting processing on {image_path}")
            if os.path.exists(image_path):
                result = process_image(image_path, operation)
                if plot_results:
                    plot_image(result)
                else:
                    output_path = os.path.join(output_dir, f'processed_image_{rank}_{time.time()}.jpg')
                    save_image(result, output_path)
                    print(f"Image processed by rank {rank} and saved to {output_path}")
            
            # Delete the message from the queue
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
        
        time.sleep(1)

if __name__ == '__main__':
    # Parameters
    output_dir = '/Users/malakelbakry/Downloads/Distributed Project/worker_thread_2.py'
    plot_results = False # Set to True if you want to plot results instead of saving
    operation = 'edge_detection'  # This should be dynamic based on message

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Run the worker function
    worker(operation, output_dir, plot_results)
