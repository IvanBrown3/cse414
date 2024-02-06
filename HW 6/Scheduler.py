from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from model.Appointments import Appointment
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime


'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    patient = Patient(username, salt=salt, hash=hash)

    try:
        patient.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)

def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Failed to create user.")
        return

    username = tokens[1]
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    caregiver = Caregiver(username, salt=salt, hash=hash)

    # save to caregiver information to our database
    try:
        caregiver.save_to_db()
    except pymssql.Error as e:
        print("Failed to create user.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Failed to create user.")
        print(e)
        return
    print("Created user ", username)


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE Username = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['Username'] is not None
    except pymssql.Error as e:
        print("Error occurred when checking username")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when checking username")
        print("Error:", e)
    finally:
        cm.close_connection()
    return False


def login_patient(tokens):
    global current_patient
    if current_patient is not None or current_caregiver is not None:
        print("User already logged in.")
        return

    if len(tokens) != 3:
        print("Login failed.")
        return
    
    username = tokens[1]
    password = tokens[2]
    patient = None

    try:
        patient = Patient(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return
    
    if patient is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("User already logged in.")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Login failed.")
        return

    username = tokens[1]
    password = tokens[2]

    caregiver = None
    try:
        caregiver = Caregiver(username, password=password).get()
    except pymssql.Error as e:
        print("Login failed.")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Login failed.")
        print("Error:", e)
        return

    # check if the login was successful
    if caregiver is None:
        print("Login failed.")
    else:
        print("Logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    global current_patient, current_caregiver
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return

    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    query = """
    SELECT Caregivers.Username, V.Name, V.Doses 
    FROM Caregivers 
    JOIN Availabilities ON Caregivers.Username = Availabilities.Username 
    LEFT JOIN (
        SELECT Appointments.Vaccine, Appointments.Time 
        FROM Appointments
    ) AS A ON Availabilities.Time = A.Time 
    LEFT JOIN Vaccines AS V ON A.Vaccine = V.Name 
    WHERE Availabilities.Time = %s AND A.Time IS NULL 
    ORDER BY Caregivers.Username
    """
    try:
        cursor.execute(query, date)
        for row in cursor:
            print(row['Username'], row['Name'] if row['Name'] is not None else 'None', row['Doses'] if row['Doses'] is not None else 'None')
    except pymssql.Error as e:
        print("Please try again!")
        print("Db-Error:", e)
        quit()



def get_next_appointment_id():
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    get_max_id = "SELECT MAX(ID) as max_id FROM Appointments"
    cursor.execute(get_max_id)
    max_id = 0
    for row in cursor:
        if row['max_id'] is not None:
            max_id = row['max_id']

    return max_id + 1


def reserve(tokens):
    global current_patient
    if current_patient is None:
        print("Please login first!")
        return

    if len(tokens) != 3:
        print("Please try again!")
        return

    date = tokens[1]
    vaccine_name = tokens[2]

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    get_vaccine_doses = "SELECT Doses FROM Vaccines WHERE Name = %s"
    cursor.execute(get_vaccine_doses, vaccine_name)
    available_doses = None
    for row in cursor:
        available_doses = row['Doses']
        break

    if available_doses is None or available_doses <= 0:
        print("Not enough available doses!")
        return

    query = "SELECT Username FROM Availabilities WHERE Time = %s ORDER BY Username"
    cursor.execute(query, date)
    caregiver_username = None
    for row in cursor:
        caregiver_username = row['Username']
        break

    if caregiver_username is None:
        print("No Caregiver is available!")
        return


    appointment_id = get_next_appointment_id() 
    appointment = Appointment(appointment_id, date, vaccine_name, caregiver_username, current_patient.get_username())
    appointment.save_to_db()

    update_vaccine_doses = "UPDATE Vaccines SET Doses = Doses - 1 WHERE Name = %s"
    cursor.execute(update_vaccine_doses, vaccine_name)
    conn.commit()

    print(f"Appointment ID: {appointment_id}, Caregiver username: {caregiver_username}")



def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    date = tokens[1]
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    try:
        d = datetime.datetime(year, month, day)
        current_caregiver.upload_availability(d)
    except pymssql.Error as e:
        print("Upload Availability Failed")
        print("Db-Error:", e)
        quit()
    except ValueError:
        print("Please enter a valid date!")
        return
    except Exception as e:
        print("Error occurred when uploading availability")
        print("Error:", e)
        return
    print("Availability uploaded!")


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = tokens[1]
    doses = int(tokens[2])
    vaccine = None
    try:
        vaccine = Vaccine(vaccine_name, doses).get()
    except pymssql.Error as e:
        print("Error occurred when adding doses")
        print("Db-Error:", e)
        quit()
    except Exception as e:
        print("Error occurred when adding doses")
        print("Error:", e)
        return

    # if the vaccine is not found in the database, add a new (vaccine, doses) entry.
    # else, update the existing entry by adding the new doses
    if vaccine is None:
        vaccine = Vaccine(vaccine_name, doses)
        try:
            vaccine.save_to_db()
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in our table
        try:
            vaccine.increase_available_doses(doses)
        except pymssql.Error as e:
            print("Error occurred when adding doses")
            print("Db-Error:", e)
            quit()
        except Exception as e:
            print("Error occurred when adding doses")
            print("Error:", e)
            return
    print("Doses updated!")


def show_appointments(tokens):
    global current_patient, current_caregiver
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)

    if current_patient is not None:
        query = "SELECT ID, Vaccine, Time, Caregiver FROM Appointments WHERE Patient = %s ORDER BY ID"
        cursor.execute(query, current_patient.get_username())
    else:
        query = "SELECT ID, Vaccine, Time, Patient FROM Appointments WHERE Caregiver = %s ORDER BY ID"
        cursor.execute(query, current_caregiver.get_username())

    for row in cursor:
        print(row['ID'], row['Vaccine'], row['Time'], row['Caregiver'] if current_patient is not None else row['Patient'])


def logout(tokens):
    global current_patient, current_caregiver
    if current_patient is None and current_caregiver is None:
        print("Please login first!")
        return

    current_patient = None
    current_caregiver = None
    print("Successfully logged out!")


def list_commands():
    print(" *** Please enter one of the following commands *** ")
    print("> create_patient <username> <password>")
    print("> create_caregiver <username> <password>")
    print("> login_patient <username> <password>")
    print("> login_caregiver <username> <password>")
    print("> search_caregiver_schedule <date>")
    print("> reserve <date> <vaccine>")
    print("> upload_availability <date>")
    print("> cancel <appointment_id>")
    print("> add_doses <vaccine> <number>")
    print("> show_appointments")
    print("> logout")
    print("> Quit")
    print()

def start():
    stop = False
    print()
    list_commands()
    while not stop:
        response = ""
        print("> ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Please try again!")
            break

        response = response.lower()
        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Please try again!")
            continue
        operation = tokens[0]
        if operation == "create_patient":
            create_patient(tokens)
            list_commands()
        elif operation == "create_caregiver":
            create_caregiver(tokens)
            list_commands()
        elif operation == "login_patient":
            login_patient(tokens)
            list_commands()
        elif operation == "login_caregiver":
            login_caregiver(tokens)
            list_commands()
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
            list_commands()
        elif operation == "reserve":
            reserve(tokens)
            list_commands()
        elif operation == "upload_availability":
            upload_availability(tokens)
            list_commands()
        elif operation == cancel:
            cancel(tokens)
            list_commands()
        elif operation == "add_doses":
            add_doses(tokens)
            list_commands()
        elif operation == "show_appointments":
            show_appointments(tokens)
            list_commands()
        elif operation == "logout":
            logout(tokens)
            list_commands()
        elif operation == "quit":
            print("Bye!")
            stop = True
        else:
            print("Invalid operation name!")



if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
