import nltk
import numpy as np
import random
import string # to process standard python strings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pyttsx3
import datetime
from dateutil.parser import parse
import json

speaker = pyttsx3.init()

raw="Hi there how are you?"
raw=raw.lower()# converts to lowercase
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
def addReminder(time,content):
    speaker.say("Reminder registered.")
    speaker.runAndWait()
    with open("reminders.txt", "a") as myfile:
        myfile.write(time+"="+content+"\n")

def removeReminders(linesRemove):
    lineNumber=0
    lines=[]
    with open("reminders.txt", "r") as f:
        lines += f.readlines()
    with open("reminders.txt","w") as file:
        for line in lines:
            if lineNumber not in linesRemove:
                file.write(line)
            lineNumber+=1


def checkForReminders():
    f=open("reminders.txt", "r")
    contents = f.read().split("\n")
    output = {}
    temp=1
    lineNumbers=0
    linesToDelete=[]
    for line in contents:
        if '=' in line:
            tempDic={}
            if parse(line.split('=')[0])<=datetime.datetime.now():
                tempDic['date']=line.split('=')[0]
                tempDic['reminder']=line.split('=')[1]
                output['data'+str(temp)]=tempDic
                linesToDelete+=[lineNumbers]
            temp+=1
        lineNumbers+=1
    removeReminders(linesToDelete)
    return output

def response(user_response,bot):
    robo_response=''
    sent_tokens.append(user_response)
    robo_response=bot.get_response(user_response)
    return robo_response

def bot(user_response,bot):
    flows=json.loads(open('flows.json').read())
    if('thanks' in user_response or 'thank' in user_response ):
        print("ROBO: Much Obliged..")
        speaker.say("Much Obliged..")
        speaker.runAndWait()
    else:
        if(greeting(user_response)!=None):
            print("ROBO: "+greeting(user_response))
            speaker.say(greeting(user_response))
            speaker.runAndWait()
        elif any(i in flows['reminders'] for i in user_response.split()):
            for rem in user_response.split():
                if rem in flows['medic']:
                    temp=rem
                    time=""
                    for inp in user_response.split():
                        if inp in flows["time"]:
                            time = user_response[user_response.find(inp):]
                        elif inp in flows["timeMini"]:
                            time = user_response[user_response.find(inp)-3:]
                    now = datetime.datetime.now()
                    if any(i in ["minutes","min"] for i in time.split()):
                        now += datetime.timedelta(minutes=int(time[0:3]))
                    if any(i in ["hours","hrs"] for i in time.split()):
                        now += datetime.timedelta(hours=int(time[0:3]))
                    if any(i in ["seconds","sec"] for i in time.split()):
                        now += datetime.timedelta(seconds=int(time[0:3]))
                    if any(i in ["tomorrow"] for i in time.split()):
                        now += datetime.timedelta(hours=24)
                    addReminder(str(now),"Time to take "+temp)
                elif rem in flows['misc']:
                    temp=user_response[user_response.find('to'):]
                    time=""
                    for inp in user_response.split():
                        if inp in flows["time"]:
                            time = user_response[user_response.find(inp):]
                            temp = temp[:temp.find(inp)]
                        elif inp in flows["timeMini"]:
                            temp1=""
                            for i in temp[:temp.find(inp)-3].split():
                                if i not in flows['fillers']:
                                    temp1+=" "+i
                            temp=temp1.lstrip()
                            time = user_response[user_response.find(inp)-3:]
                    now = datetime.datetime.now()
                    if any(i in ["minutes","min"] for i in time.split()):
                        now += datetime.timedelta(minutes=int(time[0:3]))
                    if any(i in ["hours","hrs"] for i in time.split()):
                        now += datetime.timedelta(hours=int(time[0:3]))
                    if any(i in ["seconds","sec"] for i in time.split()):
                        now += datetime.timedelta(seconds=int(time[0:3]))
                    if any(i in ["tomorrow"] for i in time.split()):
                        now += datetime.timedelta(hours=24)
                    addReminder(str(now),"Time "+temp)
        else:
            print("ROBO: ",end="")
            botRes=response(user_response,bot)
            print(botRes)
            speaker.say(botRes)
            speaker.runAndWait()
            sent_tokens.remove(user_response)
