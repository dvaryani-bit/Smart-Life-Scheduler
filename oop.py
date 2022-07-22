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




class Vars():
  accountStatusActive = True
  accountStatusInactive = False
  loggedIn = True
  loggedOut = False
  database = 'database.json'
  scopes = ['https://www.googleapis.com/auth/calendar.readonly']
  client_secret_file = 'credentials.json'
  client_secret = {"installed":{"client_id":"767527063195-v8kclhr5to7uj8oiior1om52eskk3o0n.apps.googleusercontent.com","project_id":"lifeassist-352201","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}
  create = 'Create'
  login = 'Login'


'''
class Database():

    @staticmethod
    def get_database(self):
        file = open(Vars.database)
        data = json.load(file)
        self.database = data
        return data
    @staticmethod
    def add_to_database(self, username, name, email, phone, password):
        self.database[username] = {'name': name, 'email': email, 'phone': phone, 'password': password}
        file = open('database.json','w')
        json.dump(self.database, file, indent = 4)

        ## saves the password to the database
'''


class Person():

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
        #self.account.verify_account()

    def login_account(self, username, password):
        database = self.get_database()
        if username in database:
            if password == database[username]['password']:
                #self.__init__(username, password, database[self.username]['name'],database[self.username]['email'], database[self.username]['phone'])
                self.name, self.email, self.phone = database[username]['name'], database[username]['email'], database[username]['phone']
                self.account = Account(username, password, self.name, self.email, self.phone, mode=Vars.login)
            else:
                raise Exception('Username is incorrect')
        else:
            raise Exception('Password is incorrect')






class Account(Person):

    def __init__(self, username=None, password=None, name=None, email=None, phone=None, mode = None):
        Person.__init__(self, name, email, phone)
        if mode == Vars.create:
            database = self.get_database()
            self.username = self.set_username(username, database)
            self.password = self.set_password(password, database)
            self.add_to_database(database)
        elif mode == Vars.login:
            self.username = username
            self.password = password
        #self.accountStatus = Vars.accountStatusInactive
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

    #def __setattr__(self, key, value):
    #    database = self.get_database()
    #    if key == 'username':
    #        if value in database:
    #            raise Exception('Username is already in database, please choose another one')
    #        else:
    #            self.__dict__[key] = value
    #    elif key == 'password':
    #        if len(value) < 6:
    #            raise Exception('Password should be greater than 6 characters')
    #        else:
    #            self.__dict__[key] = value
    #            self.add_to_database(database)
    #            self.logged_in = Vars.loggedIn
    #    else:
    #        self.__dict__[key] = value







    @staticmethod
    def get_database():
        file = open(Vars.database)
        data = json.load(file)
        return data

    def add_to_database(self, database):
        database[self.username] = {'name': self.name, 'email': self.email, 'phone': self.phone, 'password': self.password}
        file = open('database.json', 'w')
        json.dump(database, file)

    def send_verification_token(self):
        self.verify_token = random.randrange(1000, 9999)
        print(self.verify_token)
        ## send the verification token in email

    #def verify_account(self, user_token_input):
    #    if user_token_input == self.verify_token:
    #        self.status = Vars.accountStatusActive
    #        self.logged_in = Vars.loggedIn

    #def reset_password(self):
    #    pass

    def authenticateLogin(self, database):
        if self.username in database:
            if self.password in database[self.username]:
                return True


    def add_user_inputs(self, activity_obj):
        self.activity_objects.append(activity_obj)






class UserInputs(Account):
    def __init__(self, mode, wakeTime=None, sleepTime=None, waterIntake=None, google_calendar_token=None, username=None, password=None):
        self.sleep_time = sleepTime
        self.wake_time = wakeTime
        self.water_intake = waterIntake
        self.google_calendar_token = google_calendar_token
        self.calendar_events = None
        #'{"token": "ya29.A0AVA9y1v36wIBM_NVEn-ujHtVMvvo4B1YAG5tSDJvmDi0FP3qxT_cATRc_Rlx9DwDqXsYBThhjOwgAG_PdKu4EwYWYk9IVhlU5ES6o0H6_Bt5fCnzeny00ZBI3YIbDDv6svjbzXxTzK3dTGKgpE7bHC6MZF5UYUNnWUtBVEFTQVRBU0ZRRTY1ZHI4eWZBX0xfSlJoZTBYX0VKbUJpd2FUZw0163", "refresh_token": "1//0dRCKUpfL5MAWCgYIARAAGA0SNwF-L9IrD5FjCEpj_1bXjEMLJkuIq5GypCf4uYzUFi_8QHlFuVwJMxBFhw5PenSV2l3ZZgz1_aU", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "767527063195-v8kclhr5to7uj8oiior1om52eskk3o0n.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/calendar.readonly"], "expiry": "2022-07-21T05:30:31.794829Z"}'
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
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_config(Vars.client_secret, scopes=Vars.scopes)
                creds = flow.run_local_server(port=0)
            self.google_calendar_token = creds.to_json()
        try:
            service = build('calendar', 'v3', credentials=creds)
            now = datetime.datetime.now()
            now = now.replace(hour=0, minute=0, second=0)
            tomorrow = now + datetime.timedelta(days=1)
            now = now.isoformat() + 'Z' ## things are getting messed up because google only takes UTC
            tomorrow = tomorrow.isoformat() + 'Z'
            #test = now = datetime.datetime.utcnow().isoformat() + 'Z'
            events_result = service.events().list(calendarId='primary', timeMin=now, timeMax=tomorrow,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items')
            events = [{y: x[y] for y in ['summary', 'start', 'end']} for x in events]
            self.calendar_events = events
            for i in events:
                print(i)

            if not events:
                print('No upcoming events found.')
                return

        except HttpError as error:
            print('An error occurred: %s' % error)

    def save_user_inputs(self, person_obj):
        database = Account.get_database()
        print(1)
        database[person_obj.account.username]['wake_time'] = str(self.wake_time.year) +'-'+ str(self.wake_time.month) +'-'+ str(self.wake_time.day)+' '+ str(self.wake_time.hour) +':'+ str(self.wake_time.minute) +''+ str(self.wake_time.second)
        database[person_obj.account.username]['sleep_time'] = str(self.sleep_time.year) +'-'+ str(self.sleep_time.month) +'-'+ str(self.sleep_time.day)+' '+ str(self.sleep_time.hour) +':'+ str(self.sleep_time.minute) +''+ str(self.sleep_time.second)
        database[person_obj.account.username]['google_calendar_token'] = self.google_calendar_token
        file = open('database.json', 'w')
        json.dump(database, file)

    def get_inputs_from_database(self, username, password):
        database = self.get_database()
        self.wake_time, self.sleep_time, self.google_calendar_token = database[username]['wake_time'], database[username]['sleep_time'], database[username]['google_calendar_token']



        #createActivity(activity type = calendar )
    #sleeping time, waking time, calendar log in,




class Activity(Account):
    def __init__(self, activity_type, subactivity_type, start_time, end_time):
        self.activity_type = activity_type
        self.subactivity_type = subactivity_type
        self.notification_type = None ## hard or soft
        self.start_time = start_time
        self.end_time = end_time
        self.createActivity(activity_type, subactivity_type, start_time, end_time)

    def createActivity(self, activity_type, subactivity_type, start_time, end_time):
        ## implement the whole thing in a dictionary to make code shorter
        if activity_type == 'lifestyle': #water, wake time, sleep time...meals
            if subactivity_type == 'wake':
                self.notification_type = 'hard'
            elif subactivity_type == 'sleep':
                self.notification_type = 'soft'
            elif subactivity_type == 'water':
                self.notification_type = 'soft'
        elif activity_type == 'meetings': #just google events
            self.start_time
            self.end_time
            self.notification_type = 'soft'
            #self.duration_type    ## is it a block on the calendar or a quick notification..
        elif activity_type == 'chores': #grocery, bills
            pass





class Calendar(Account):
    def __init__(self, ):
        self.calendar = {}



'''
# Hi, welcome to the app. chose sign up or login
### sign up.. creates object, stores data in db, also logged in...
p_test = Person('rick', 'rick69@gmail.com', '6785356669')
p_test.create_account('username7', 'password123')
### Now that you are signed in, welcome to the home page.
### In the home page, you can input user inputs or see your calendar

wake_time = 8
sleep_time = 23
water_intake = 8

now = datetime.datetime.now()
wake_time = now.replace(hour=wake_time, minute=0, second=0)
sleep_time = now.replace(hour=sleep_time, minute=0, second=0)


inputs = UserInputs(mode=Vars.create, wake_time, sleep_time, water_intake)
inputs.save_user_inputs(p_test)

p_test.account.add_user_inputs( Activity('lifestyle', 'wake', None, inputs.wake_time) )
p_test.account.add_user_inputs( Activity('lifestyle', 'sleep', inputs.sleep_time, None) )
for item in inputs.calendar_events:
    p_test.account.add_user_inputs(Activity('meetings', None, item['start']['dateTime'], item['end']['dateTime']))


print("hi")

'''


### log in
uName = 'username6'
pswrd = 'password123'
# create a login method...
# for login, we will create a method which takes the data from the db and makes the object exactly like how its created in sign up
p_test = Person()
p_test.login_account(uName, pswrd)
inputs = UserInputs(mode=Vars.login, username=p_test.account.username, password=p_test.account.password)
p_test.account.add_user_inputs(Activity('lifestyle', 'wake', None, inputs.wake_time))
p_test.account.add_user_inputs(Activity('lifestyle', 'sleep', inputs.sleep_time, None))
for item in inputs.calendar_events:
    p_test.account.add_user_inputs(Activity('meetings', None, item['start']['dateTime'], item['end']['dateTime']))
print("hi")
#make the method in the Account Class
# also init the Person object... using this example
#Person.__init__(self, name, email, phone)







### once activity objects are made, we need a method to create the calendar

