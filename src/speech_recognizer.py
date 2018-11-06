import speech_recognition as sr
r = sr.Recognizer()
audio = "C:\\Users\\Neeraja\\Documents\\CSC2526Project\inside_out.wav"

with sr.AudioFile(audio) as source:
    audio = r.record(source)

IBM_USERNAME = "f3a73821-92e7-45cc-b315-20ad731a79ca"
IBM_PASSWORD = "PDtoYxoV2Y0b"
try:
    print("The audio file contains: " + r.recognize_ibm(audio, username=IBM_USERNAME, password=IBM_PASSWORD))
except sr.UnknownValueError:
    print("IBM Speech to Text could not understand audio")
except sr.RequestError as e:
    print("Could not request results from IBM Speech to Text service; {0}".format(e))
