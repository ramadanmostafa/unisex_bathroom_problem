"""
this file contains some test cases that connects to the soket server as a client
and also check the database.
"""
import socket
import time
import os
from shutil import copyfile
from database_operations import BathroomDBConnection
from threading import Thread

# py.test -q test.py
# put the resources_testing_mode key in os.environ which means that
# this is the testing mode so we need to work on a copy of the db

# ip address of the server
HOST = '127.0.0.1'

# port number that the soket server is listening to
PORT = 8888

def setup():
    """
    make a copy of the database
    """
    copyfile('unisex.sqlite', 'unisex_testing.sqlite')
    # initiate the soket client
    soket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soket_client.connect((HOST, PORT))
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(1)
    soket_client.sendall('female')
    time.sleep(2)

def test_bathroom_using_sex():
    """
    make sure there is only one sex in the bathroom
    :return:
    """
    bathroom_db = BathroomDBConnection()
    for bathroom in bathroom_db.get_all_bathrooms():
        assert bathroom[-1] == "female"

def test_no_available_bathrooms():
    """
    make sure there is no available  bathroom
    :return:
    """
    bathroom_db = BathroomDBConnection()
    for bathroom in bathroom_db.get_all_bathrooms():
        assert bathroom[1] == "busy"







