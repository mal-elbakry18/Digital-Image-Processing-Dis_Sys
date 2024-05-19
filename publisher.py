
import boto3
import json
import uuid

sns = boto3.client('sns', region_name='us-east-1')
topic_arn = 'arn:aws:sns:us-east-1:654654278566:MyTopicDisProject.fifo'

def publish_message(image_path, operation):
    message = {
        'imageUrl': image_path,  # Path to the local image
        'operation': operation
    }
    deduplication_id = str(uuid.uuid4())  # Generate a unique deduplication ID
    sns.publish(
        TopicArn=topic_arn,
        Message=json.dumps(message),
        MessageDeduplicationId=deduplication_id,
        MessageGroupId='1'  # Provide a message group ID for FIFO topics
    )

if __name__ == '__main__':
    image_path = 'Test_img.jpeg'  # Local path to your image
    operation = 'edge_detection'
    publish_message(image_path, operation)
    print('Message published to SNS')
