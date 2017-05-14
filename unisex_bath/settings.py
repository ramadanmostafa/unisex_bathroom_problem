"""
this file contains some useful constants values required for database, the socket server and bathrooms
"""
import os

# check if resources_testing_mode key is found in os.environ which means that
# this is the testing mode so we need to work on a copy of the db
if "unisex_testing_mode" in os.environ:
    DATABASE_NAME = "unisex_testing.sqlite"
else:
    DATABASE_NAME = "unisex.sqlite"

# the host name of the socket server
HOST = ''

# the port number of the socket server
PORT = 8888

# receiving buffer limits
RECV_BUFFER = 1024

# number of seconds required to wait
TIMEOUT = 10

# Number of available bathrooms
STALL_COUNT = 3

# Average time a male takes to use the bathroom in seconds
AVERAGE_MALE_USING_TIME = 30

# Average time a female takes to use the bathroom in seconds
AVERAGE_FEMALE_USING_TIME = 60

# waiting time after check in seconds
WAIT_TIME = 1
