'''
Simple socket server using threads
there will be a thread for the socket that always listening for incoming clients,
it will create a record in the db for each client and disconnect him when done using the bathroom
restarting the socket will automatically create bathrooms and clear the person table

and another thread will always hit the db to manage entering bathroom process
(will be repeated every settings.WAIT_TIME seconds)
'''
import socket
import sys
from thread import *
from settings import *
from database_operations import BathroomDBConnection, PersonDBConnection
from person import Person
from threading import Thread
from manage_bathroom import manage_bathroom_main_loop


def start_socket():
    """
    socket that always listening for incoming clients,
    it will create a record in the db for each client and disconnect him when done using the bathroom
    restarting the socket will automatically create bathrooms and clear the person table
    :return:
    """
    # initiate socket server s
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print 'Socket created'

    # Bind socket to local host and port
    try:
        my_socket.bind((HOST, PORT))
    except socket.error as msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    print 'Socket bind complete'

    # Start listening on socket
    my_socket.listen(10)
    print 'Socket now listening'

    # Create Number of available bathrooms
    bathroom = BathroomDBConnection()
    bathroom.create_bathroom()
    print "%d bathrooms created" % STALL_COUNT

    # Function for handling connections. This will be used to create threads
    def clientthread(conn, client_address):
        # infinite loop so that function do not terminate and thread do not end.
        while True:
            # Receiving from client
            try:
                data = conn.recv(RECV_BUFFER)  # male or female
            except:
                print "Exception happened in receiving data, maybe connection terminated"
                break
            else:

                # check if the message Received follows the correct format
                if data == "female" or data == "male":

                    # person sex has to be male or female
                    person_sex = data
                    arrived_person = Person(sex=person_sex, client_address=client_address)
                    person_id = arrived_person.save()
                    print "person created, id=%d" % person_id
                    reply = "you are added to the queue"

                else:
                    tmp_person_db = PersonDBConnection()
                    tmp_person = tmp_person_db.get_person_by_client_address(client_address)
                    if tmp_person is not None and tmp_person[2] == "done":
                        conn.sendall("done")
                        break
                    elif data == "am i done?":
                        reply = "You're not done yet, please wait."
                    else:
                        # the message Received does not follow the correct format so send an error message
                        reply = "wrong message, you must send male or female as the only word"

                # send the message to the client
                conn.sendall(reply)

        # came out of loop and close the connection
        conn.close()

    # now keep talking with the client
    while 1:
        # wait to accept a connection - blocking call
        conn, addr = my_socket.accept()
        client_address = addr[0]
        print 'Connected with ' + client_address + ':' + str(addr[1])

        # start new thread takes 1st argument as a function name to be run,
        #  second is the tuple of arguments to the function.
        start_new_thread(clientthread, (conn, client_address + ':' + str(addr[1])))

    # close the socket server
    my_socket.close()


def threaded_function():
    """
    will always hit the db to manage entering bathroom process
    (will be repeated every settings.WAIT_TIME seconds)
    :return:
    """
    manage_bathroom_main_loop()


thread1 = Thread(target=threaded_function)
thread2 = Thread(target=start_socket)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print "thread finished...exiting"

