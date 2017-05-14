"""
class to interact with the database
"""
from settings import DATABASE_NAME, STALL_COUNT
import sqlite3
import time

class MyDatabase:
    """
    parent class of the database classes, contains the shared methods
    """

    def _connect(self):
        """
        connect to the sqlite database and return the connection

        :rtype: sqlite db connection
        """
        try:
            con = sqlite3.connect(DATABASE_NAME)
            return con
        except:
            raise RuntimeError("An Exception happened with the Database, make sure you are connected")


class PersonDBConnection(MyDatabase):
    """
    used to interact with the Person Table.
    """
    def insert_person(self, arriv_time, sex, status, using_time, client_address):
        """
        insert a record into person table
        :param arriv_time: the time when this person arrived
        :param sex: male or female
        :param status: waiting, using or done
        :param using_time: how many seconds this person will spend in th bathroom
        :return:
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "insert into person (arrive_timestamp, sex, status, using_time, client_address)" \
                    " values(?, ?, ?, ?, ?)"
        cur.execute(sql_query, (arriv_time, sex, status, using_time, client_address))
        person_id = cur.lastrowid
        conn.commit()
        conn.close()
        return person_id

    def list_persons(self, sex):
        """
        get a list of persons ordered by arrival time
        :param sex:
        :return:
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "select * from person WHERE sex = ? and status = 'waiting' ORDER BY arrive_timestamp"
        cur.execute(sql_query, (sex,))
        data = cur.fetchall()
        conn.close()
        return data

    def update_status(self, person_id, new_status):
        """
        will update the status of the user that inserted previously.
        :param person_id: id of the person
        :param new_status: waiting, using or done
        :return:
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "update person set status=? WHERE id = ?"
        cur.execute(sql_query, (new_status, person_id))
        conn.commit()
        conn.close()

    def get_person_by_id(self, person_id):
        """
        get a person record from the table person by his id
        :param person_id: 
        :return: person record
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "select * from person WHERE id = ?"
        cur.execute(sql_query, (person_id, ))
        data = cur.fetchone()
        conn.close()
        return data

    def get_person_by_client_address(self, client_address):
        """
        get a person record from the table person by his client_address
        :param person_id:
        :return: person record
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "select * from person WHERE client_address = ?"
        cur.execute(sql_query, (client_address, ))
        data = cur.fetchone()
        conn.close()
        return data


class BathroomDBConnection(MyDatabase):
    """
    used to interact with the Bathroom Table.
    """
    def get_all_bathrooms(self):
        """
        get all bathrooms (available or not)
        :return:
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "select * from bathrooms"
        cur.execute(sql_query)
        data = cur.fetchall()
        conn.close()
        return data

    def get_available_bathrooms(self):
        """
        get all available bathrooms
        :return:
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "select * from bathrooms WHERE status = 'available' and person_id is NULL"
        cur.execute(sql_query)
        data = cur.fetchall()
        conn.close()
        return data

    def create_bathroom(self):
        """
        create an empty bathroom
        :return:
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query1 = "delete from bathrooms where 1"
        sql_query2 = "delete from person where 1"
        sql_query3 = "insert into bathrooms (person_id) values(null)"
        cur.execute(sql_query1)
        conn.commit()
        cur.execute(sql_query2)
        conn.commit()
        for _ in range(STALL_COUNT):
            cur.execute(sql_query3)
        conn.commit()
        conn.close()

    def reserve_bathroom(self, sex, person_id):
        """
        change the status of the bathroom to reserved if available for this sex
        :param sex: male or female
        :param person_id: the id of the person wants to get this bathroom
        :return: bathroom id
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query1 = "select id from bathrooms WHERE " \
                    "bathrooms.status = 'available' and (bathrooms.sex is NULL or bathrooms.sex = ?)"

        sql_query2 = "update bathrooms set status = ?, person_id = ?, last_action_time = ?, sex = ? " \
                     "WHERE id = ?"
        cur.execute(sql_query1, (sex,))
        data = cur.fetchall()
        if len(data) > 0:
            bathroom_id = data[0][0]
            cur.execute(sql_query2, ("reserved", person_id, time.time(), sex, bathroom_id))
            conn.commit()
            conn.close()
            return bathroom_id
        else:
            conn.close()
            return None

    def use_bathroom(self, sex, person_id):
        """
        check if the user reserved the bathroom
        if true, change the bathroom status to busy
        update all the bathrooms sex to this use sex
        :param sex: male or female
        :param person_id: the id of the person wants to get this bathroom
        :return: bathroom id
        """
        # check if the user reserved the bathroom
        sql_query1 = "select id from bathrooms WHERE status = 'reserved' and person_id = ? and sex = ?"
        # if true, change the bathroom status to busy
        sql_query2 = "update bathrooms set status = 'busy', last_action_time = ? WHERE id = ?"
        # update all the bathrooms sex to this use sex
        sql_query3 = "update bathrooms set sex = ? WHERE sex is NULL"

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql_query1, (person_id, sex))
        data = cur.fetchall()
        if len(data) != 1:
            conn.close()
            return False
        else:
            bathroom_id = data[0][0]
            cur.execute(sql_query2, (time.time(), bathroom_id))
            conn.commit()
            cur.execute(sql_query3, (sex, ))
            conn.commit()
            conn.close()
            return True

    def leave_bathroom(self, bathroom_id):
        """
        simulate client leaving the bathroom,
        set the status of the bathroom to available
        :param bathroom_id:
        :return:
        """
        sql_query1 = "update bathrooms set sex = NULL, person_id = NULL, status = 'available' WHERE id = ?"
        sql_query2 = "update bathrooms set sex = NULL, person_id = NULL, status = 'available' WHERE " \
                     "person_id is NULL"

        conn = self._connect()
        cur = conn.cursor()
        cur.execute(sql_query1, (bathroom_id, ))
        conn.commit()
        cur.execute(sql_query2)
        conn.commit()
        conn.close()
        return True

    def get_sex_bathroom_now(self):
        """
        :return the sex using the bathroom now.
        :return: female, male or None
        """
        conn = self._connect()
        cur = conn.cursor()
        sql_query = "select sex from bathrooms WHERE status != 'available' "
        cur.execute(sql_query)
        data = cur.fetchall()
        conn.close()
        return None if len(data) == 0 else data[0][0]