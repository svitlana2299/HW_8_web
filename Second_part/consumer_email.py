import pika
from mongoengine import connect
# Підключіть вашу оновлену модель Contact з полем phone_number та способом надсилання
from models import Contact

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

# Створення черги для Email
channel.queue_declare(queue='email_queue')

# Підключення до MongoDB
connect('svitlana', host='mongodb+srv://svitlana:JHp56XKEKjpAnMqF@atlascluster.9lwm8qe.mongodb.net/')


def send_email_stub(contact_id):
    # Тут можна імітувати надсилання email
    print(f"Sending email to contact with ID: {contact_id}")
    return True


def callback(ch, method, properties, body):
    contact_id = body.decode('utf-8')
    contact = Contact.objects(id=contact_id).first()

    if contact:
        if not contact.email_sent:
            if send_email_stub(contact_id):
                contact.email_sent = True
                contact.save()
                print(
                    f"Email sent and updated for contact with ID: {contact_id}")
        else:
            print(f"Email already sent for contact with ID: {contact_id}")
    else:
        print(f"Contact with ID {contact_id} not found")


# Обробка повідомлень з черги для Email
channel.basic_consume(queue='email_queue',
                      on_message_callback=callback, auto_ack=True)

print("Email Consumer is waiting for messages. To exit press CTRL+C")
channel.start_consuming()
