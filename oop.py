

# factory for making calendars,
# the final product is the calendar
# the final product will be objects of people's calendar...
# create a factory for the process



# the app will make a daily calendar, based on wake up time, activities and works and then sleeping time
# works we are getting from google
#User inputs: - wake time, sleep time
#                - google claendar auth log in object


# activities:- lifestyle activites: water, meals, workout (these are calendar objects)
#            - work activities (we take the google calendar and make it into objects
#            - chores (we make them into objects)
# there are two types of reminders: block reminders: work, study, workout; small task reminders like drink water: drink water, eat meal

# result: calendar as a dictionary:
# date: {waking time: .lifestyle activity.....     sleeping time







import os
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import json
import random




class Vars():
  accountStatusActive = True
  accountStatusInactive = False
  loggedIn = True
  loggedOut = False
  database = 'database.json'
  Vars.scopes = ['https://www.googleapis.com/auth/calendar.readonly']




class Person():

    def __init__(self, name, email, phone):
        self.__name = name
        self.__email = email
        self.phone = phone
        self.account = None

    def create_account(self, username, password):
        self.account = Account(username, password)
        self.account.verify_account()



class PasswordsDatabase():
    def __init__(self):
        self.database = None

    def get_database(self):
        file = open(Vars.database)
        data = json.load(file)
        self.database = data
        return data


class Account(Person):
    def __init__(self, username, password):
        self.username = username ## apply getter and setter to make sure account is not duplicated
        self.password = password  ## apply getter and setter to satisfy requirement
        self.accountStatus = Vars.accountStatusInactive
        self.logged_in = Vars.loggedOut

    def send_verification_token(self):
        self.verify_token = random.randrange(1000, 9999)
        print(self.verify_token)
        ## send the verification token in email

    def verify_account(self, user_token_input):
        if user_token_input == self.verify_token:
            self.status = Vars.accountStatusActive
            self.logged_in = Vars.loggedIn

    def reset_password(self):
        pass

    def authenticateLogin(self, username_input, password_input):
        if username_input in PasswordsDatabase.get_database():
            if password_input in PasswordsDatabase.database[username_input]:
                self.logged_in = Vars.loggedIn


p_test = Person('rick', 'rick69@gmail.com', '6785356669')
p_test.create_account('username1', 'password123')
test = UserInputs(1, 2)



class UserInputs:
    def __init__(self, sleepTime, wakeTime):
        self.sleepTime = sleepTime
        self.wakeTime = wakeTime
        self.get_calendar_data()
        self.google_calendar_token = None

    def updateDetails(self):
        pass

    def userInputs(self):
        pass



    def get_calendar_data(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', Vars.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', Vars.scopes)
                creds = flow.run_local_server(port=0)
            self.google_calendar_token = creds.to_json()
            #with open('token.json', 'w') as token:
            #    token.write(creds.to_json())
        try:
            # modify to get events for that specific day
            service = build('calendar', 'v3', credentials=creds)
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            print('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId='primary', timeMin=now,
                                                  maxResults=10, singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items')
            for i in events:
                print(i)

            if not events:
                print('No upcoming events found.')
                return

        except HttpError as error:
            print('An error occurred: %s' % error)

    #sleeping time, waking time, calendar log in,







class Activity():
    def __init__(self, activity_type, subactivity_type, start_time, end_time):
        self.activity_type = activity_type
        self.subactivity_type = subactivity_type
        self.notification_type = None ## hard or soft
        self.start_time = None
        self.end_time = None
        self.createActivity(activity_type, subactivity_type, start_time, end_time)

    def createActivity(self, activity_type, subactivity_type, start_time, end_time):
        ## implement the whole thing in a dictionary to make code shorter
        if activity_type == 'lifestyle': #water, wake time, sleep time...meals
            if subactivity_type == 'wake':
                self.notification_type = 'hard'
            elif subactivity_type == 'sleep':
                pass
            elif subactivity_type == 'water':
                pass
        elif activity_type == 'meetings': #just google events
            self.start_time
            self.end_time
            self.notification_type = 'soft'
            self.duration_type    ## is it a block on the calendar or a quick notification..
        elif activity_type == 'chores': #grocery, bills
            pass






class Calendar():
    def __init__(self, ):
        pass




class Notifications():
    def __init__(self, optimizedCalendar):
        self.optimizedCalendar = optimizedCalendar




