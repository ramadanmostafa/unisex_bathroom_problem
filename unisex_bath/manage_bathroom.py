"""
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
"""
from utils import person_done, stall_available, get_waiting_list, get_bathroom_sex, get_bathroom
from settings import AVERAGE_FEMALE_USING_TIME, AVERAGE_MALE_USING_TIME, WAIT_TIME
import time


def manage_bathroom_main_loop():
    """
    THE main algorithm is here
    :return:
    """
    while 1:
        # check users in the bathrooms if anyone finished
        # then get them out and disconnect the client
        person_done()

        num_stall_available = stall_available()
        sex_using_now = get_bathroom_sex()  # female, male or None
        print "num_stall_available", num_stall_available
        print "sex_using_now", sex_using_now
        if num_stall_available > 0:
            females_queue = get_waiting_list('female')
            males_queue = get_waiting_list('male')
            enter_sex = None
            if len(females_queue) == 0 and len(males_queue) == 0:
                time.sleep(WAIT_TIME)
                print "no waiting list"
                continue
            if sex_using_now == "male" and len(males_queue) == 0:
                time.sleep(WAIT_TIME)
                print "male list is empty (nothing to do)"
                continue
            if sex_using_now == "female" and len(females_queue) == 0:
                time.sleep(WAIT_TIME)
                print "female list is empty (nothing to do)"
                continue
            if sex_using_now is None:
                # all stalls are empty
                if len(females_queue) == 0:
                    # females queue is empty then enter the males
                    enter_sex = "male"
                    operation_list = males_queue
                elif len(males_queue) == 0:
                    # males queue is empty then enter the females
                    enter_sex = "female"
                    operation_list = females_queue
                elif females_queue[0][1] < males_queue[0][1]:
                    # female came first
                    enter_sex = "female"
                    operation_list = females_queue
                else:
                    # male came first
                    enter_sex = "male"
                    operation_list = males_queue
            elif sex_using_now == "male":
                # one or more males is using the bathroom
                if len(females_queue) == 0:
                    # females waiting list it empty
                    enter_sex = "male"
                    operation_list = males_queue
                elif females_queue[0][1] < males_queue[0][1]:
                    # female came first, male using bathroom now, males still can enter if
                    # the female waiting time is less than her avg using time
                    # enter list of males (len = num_stall_available)
                    # if female waiting time < female avg waiting, else continue
                    if int(females_queue[0][1]) + AVERAGE_FEMALE_USING_TIME > time.time():
                        counter = 0
                        for person_male in males_queue:
                            if counter < num_stall_available:
                                counter += 1
                                get_bathroom(person_male[0], "male")
                            else:
                                break
                    continue
                else:
                    # wait
                    # enter list of males that come first then
                    # enter list of males (len = num_stall_available - len(list of males entered))
                    # if female waiting time < female avg waiting, else continue
                    counter = 0
                    for person_male in males_queue:
                        if counter < num_stall_available:
                            if person_male[1] < females_queue[0][1]:
                                get_bathroom(person_male[0], "male")
                                counter += 1
                            elif int(females_queue[0][1]) + AVERAGE_FEMALE_USING_TIME > time.time():
                                get_bathroom(person_male[0], "male")
                                counter += 1
                        else:
                            break
                    continue

            elif sex_using_now == "female":
                if len(males_queue) == 0:
                    enter_sex = "female"
                    operation_list = females_queue
                elif females_queue[0][1] < males_queue[0][1]:
                    # wait
                    # enter list of females that come first then
                    # enter list of females (len = num_stall_available - len(list of females entered))
                    # if male waiting time < male avg waiting, else continue
                    #
                    counter = 0
                    for person_female in females_queue:
                        if counter < num_stall_available:
                            if person_female[1] < males_queue[0][1]:
                                get_bathroom(person_female[0], "female")
                                counter += 1
                            elif int(males_queue[0][1]) + AVERAGE_MALE_USING_TIME > time.time():
                                get_bathroom(person_female[0], "female")
                                counter += 1
                        else:
                            break
                    continue
                else:
                    # wait
                    # enter list of females (len = num_stall_available)
                    # if male waiting time < male avg waiting, else continue
                    #
                    if int(males_queue[0][1]) + AVERAGE_MALE_USING_TIME > time.time():
                        counter = 0
                        for person_female in females_queue:
                            if counter < num_stall_available:
                                counter += 1
                                get_bathroom(person_female[0], "female")
                            else:
                                break
                    continue

            # execute the predefined actions
            if enter_sex is not None:
                if num_stall_available <= len(operation_list):
                    limit = num_stall_available
                else:
                    limit = len(operation_list)
                for i in range(limit):
                    get_bathroom(operation_list[i][0], enter_sex)
        print "running"
        time.sleep(WAIT_TIME)
