import pika
import time
import json

def on_request(ch, method, props, body):
    request = json.loads(body)
    print(f"Processing request from App {request['app_id']} for GPU access.")

    # Simulate GPU processing time
    print(request)
    time.sleep(request['processing_time'])
    # print('hi')

    response = json.dumps({'app_id': request['app_id'], 'status': 'completed'})
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print(f"Completed processing for App {request['app_id']}.")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='gpu_requests')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='gpu_requests', on_message_callback=on_request)

print("GPU Manager started. Awaiting requests.")
channel.start_consuming()
