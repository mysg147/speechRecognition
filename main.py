import speech_recognition as sr # recognise speech
import playsound # to play an audio file
from gtts import gTTS # google text to speech
import random
from time import ctime # get time details
import webbrowser # open browser
import time
import os # to remove created audio files

class person:
    name = ''
    def setName(self, name):
        self.name = name

class assistant:
    def __init__(self,name):
        self.name=name
    def setName(self,name):
        self.name=name

def there_exists(terms):
    for term in terms:
        if term in voice_data:
            return True

r = sr.Recognizer() # initialise a recogniser
# listen for audio and convert it to text:
askt=False
def record_audio(ask=False):
    with sr.Microphone() as source: # microphone as source
        global askt
        if ask:
            if  ("or you want to give me a nickname" in ask) and (askt==False):
                askt=True
                speak(ask)
            if ("or you want to give me a nickname" not in ask) and (askt==True):
                speak(ask)
        audio = r.listen(source)  # listen for the audio via source
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)  # convert audio to text
        except sr.UnknownValueError: # error: recognizer does not understand
            speak('I did not get that')
        except sr.RequestError:
            speak('Sorry, the service is down') # error: recognizer is not connected
        print(f">> {voice_data.lower()}") # print what user said
        return voice_data.lower()

# get string and make a audio file to be played
def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en') # text to speech(voice)
    r = random.randint(1,20000000)
    audio_file = 'audio' + str(r) + '.mp3'
    tts.save(audio_file) # save as mp3
    playsound.playsound(audio_file) # play the audio file
    print(f"{assistant_obj.name}: {audio_string}") # print what app said
    os.remove(audio_file) # remove audio file

def respond(voice_data):
    
    # Just starting
    if there_exists(['yes','yep','yeah','yeah offcourse','yes offcourse','yes i want']):
        vd=record_audio("so what nickname you want to give me")
        assistant_name = vd.split("is")[-1].strip()    
        speak(f"okay, now my nickname is  {assistant_name}")
        assistant_obj.setName(assistant_name)#remember assistant nickname
        pd=record_audio("and what is your name")
        person_name = pd.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name) # remember name in person object

    if there_exists(['no','naa','nah']):
        pd=record_audio("so what is your name")
        person_name = pd.split("is")[-1].strip()
        speak(f"okay, i will remember that {person_name}")
        person_obj.setName(person_name)

    # 1: greeting
    if there_exists(['hey','hi','hello']):
        greetings = [f"hey, how can I help you {person_obj.name}", f"hey, what's up? {person_obj.name}", f"I'm listening {person_obj.name}", f"how can I help you? {person_obj.name}", f"hello {person_obj.name}"]
        greet = greetings[random.randint(0,len(greetings)-1)]
        speak(greet)

    if there_exists(["how are you","how are you doing","how's you doing"]):
        speak(f"I'm very well, thanks for asking {person_obj.name}")


    # 2: name
    if there_exists(["what is your name","what's your name","tell me your name"]):
        if person_obj.name:
            speak(f"my name is {assistant_obj.name}")
    
    if there_exists(['i want to change your nickname','want to change your name',\
        'want to change your niknamename','i want to change your nickname']):
        vd=record_audio("so what nickname you want to give me")
        assistant_name = vd.split("is")[-1].strip()    
        speak(f"okay, now my nickname is  {assistant_name}")
        assistant_obj.setName(assistant_name)#remember assistant nickname
         
    # 3: time
    if there_exists(["what's the time","tell me the time","what time is it"]):
        time = ctime().split(" ")[3].split(":")[0:2]
        if time[0] == "00":
            hours = '12'
        else:
            hours = time[0]
        minutes = time[1]
        time = f'{hours} {minutes}'
        speak(time)

    # 4: search google
    if there_exists(["search for"]) and 'youtube' not in voice_data:
        search_term = voice_data.split("for")[-1]
        url = f"https://google.com/search?q={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on google')

    # 5: search youtube
    if there_exists(["youtube"]):
        search_term = voice_data.split("for")[-1]
        url = f"https://www.youtube.com/results?search_query={search_term}"
        webbrowser.get().open(url)
        speak(f'Here is what I found for {search_term} on youtube')
    #6: exiting
    if there_exists(['exit']):
        speak("exiting")
        exit()



time.sleep(1)

person_obj = person()
assistant_obj=assistant('anebelle')

while(1):
    voice_data = record_audio(f"hey you can call me  {assistant_obj.name}  or you want to give me a nickname") # get the voice input
    respond(voice_data) # respond
