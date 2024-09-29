import speech_recognition as sr
import os
import webbrowser
import ollama
import datetime
import pyttsx3  # For text-to-speech
import json
import random
import subprocess  # For running external scripts

ollama.api_key = None  

chatStr = ""
reminders = {}

engine = pyttsx3.init()

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"User: {query}\ncc: "
    
    prompt = chatStr
    try:
        full_response = ""
        for response in ollama.generate(
            model='llama3', 
            prompt=prompt, 
            stream=True
        ):
            full_response += response['response']
        
        say(full_response)
        chatStr += f"{full_response}\n"
        return full_response
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I'm sorry, there was an error."

def ai(prompt):
    try:
        full_response = ""
        for response in ollama.generate(
            model='llama3',
            prompt=prompt,
            stream=True
        ):
            full_response += response['response']
        
        text = f"Ollama response for Prompt: {prompt} \n *************************\n\n{full_response}"
        
        if not os.path.exists("Ollama"):
            os.mkdir("Ollama")

        filename = f"Ollama/{''.join(prompt.split('intelligence')[1:]).strip()}.txt"
        with open(filename, "w") as f:
            f.write(text)
    except Exception as e:
        print(f"An error occurred: {e}")

def say(text):
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            print(f"An error occurred: {e}")
            return "Some Error Occurred. Sorry from cc"

def save_reminders():
    with open("reminders.json", "w") as f:
        json.dump(reminders, f)

def load_reminders():
    global reminders
    if os.path.exists("reminders.json"):
        with open("reminders.json", "r") as f:
            reminders = json.load(f)

def set_reminder(date, event):
    if date in reminders:
        reminders[date].append(event)
    else:
        reminders[date] = [event]
    save_reminders()
    say(f"Reminder set for {date} for {event}")

def check_reminders(date):
    if date in reminders:
        events = reminders[date]
        say(f"You have the following events on {date}: {', '.join(events)}")
    else:
        say(f"You have no events on {date}")

def play_trivia():
    trivia_questions = [
        {"question": "What is the capital of France?", "answer": "Paris"},
        {"question": "Who wrote 'To Kill a Mockingbird'?", "answer": "Harper Lee"},
        {"question": "What is the largest planet in our solar system?", "answer": "Jupiter"}
    ]
    question = random.choice(trivia_questions)
    say(question["question"])
    user_answer = takeCommand().lower()
    if question["answer"].lower() in user_answer:
        say("Correct!")
    else:
        say(f"Incorrect. The correct answer is {question['answer']}.")

def play_rock_paper_scissors():
    choices = ["rock", "paper", "scissors"]
    say("Rock, Paper, or Scissors?")
    user_choice = takeCommand().lower()
    if user_choice not in choices:
        say("Invalid choice, please choose rock, paper, or scissors.")
        return
    computer_choice = random.choice(choices)
    say(f"I chose {computer_choice}")
    
    if user_choice == computer_choice:
        say("It's a tie!")
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        say("You win!")
    else:
        say("I win!")

def wait_for_wake_word():
    r = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            print("Waiting for wake word...")
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language="en-in").lower()
                if "cc" in query:
                    say("Yes, how can I help you?")
                    return
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == '__main__':
    load_reminders()
    print('Welcome to cc')
    say("Welcome to cc")
    
    while True:
        wait_for_wake_word()
        while True:
            print("Listening...")
            query = takeCommand()
            sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
            
            for site in sites:
                if f"Open {site[0]}".lower() in query.lower():
                    say(f"Opening {site[0]}...")
                    webbrowser.open(site[1])
            
            if "open music" in query.lower():
                musicPath = "C:/Users/harry/Downloads/downfall-21371.mp3"  
                os.system(f"start {musicPath}")

            elif "the time" in query.lower():
                now = datetime.datetime.now()
                say(f"The time is {now.strftime('%H:%M')}")

            elif "the date" in query.lower():
                today = datetime.date.today()
                say(f"Today's date is {today.strftime('%B %d, %Y')}")

            elif "set a reminder" in query.lower():
                say("What is the date for the reminder?")
                date = takeCommand()
                say("What is the event?")
                event = takeCommand()
                set_reminder(date, event)

            elif "check reminders" in query.lower():
                say("For which date would you like to check the reminders?")
                date = takeCommand()
                check_reminders(date)

            elif "open Spotify" in query.lower():
                os.system("start /System/Applications/FaceTime.app")  

            elif "open pass" in query.lower():
                os.system("start /Applications/Passky.app")  

            elif "using artificial intelligence" in query.lower():
                ai(prompt=query)

            elif "cc quit" in query.lower():
                exit()

            elif "reset chat" in query.lower():
                chatStr = ""

            elif "play trivia" in query.lower():
                play_trivia()
            
            elif "rock paper scissors" in query.lower():
                play_rock_paper_scissors()

            elif "take attendance" in query.lower():
                say("Taking attendance...")
                subprocess.run(["python", "attendance.py"])

            elif "summarise it" in query.lower():
                say("summarizing...")
                subprocess.run(["python", "summarizer.py"])

            else:
                print("Chatting...")
                chat(query)
            
            break  
