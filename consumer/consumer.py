import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='tweet')

def callback(ch, method, properties, body):
    tw = json.loads(body)
    print(tw)
    
channel.basic_consume(queue='tweet', on_message_callback=callback, auto_ack=True)

channel.start_consuming()