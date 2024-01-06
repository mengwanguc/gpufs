
class App:
    def __init__(self):
        app_id = str(uuid.uuid4())
        self.request_topic = 'batch_requests'
        self.response_topic = f'response_{app_id}'

        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.consumer = KafkaConsumer(response_topic, bootstrap_servers='localhost:9092',
                                auto_offset_reset='earliest', enable_auto_commit=True)
    

    def emuSharedCompute(batch_compute_time):
        batch_start = time.time()
        message = json.dumps({'app_id': app_id, 'batch_id': batch_id, 'duration': batch_compute_time, 'response_topic': response_topic})
        producer.send(request_topic, message.encode('utf-8'))
        # Wait for response
        for message in consumer:
            break  # Exit after receiving the response