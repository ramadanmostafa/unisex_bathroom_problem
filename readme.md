***unisex bathroom problem***

this project contains a simple simulating and a solution for the unisex bathroom problem.

***Installation***
you just need to have python 2.7 installed then you can run the scripts

***Used Packages***

-socket: to listen to the client requests

-multi-threading: to run the socket in a thread and the main managing script in another thread.

-sqlite database: to hold the data(i chose sqlite for simplicity only but i prefer MySQL)

***How to run***

First you need to change settings.py file if you want a custom configuration.

Second run the socket server to init the db (socket that always listening for incoming clients,
    it will create a record in the db for each client and disconnect him when done using the bathroom
    restarting the socket will automatically create bathrooms and clear the person table)

cd /path/to/unisex_bath/

python socket_server.py

Third you need to simulate client arrival by running some scripts that connect to the socket and request to use the unisex bathroom.
you will find examples scripts in simple_client.py and simple_client2.py
to test the script, you will need multiple terminals to run simple_client.py or simple_client2.py with the socket server.

***Used algorithm***

THE main algorithm is here, it is so simple

first check the bathroom stalls for any finished client, if found, get him out the bathroom and
disconnect this client.

second get some information about the current status of the bathroom (num_stall_available, sex_using_now)
if num_stall_available is 0, do nothing
else,
get males and females waiting list ordered by arriving time ascending.

if the 2 queues are empty, do nothing

if a male is in the bathroom and the male waiting list is empty, do nothing.

if a female is in the bathroom and the female waiting list is empty, do nothing.

if all bathroom stalls are empty, who came first enters (male or female)

if sex x (male or female) is using the bathroom,
   if the opposite sex waiting list is empty, enter sex x until the available stalls reaches zero or the list is done.
   if there are female(s) or male(s) waiting,
      list of sex x will use the available stalls if they came first
      list of sex x will use the available stalls if the opposite sex waiting time is less than his average using time

***Project settings***

Feel free to change the settings as you want.

you can change number if stalls be change the value of (STALL_COUNT)

you can change average using time for males or females by changing the variables (AVERAGE_FEMALE_USING_TIME, AVERAGE_MALE_USING_TIME)

all time values are in seconds

***Database scheme***

just 2 tables

"bathrooms" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`status`	TEXT NOT NULL DEFAULT 'available',
	`person_id`	INTEGER PRIMARY KEY person.id,
	`last_action_time`	REAL,
	`sex`	TEXT
)

"person" (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`arrive_timestamp`	REAL NOT NULL,
	`status`	TEXT NOT NULL DEFAULT 'waiting',
	`sex`	TEXT NOT NULL DEFAULT 'male',
	`using_time`	REAL NOT NULL,
	`client_address`	INTEGER
)

***Testing***

I was really very busy so i did not write full testing for 
the projects. i just wrote 2 test cases to make sure the make sure there is only one sex in the bathroom after 
sending requests from some females and the other one to make sure there is no available  stalls after some requests.