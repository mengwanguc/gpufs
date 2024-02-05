import pika
import json
import uuid

app_id = str(uuid.uuid4())

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
request_queue = 'gpu_requests'
channel = connection.channel()
callback_queue =  f'response_{app_id}'
result = channel.queue_declare(queue=callback_queue, exclusive=True)

def on_response(ch, method, props, body):
    response = json.loads(body)
    if response['app_id'] == app_id:
        print(f"Received GPU processing completion: {response}")

channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)


def send_gpu_request(processing_time):
    request = json.dumps({'app_id': app_id, 'processing_time': processing_time})
    channel.basic_publish(exchange='',
                          routing_key=request_queue,
                          properties=pika.BasicProperties(reply_to=callback_queue, correlation_id=app_id),
                          body=request)
    print(f"App {app_id} requested GPU processing.")

# Example request for GPU processing
send_gpu_request(2)  # Requesting 2 seconds of GPU processing

channel.start_consuming()
