import zmq
from mpi4py import MPI
import numpy as np

def create_pub_socket(bind_address):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(bind_address)
    return socket

def create_sub_socket(connect_address, topics):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(connect_address)
    for topic in topics:
        socket.setsockopt_string(zmq.SUBSCRIBE, topic)
    return socket

def create_push_socket(bind_address):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind(bind_address)
    return socket

def create_pull_socket(connect_address):
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.connect(connect_address)
    return socket

def process_image_chunk(image_chunk):
    # Perform image processing on the chunk
    # Example: Apply a filter or some other transformation
    processed_chunk = image_chunk  # Placeholder for actual processing
    return processed_chunk

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # Initialize sockets based on rank
    if rank == 0:
        # Root node: publisher and pusher
        pub_socket = create_pub_socket("tcp://127.0.0.1:2000")
        push_socket = create_push_socket("tcp://127.0.0.1:2000")
    else:
        # Non-root nodes: subscriber and puller
        sub_socket = create_sub_socket("tcp://127.0.0.1:2000", ["topic1"])
        pull_socket = create_pull_socket("tcp://127.0.0.1:2000")

    if rank == 0:
        # Load the image on the root node
        image = np.load("image.npy")

        # Calculate chunk size
        chunk_size = len(image) // size

        # Scatter image chunks to nodes/VMs
        for i in range(1, size):
            start_idx = i * chunk_size
            end_idx = start_idx + chunk_size
            comm.send(image[start_idx:end_idx], dest=i)

        # Process the image chunk locally on the root node
        processed_chunk = process_image_chunk(image[:chunk_size])

        # Publish processed chunk
        pub_socket.send_string("topic1", np.array2string(processed_chunk))

        # Gather processed chunks back to the root node
        for i in range(1, size):
            processed_chunk = comm.recv(source=i)
            processed_image[start_idx:end_idx] = processed_chunk

        # Save or display the processed image
        np.save("processed_image.npy", processed_image)
        print("Image processing completed.")
    else:
        # Receive image chunk from the root node
        image_chunk = comm.recv(source=0)

        # Process the image chunk locally on the non-root nodes
        processed_chunk = process_image_chunk(image_chunk)

        # Send processed chunk to the root node
        comm.send(processed_chunk, dest=0)

if __name__ == "__main__":
    main()
