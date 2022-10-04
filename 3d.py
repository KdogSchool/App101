from __future__ import print_function
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import *
from gcsa.google_calendar import GoogleCalendar
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import os.path
import datetime
from googleapiclient.discovery import build
import sqlite3

def login():
    # getting form data
    uname = username.get()
    pwd = password.get()
    # applying empty validation
    if uname == '' or pwd == '':
        message.set("fill the empty field!!!")
    else:
        # open database
        conn = sqlite3.connect('student.db')
        # select query
        cursor = conn.execute('SELECT * from ADMIN where USERNAME="%s" and PASSWORD="%s"' % (uname, pwd))
        # fetch data
        if cursor.fetchone():
            message.set("Login Success")
            app.__call__()
        else:
            message.set("Wrong username or password")


def Loginform():
    global login_screen
    login_screen = Tk()
    # Setting title of screen
    login_screen.title("Login")
    # setting height and width of screen
    login_screen.geometry("350x250")
    login_screen["bg"] = "#1C2833"
    # declaring variable
    global message;
    global username
    global password
    username = StringVar()
    password = StringVar()
    message = StringVar()

    # Username Label
    Label(login_screen, text="Username * ", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).place(x=20, y=40)
    # Username textbox
    Entry(login_screen, textvariable=username, bg="#1C2833", fg="white", font=("Arial", 12, "bold")).place(x=120, y=42)
    # Password Label
    Label(login_screen, text="Password * ", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).place(x=20, y=80)
    # Password textbox
    Entry(login_screen, textvariable=password, show="*", bg="#1C2833", fg="white", font=("Arial", 12, "bold")).place(
        x=120, y=82)
    # Label for displaying login status[success/failed]
    Label(login_screen, text="", textvariable=message, bg="#1C2833", fg="white", font=("Arial", 12, "bold")).place(x=95,
                                                                                                                   y=120)
    # Login button
    Button(login_screen, text="Login", width=10, height=1, command=login, bg="#00008b", fg="white",
           font=("Arial", 12, "bold")).place(x=125, y=170)
    login_screen.mainloop()

def app():
    # google calendar code
    def clicked():
        calendar = GoogleCalendar('1039522km@gmail.com')
        for event in calendar:
            print(event)
    SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
    def main():
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        def service():
            build('calendar', 'v3', credentials=creds)


        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')

        events_result = service.events().list(calendarId='primary', timeMin=now,
                                              maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')


        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


    def click():
        from beautiful_date import Apr, Mar, Nov, Jan, Jun, Oct, Dec, May, Sept, Feb
        from gcsa.event import Event
        from gcsa.google_calendar import GoogleCalendar
        calendar = GoogleCalendar('1039522km@gmail.com')
        summary = 'Test 1'
        start = (27 / Dec / 2021)[8:00]
        end = (27 / Dec / 2021)[12:00]
        event = Event(summary=summary, start=start, end=end, calendarId='bujsek bob')
        calendar.add_event(event)
    # credit goes to : https://google-calendar-simple-api.readthedocs.io/en/latest/events.html#create-event
    # will not show events that are passed the current date

    # create the window for the GUI and add a title
    window = ThemedTk(theme="equilux")
    window.config(themebg="equilux")
    window.title("3D Printer Scheduler")
    window.geometry('300x320')

#labels and commands for buttons and other entry types

    nameLabel = ttk.Label(window, text="Name: Student ")

    snumberLabel = ttk.Label(window, text="S-number: s1039522")

    labelTop = ttk.Label(window, text="Enter Month")

    comboexample = ttk.Combobox(window,
                                values=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Aug", "Sept", "Oct", "Nov", "Dec"],
                                state="readonly")
    comboexample.current(0)

    labeldate = ttk.Label(window, text='Enter Date')

    combodate = ttk.Combobox(window,
                             values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                                     18, 19, 20, 21, 22, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31], state="readonly")


    combodate.current(0)
    submitButton = ttk.Button(window, text="Submit", command=click, )
    viewButton = ttk.Button(window, text="View Calendar", command=clicked)


    # add labels and text entry/buttons to GUI
    nameLabel.pack()
    snumberLabel.pack()
    labeldate.pack()
    combodate.pack()
    labelTop.pack()
    comboexample.pack()
    submitButton.pack(side=LEFT)
    viewButton.pack(side=RIGHT)
    window.mainloop()


Loginform()