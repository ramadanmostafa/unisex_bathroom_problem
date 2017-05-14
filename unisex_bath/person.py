"""
this file contains the implementation of the Person class which is responsible for
persons records
"""
import time
import random
from settings import AVERAGE_FEMALE_USING_TIME, AVERAGE_MALE_USING_TIME
from database_operations import PersonDBConnection, BathroomDBConnection


class Person(object):
    """
    responsible for managing clients that hits the socket server.
    """

    def __init__(self, sex, client_address):
        """
        constructor of the person class
        :param sex: should be male or female only.
        """
        self.sex = sex
        self.arrival_time = time.time()
        self.status = "waiting"
        self.using_time = 2 * random.random() * (AVERAGE_FEMALE_USING_TIME \
            if sex == "female" else AVERAGE_MALE_USING_TIME)
        self.bathroom = None
        self.client_address = client_address

    def save(self):
        """
        save the person info to the database in the person table
        :return:
        """
        person_db = PersonDBConnection()
        person_id = person_db.insert_person(
            arriv_time=self.arrival_time,
            sex=self.sex,
            status=self.status,
            using_time=self.using_time,
            client_address=self.client_address
        )
        return person_id


