import pyttsx3

engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("volume", 1)


def speak(text):
    engine.say(text)
    engine.runAndWait()
