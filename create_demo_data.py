import psycopg2
from faker import Faker

connection = psycopg2.connect(
    host='localhost',
    database='assignment_api',
    user='assign_user',
    password='assign_123')

cursor = connection.cursor()
fake = Faker()


for i in range(1, 101):
    name = fake.name()
    dob = fake.date()
    Contact_address = fake.address()
    Contact_emailId = fake.email()
    cursor.execute(
        """INSERT INTO customer ("name","dob") VALUES (%s,%s)""", (name, dob))
    connection.commit()
