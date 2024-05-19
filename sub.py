import zmq

def create_sub_socket(connect_address, topics):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(connect_address)
    for topic in topics:
        socket.setsockopt_string(zmq.SUBSCRIBE, topic)
    return socket

def receive_processed_images(sub_socket):
    while True:
        topic, processed_chunk = sub_socket.recv_multipart()  # Receive topic and message parts
        print(f"Received processed image chunk with topic {topic.decode()}")

       
        with open(f"processed_image_chunk_{topic.decode()}.npy", "wb") as f:
            f.write(processed_chunk)

def main():
    # Connect to the PUB socket of the publisher
    sub_socket = create_sub_socket("tcp://127.0.0.1:2000", ["topic1"])

    # Receive and process processed image chunks
    receive_processed_images(sub_socket)

if __name__ == "__main__":
    main()
