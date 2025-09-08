import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import webbrowser
import pyttsx3
import threading
import musiclibrary
import subprocess
import os
from datetime import datetime
# import wolframalpha


recognizer = sr.Recognizer()
engine = pyttsx3.init()

# === TTS Function ===
def speak(text):
    engine.say(text)
    engine.runAndWait()

# === Command Processing ===
def processCommand(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif "open chat gpt" in command:
      webbrowser.open("https://www.chatgpt.com") 
    elif "open kimi" in command:
      webbrowser.open("https://www.kimi.com") 

    elif "open instagram" in command:
      webbrowser.open("https://instagram.com")
    elif "open calculator" in command:
        subprocess.Popen("calc.exe")
    elif "open notepad" in command:
        subprocess.Popen("notepad.exe")

    elif "open excel" in command:
        subprocess.Popen(r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE")
    elif "time" in command:
        now = datetime.now().strftime("%I:%M %p")

        speak(f"The time is {now}")

    elif "hello" in command:
       speak("Hello sir,how can i assist you..")

    elif "your name" in command or "who are you" in command:
        speak("I'm Jarvis ,Your virtual assistant..")

    elif "your father" in command or "your creator" in command:
        speak("Mr.Kapil Kumar ji..")

    elif "how r u" in command or "how are you" in command:
      h = datetime.now().hour
      if 5 <= h < 12:
        speak("Good morning! I'm doing great, thanks for asking.")
      elif 12 <= h < 17:
        speak("Good afternoon! All systems running fine.")
      else:
        speak("Good evening! Ready to help.")

    elif command.startswith("play "):
       song = command[5:].strip()           # remove "play " and any leading/trailing spaces
       if song in musiclibrary.music:
        link = musiclibrary.music[song]
        webbrowser.open(link)
       else:
         print("Song not found.")

    # elif command.startswith("tell me ") or command.startswith("wolfram "):
    # # keep everything after the trigger phrase
    #   if command.startswith("tell me "):
    #     question = command[8:]          # length of "tell me "
    #   else:
    #     question = command[7:]           # length of "wolfram "
    #   question = question.strip()

    #   if not question:
    #     speak("Sure, what would you like to ask Wolfram?")
    #     return
    #   answer = ask_wolfram(question)
    #   speak(answer or "No answer found.")
      
    elif "sleep" in command:
        speak("Shutting down")
        app.quit()

    elif "shutdown pc" in command:
     speak("Shutting down the PC")
     
     os.system("shutdown /s /t 5")  
    else:
        speak(f"You said: {command}")

# === Listen for Actual Command (after wake word) ===
def listen_for_command():
    with sr.Microphone() as source:
        status_label.config(text="Jarvis Active. Listening...")
        audio = recognizer.listen(source,timeout=4,phrase_time_limit=3)
        try:
            command = recognizer.recognize_google(audio, language=language_var.get())
            command_display.delete(0, tk.END)
            command_display.insert(0, command)
            should_exit = processCommand(command)
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        status_label.config(text="Idle")
        start_wake_word_thread()

# === Wake Word Detection ===
def detect_wake_word():
    with sr.Microphone() as source:
        status_label.config(text="Listening for 'Jarvis'...")
        try:
            audio = recognizer.listen(source, timeout=3, phrase_time_limit=2)
            word = recognizer.recognize_google(audio, language=language_var.get())
            if "jarvis" in word.lower():
                speak("Ya.")
                listen_for_command()
            else:
                start_wake_word_thread()  # Keep listening
        except:
            start_wake_word_thread()  # Restart wake word listener


# APP_ID = os.getenv("WOLFRAM_APP_ID", "6JQ4VAGEK9")
# wa_client = wolframalpha.Client("6JQ4VAGEK9")

# def ask_wolfram(query: str) -> str:
#     """Return a short, plain-text answer or None if nothing found."""
#     try:
#         res = wa_client.query(query)
#         # Pick the first pod that has a plaintext answer
#         for pod in res.pods:
#             if pod.text:
#                 return pod.text.strip()
#         return "No answer found"
#     except Exception as e:
#         return f"Error contacting Wolfram|Alpha: {e}"


def start_wake_word_thread():
    threading.Thread(target=detect_wake_word, daemon=True).start()

# === GUI Setup ===
app = tk.Tk()
app.title("Jarvis Voice Assistant")

tk.Label(app, text="Recognized Command:").pack()
command_display = tk.Entry(app, width=50)
command_display.pack(pady=5)
#app.iconbitmap(r"D:\Downloads\ChatGPT Image ")

status_label = tk.Label(app, text="Idle", fg="green")
status_label.pack()
#app["bg"]="dark orange"
language_var = tk.StringVar(value='en-IN')  # default: English (India)
tk.Label(app, text="Language:").pack()
tk.OptionMenu(app, language_var, 'en-IN', 'hi-IN').pack()

tk.Button(app, text="Exit", command=app.quit).pack(pady=10)

# === Start wake word detection thread ===
start_wake_word_thread()
app.mainloop()
