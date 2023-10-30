# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import sqlite3



class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []

class ActionCheckAvailability(Action):

    def name(self) -> Text:
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Let me check, please wait for a moment ...")

        conn = sqlite3.connect('../sqlite/restaurant-20231024.db') 
        cursor = conn.cursor()

        sql = "SELECT * FROM reservations WHERE reserved_under = ?"
        res = cursor.execute(sql, (tracker.get_slot('name'),))

        #print(res.fetchall())

        booking_available = False
        if len(res.fetchall()) == 0:
            booking_available = True
            print("User has not booked yet")

        # Close connection
        conn.close()

        return [SlotSet("booking_available", booking_available)]
    
class ActionBookAppointment(Action):

    def name(self) -> Text:
        return "action_book_appointment"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = sqlite3.connect('../sqlite/restaurant-20231024.db') 
        cursor = conn.cursor()

        sql="INSERT INTO reservations (date, time_start, time_end, table_id, reserved_under, nr_guests) VALUES (?, ?, ?, ?, ?, ?);"
        #cursor.execute(sql,(tracker.get_slot('email'), tracker.get_slot('enrollment')))
        cursor.execute(sql,("bla", "bla", "bla", "1", tracker.get_slot('name'), tracker.get_slot('number_guests')))

        # Commit your changes in the database and close connection
        conn.commit()
        conn.close()

        return []