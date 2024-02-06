import sys
sys.path.append("../util/*")
sys.path.append("../db/*")
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql

class Appointment:
    def __init__(self, id, time, vaccine, caregiver, patient):
        self.id = id
        self.time = time
        self.vaccine = vaccine
        self.caregiver = caregiver
        self.patient = patient

    # getters
    def get_id(self):
        return self.id

    def get_time(self):
        return self.time

    def get_vaccine(self):
        return self.vaccine

    def get_caregiver(self):
        return self.caregiver

    def get_patient(self):
        return self.patient

    def save_to_db(self):
        cm = ConnectionManager()
        conn = cm.create_connection()
        cursor = conn.cursor()

        add_appointment = "INSERT INTO Appointments VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor.execute(add_appointment, (self.id, self.time, self.vaccine, self.caregiver, self.patient))
            
            conn.commit()
        except pymssql.Error:
            raise
        finally:
            cm.close_connection()
