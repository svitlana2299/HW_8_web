import pika
from mongoengine import connect
from models import Contact

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# Створення черги для SMS
channel.queue_declare(queue='sms_queue')

# Підключення до MongoDB
connect(connect('svitlana',
        host='mongodb+srv://svitlana:JHp56XKEKjpAnMqF@atlascluster.9lwm8qe.mongodb.net/'))


def send_sms_stub(contact_id):
    # Тут можна імітувати надсилання SMS
    print(f"Sending SMS to contact with ID: {contact_id}")
    return True


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()

    if contact:
        if not contact.email_sent:
            if send_sms_stub(contact_id):
                contact.email_sent = True
                contact.save()
                print(
                    f"SMS sent and updated for contact with ID: {contact_id}")
        else:
            print(f"SMS already sent for contact with ID: {contact_id}")
    else:
        print(f"Contact with ID {contact_id} not found")


# Обробка повідомлень з черги для SMS
channel.basic_consume(
    queue='sms_queue', on_message_callback=callback, auto_ack=True)

print("SMS Consumer is waiting for messages. To exit press CTRL+C")
channel.start_consuming()
