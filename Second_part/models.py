from mongoengine import Document, StringField, BooleanField


class Contact(Document):
    full_name = StringField(required=True, max_length=100)
    email = StringField(required=True, max_length=100, unique=True)
    # Можна вказати більш точні обмеження залежно від формату телефонного номера
    phone_number = StringField(max_length=15)
    send_method = StringField(choices=["email", "sms"], required=True)
    email_sent = BooleanField(default=False)

    meta = {'collection': 'contacts'}  # Назва колекції у MongoDB
