### Due to sensitivity, cannot share the Google Calendar API token and credentials


import os
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import random
import pytz
import copy
import maskpass

class Vars:
    accountStatusActive = True
    accountStatusInactive = False
    loggedIn = True
    loggedOut = False
    database = 'database.json'
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    client_secret_file = '' ### add your credentials file path here
    client_secret = {} ### add your client secret here
    create = 'Create'
    login = 'Login'


class Person:

    def __init__(self, name=None, email=None, phone=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.account = None

    @staticmethod
    def get_database():
        file = open(Vars.database)
        data = json.load(file)
        return data

    def create_account(self, username, password):
        self.account = Account(username, password, self.name, self.email, self.phone, mode=Vars.create)

    def login_account(self, username, password):
        database = self.get_database()
        x = True
        if username in database:
            if password == database[username]['password']:
                 # self.__init__(username, password, database[self.username]['name'],database[self.username]['email'], database[self.username]['phone'])
                self.name, self.email, self.phone = database[username]['name'], database[username]['email'], \
                                                        database[username]['phone']
                self.account = Account(username, password, self.name, self.email, self.phone, mode=Vars.login)
            else:
                raise Exception('Password is incorrect')
        else:
            raise Exception('Username is incorrect')


class Account(Person):

    def __init__(self, username=None, password=None, name=None, email=None, phone=None, mode=None):
        Person.__init__(self, name, email, phone)
        if mode == Vars.create:
            database = self.get_database()
            self.username = self.set_username(username, database)
            self.password = self.set_password(password, database)
            self.add_to_database(database)
        elif mode == Vars.login:
            self.username = username
            self.password = password
        self.logged_in = Vars.loggedIn
        self.activity_objects = []

    def set_username(self, username, database):
        if username in database:
            raise Exception('Username is already in database, please choose another one')
        else:
            return username

    def set_password(self, password, database):
        if len(password) < 6:
            raise Exception('Password should be greater than 6 characters')
        else:
            return password

    @staticmethod
    def get_database():
        file = open(Vars.database)
        data = json.load(file)
        return data

    def add_to_database(self, database):
        database[self.username] = {'name': self.name, 'email': self.email, 'phone': self.phone,
                                   'password': self.password}
        file = open('database.json', 'w')
        json.dump(database, file)

    def send_verification_token(self):
        self.verify_token = random.randrange(1000, 9999)
        print(self.verify_token)

    def authenticateLogin(self, database):
        if self.username in database:
            if self.password in database[self.username]:
                return True

    def add_user_inputs(self, activity_obj):
        self.activity_objects.append(activity_obj)

class UserInputs(Account):

    def __init__(self, mode, wakeTime=None, sleepTime=None, waterIntake=None, google_calendar_token=None, username=None,
                 password=None):
        self.sleep_time = sleepTime
        self.wake_time = wakeTime
        self.water_intake = waterIntake
        self.google_calendar_token = google_calendar_token
        self.calendar_events = None
        if mode == Vars.login:
            self.get_inputs_from_database(username, password)
        self.get_calendar_data()

    def updateDetails(self):
        pass

    def get_calendar_data(self):
        creds = None
        if self.google_calendar_token:
            creds = Credentials.from_authorized_user_info(json.loads(self.google_calendar_token), Vars.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    flow = InstalledAppFlow.from_client_config(Vars.client_secret, scopes=Vars.scopes)
                    creds = flow.run_local_server(port=0)
            else:
                flow = InstalledAppFlow.from_client_config(Vars.client_secret, scopes=Vars.scopes)
                creds = flow.run_local_server(port=0)
            self.google_calendar_token = creds.to_json()
        try:
            service = build('calendar', 'v3', credentials=creds)
            now = datetime.datetime.now()
            now = now.replace(hour=0, minute=0, second=0)
            tomorrow = now + datetime.timedelta(days=1)
            now = now.isoformat() + 'Z'  ## things are getting messed up because google only takes UTC
            tomorrow = tomorrow.isoformat() + 'Z'
            events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items')
            events = [{y: x[y] for y in ['summary', 'start', 'end']} for x in events]
            self.calendar_events = events
            if not events:
                print('No upcoming events found.')
                return
        except HttpError as error:
            print('An error occurred: %s' % error)

    def save_user_inputs(self, person_obj):
        database = Account.get_database()
        database[person_obj.account.username]['wake_time'] = self.wake_time.strftime("%Y-%m-%d %H:%M")
        database[person_obj.account.username]['sleep_time'] = self.sleep_time.strftime("%Y-%m-%d %H:%M")
        database[person_obj.account.username]['google_calendar_token'] = self.google_calendar_token
        file = open('database.json', 'w')
        json.dump(database, file)

    def get_inputs_from_database(self, username, password):
        database = self.get_database()
        self.wake_time = datetime.datetime.strptime(database[username]['wake_time'], '%Y-%m-%d %H:%M')
        self.sleep_time = datetime.datetime.strptime(database[username]['sleep_time'], '%Y-%m-%d %H:%M')
        now = datetime.datetime.now()
        self.wake_time = self.wake_time.replace(year=now.year, month=now.month, day=now.day)
        self.sleep_time = self.sleep_time.replace(year=now.year, month=now.month, day=now.day)
        self.google_calendar_token = database[username]['google_calendar_token']


class Activity():

    def __init__(self, activity_type, subactivity_type, start_time, end_time):
        self.activity_type = activity_type
        self.subactivity_type = subactivity_type
        self.notification_type = None  ## hard or soft
        self.start_time = start_time
        self.end_time = end_time
        self.createActivity(activity_type, subactivity_type, start_time, end_time)

    def createActivity(self, activity_type, subactivity_type, start_time, end_time):
        if activity_type == 'lifestyle':  # water, wake time, sleep time...meals
            if subactivity_type == 'wake':
                self.start_time = start_time + datetime.timedelta(days=-1)
                self.end_time = end_time
                self.notification_type = 'hard'
            elif subactivity_type == 'sleep':
                self.start_time = start_time
                self.end_time = end_time + datetime.timedelta(days=1)
                self.notification_type = 'soft'
            elif subactivity_type == 'water':
                self.notification_type = 'soft'
        elif activity_type == 'meetings':  # just google events
            self.start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S%z')
            self.end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S%z')
            self.start_time = self.start_time.replace(tzinfo=None)
            self.end_time = self.end_time.replace(tzinfo=None)
            self.notification_type = 'soft'
        elif activity_type == 'chores':  # grocery, bills
            pass


class Calendar():
    def __init__(self, ):
        self.calendar = []

    def create_calendar_template(self, wake_time, sleep_time):
        self.calendar[(wake_time, wake_time + datetime.timedelta(minutes=15))] = {}
        i = copy.deepcopy(wake_time)
        while i <= sleep_time:
            self.calendar[(i, i + datetime.timedelta(minutes=15))] = {}
            i += datetime.timedelta(minutes=15)

    def create_calendar(self, activity_objects):
        print(activity_objects)
        for activity in activity_objects:
            self.calendar.append([(activity.start_time, activity.end_time),  activity.activity_type, activity.subactivity_type, activity.notification_type])
        self.calendar.sort(key = lambda x: x[0][0])


if __name__ == "__main__":
    print('Hi, welcome to the app. chose sign up or login')
    opt1 = input("a:Sign    b:Log in")
    if opt1 == 'a':
        name = input('Enter your name')
        email = input('Enter your email')
        phone = input('Enter your phone')
        p_test = Person(name, email, phone)
        username = input('Enter your username')
        password = input('Enter your password')
        #password = maskpass.askpass()
        p_test.create_account(username, password)
        wake_time = int(input('Enter your wake time in integer. Eg: 8'))
        sleep_time = int(input('Enter your sleep time in integer. Eg: 23'))
        water_intake = int(input('How many glasses of water do you drink? Eg: 23'))
        now = datetime.datetime.now()
        wake_time = now.replace(hour=wake_time, minute=0, second=0)
        sleep_time = now.replace(hour=sleep_time, minute=0, second=0)
        inputs = UserInputs(Vars.create, wake_time, sleep_time, water_intake)
        inputs.save_user_inputs(p_test)

    else:
        x = True
        while x == True:
            try:
                username = input('Enter your username')
                password = input('Enter your password')
                #password = maskpass.askpass("")
                p_test = Person()
                p_test.login_account(username, password)
                x = False
            except:
                pass
        inputs = UserInputs(mode=Vars.login, username=p_test.account.username, password=p_test.account.password)

    p_test.account.add_user_inputs(Activity('lifestyle', 'wake', inputs.sleep_time, inputs.wake_time))
    p_test.account.add_user_inputs(Activity('lifestyle', 'sleep', inputs.sleep_time, inputs.wake_time))
    for item in inputs.calendar_events:
        p_test.account.add_user_inputs(
            Activity('meetings', item['summary'], item['start']['dateTime'], item['end']['dateTime']))

    cal = Calendar()
    cal.create_calendar(p_test.account.activity_objects)
    print(cal.calendar)


