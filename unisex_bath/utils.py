"""
some useful functions
"""
import time
from database_operations import BathroomDBConnection, PersonDBConnection


def person_done():
    """
    check the status of all the available stalls and empty them if the person is done
    :return: 
    """
    bathroom_db = BathroomDBConnection()
    person_db = PersonDBConnection()
    for stall in bathroom_db.get_all_bathrooms():
        if stall[1] == "busy":
            person_id = stall[2]
            person = person_db.get_person_by_id(person_id)
            if time.time() >= int(person[4]) + int(stall[3]):
                # this person is done using the bathroom, get him out
                person_db.update_status(person_id, "done")
                bathroom_db.leave_bathroom(stall[0])


def stall_available():
    """
    :return: number of stalls available
    """
    bath_db = BathroomDBConnection()
    return len(bath_db.get_available_bathrooms())


def get_bathroom(person_id, person_sex):
    """
    let the client use the available bathroom
    :return:
    """
    bathroom_db = BathroomDBConnection()
    bathroom_id = bathroom_db.reserve_bathroom(sex=person_sex, person_id=person_id)
    if bathroom_id is None:
        print "all bathrooms are busy now, please wait"
        return False
    else:
        print "a bathroom has been reserved for you (%d)" % person_id
        # use this bathroom
        if bathroom_db.use_bathroom(sex=person_sex, person_id=person_id):
            # update user status to using
            person = PersonDBConnection()
            person.update_status(person_id=person_id, new_status="using")
            print "you are using the bathroom now(%d)" % person_id
            return True
        return False


def get_waiting_list(sex):
    """
    get the a list of persons for a particular sex, ordered by time of arrival (ascending).
    :param sex:
    :return:
    """
    person_db = PersonDBConnection()
    return person_db.list_persons(sex)

def get_bathroom_sex():
    """
    :return the sex using the bathroom now.
    :return: female, male or None
    """
    bath_db = BathroomDBConnection()
    return bath_db.get_sex_bathroom_now()