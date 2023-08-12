import pika
from mongoengine import connect
# Підключіть вашу оновлену модель Contact з полем phone_number та способом надсилання
from models import Contact

# Підключення до RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))

channel = connection.channel()

# Створення черг для SMS та Email
channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='email_queue')

# Підключення до MongoDB
connect('svitlana', host='mongodb+srv://svitlana:JHp56XKEKjpAnMqF@atlascluster.9lwm8qe.mongodb.net/')

# Створення фейкових контактів та запис у базу даних
contacts_data = [
    {"full_name": "John Doe", "email": "john@example.com",
        "phone_number": "1234567890", "send_method": "email"},
    {"full_name": "Jane Smith", "email": "jane@example.com",
        "phone_number": "9876543210", "send_method": "sms"},
    # Додайте інші контакти з різними способами надсилання
]

for data in contacts_data:
    contact = Contact(**data)
    contact.save()

    # Відправлення повідомлення до черги відповідно до способу надсилання
    if contact.send_method == "email":
        channel.basic_publish(exchange='',
                              routing_key='email_queue',
                              body=str(contact.id))
    elif contact.send_method == "sms":
        channel.basic_publish(exchange='',
                              routing_key='sms_queue',
                              body=str(contact.id))

print("Sent messages to email_queue and sms_queue")
connection.close()
