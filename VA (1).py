from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials  
import os 
import time
import pyttsx3
import speech_recognition as sr
import pytz
import subprocess

SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
MONTHS = ["january","february","march","april","may","june","july","august","september","october","november","december"]
DAYS = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
DAY_EXTENSIONS = ["rd","th","st","nd"]

def speak(text):
    engine = pyttsx3.init()

    # Get available voices
    voices = engine.getProperty('voices')
    
    # Choose female voice (usually indexed at 1; index 0 is male)
    engine.setProperty('voice', voices[1].id)
    
    # Set speaking rate (optional)
    engine.setProperty('rate', 150)  # Adjust the rate to your preference
    
    # Set volume (optional)
    engine.setProperty('volume', 1)  # Set volume level between 0 and 1

    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        said = " "

        try:
            said = r.recognize_google(audio)    # Use Google API to recognize what was said
            print(said)
        except Exception as e:
            print("Exception: " + str(e))
    
    return said.lower()

text = get_audio()

if "hello" in text:
    speak("hello how are you?")

if "me your name" in text:
    speak("Hello Manan how are you,My name is Shridha")

# Google Calendar API

def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)  # Corrected here
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    return service


def get_events(day,service):
    if day is None:  # **Handle case when date is None**
        print("Invalid date input.")
        speak("Sorry, I could not understand the date.")
        return  # **Exit the function if the date is not valid*
    # Call the Calendar API
    
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId="primary", timeMin=date.isoformat(), timeMax=end_date.isoformat(),
            singleEvents=True, orderBy="startTime").execute()
    
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
    else:
        speak(f"You have {len(events)} events on this day.")
    # Prints the start and name of the next 10 events
        for event in events:
          start = event["start"].get("dateTime", event["start"].get("date"))
          print(start, event["summary"])
          start_time = str(start.split("T")[1].split("-")[0])
          if int (start_time.split(":")[0]) < 12:
            start_time = start_time + " AM" 
          else:
            start_time = str(int (start_time.split(":")[0]) - 12) + start_time.split(":")[1] #added this in the end kr skta hai delete after plus...its just giving saade wala thing
            start_time = start_time + " PM"

          speak(event["summary"] + " at "+ start_time)


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today
    
    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word) 
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext) 
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
                    
    if month < today.month and month != -1:
        year = year+1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7
        
        return today + datetime.timedelta(dif)
    
    if month == -1 or day == -1:
        return None
    
    return datetime.date(year=year, month=month, day=day)
    
# text = get_audio().lower()
# print(get_date(text))

# speak("hello manan how are you")

def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":","-") + "-note.txt"
    with open (file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])  

WAKE = "hello"
SERVICE = authenticate_google()
print("Start")

while True:
    print("Listening")
    text = get_audio()

    if text.count(WAKE) > 0:
      speak("Heyyyy Manannnnnn") #can also write i am ready
      text = get_audio()
      CALENDER_STRS = ["what do i have","do i have plans","am i busy"]
  

      for phrase in CALENDER_STRS:
          if any(word in text.lower() for word in phrase.split()):
              date = get_date(text)
              if date:
                get_events(date, SERVICE)
              else:
                  speak("I don't understand")
              break

      NOTE_STRS = ["make a note","write this down","remember this","write down"]
      for phrase in NOTE_STRS:
          if phrase in text:
            speak("What would you like me to note?")
            note_text = get_audio()
            note(note_text)
            speak("Cool,I have made a note of that")