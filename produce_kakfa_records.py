import random
import time
from time import sleep

from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: x.encode('utf-8'))

alphabet_choice = "ABCDEFG"
activities = ["status", "login", "comment", "like", "interested", "going", "shared", "tagged"]
separator = "|"
user_key_size = 4

while True:
    """
    Keep producing records with a 
    variable delay.
    """

    for _ in range(0, random.randint(0, 20)):
        user = ''.join(random.choice(alphabet_choice) for _ in range(user_key_size))
        epoch_time = str(int(time.time()))
        record = separator.join([epoch_time, user, activities[random.randint(0, 7)]])

        producer.send('activity_test', record)

    sleep(random.randint(0, 2))
