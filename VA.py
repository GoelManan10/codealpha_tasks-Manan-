# from __future__ import print_function
# import datetime
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# import os 
# import time
# import playsound
# import speech_recognition as sr
# from gtts import gTTS

# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

# def speak(text):
#     tts = gTTS(text=text, lang="en")
#     filename = "voice.mp3"
#     tts.save(filename)
#     playsound.playsound(filename)

# def get_audio():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         audio = r.listen(source)
#         said = " "

#         try:
#             said = r.recognize_google(audio)    #use google api to recognize what we said 
#             print(said)
#         except Exception as e:
#             print("Exception: " + str(e))
    
#     return said

# # text = get_audio()

# # if "hello" in text:
# #     speak("hello how are you?")

# # if "what is your name" in text:
# #     speak("My name is Mackie")


# #                                   Google calender api
# #                                     ===============

# # import datetime
# # import os.path

# # from google.auth.transport.requests import Request
# # from google.oauth2.credentials import Credentials
# # from google_auth_oauthlib.flow import InstalledAppFlow
# # from googleapiclient.discovery import build
# # from googleapiclient.errors import HttpError


# def main():
#   """Shows basic usage of the Google Calendar API.
#   Prints the start and name of the next 10 events on the user's calendar.
#   """
#   creds = None
  
#   if os.path.exists("token.json"):
#     with open('token.json','rb') as token:
#        creds = credentials.from_authorized_user_file("token.json",SCOPES)
  
#   if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#       creds.refresh(Request())
#     else:
#       flow = InstalledAppFlow.from_client_secrets_file(
#           "credentials.json", SCOPES
#       )
#       creds = flow.run_local_server(port=0)
    
#     with open("token.json", "w") as token:
#       token.write(creds.to_json())

#     service = build("calendar", "v3", credentials=creds)

#     # Call the Calendar API
#     now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
#     print("Getting the upcoming 10 events")
#     events_result = service.events().list(calendarId="primary",timeMin=now,
#             maxResults=10,singleEvents=True,orderBy="startTime",).execute()
    
#     events = events_result.get("items", [])

#     if not events:
#       print("No upcoming events found.")

#     # Prints the start and name of the next 10 events
#     for event in events:
#       start = event["start"].get("dateTime", event["start"].get("date"))
#       print(start, event["summary"])


# if __name__ == "__main__":
#   main()