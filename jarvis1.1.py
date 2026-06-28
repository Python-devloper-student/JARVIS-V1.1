from faster_whisper import WhisperModel
import silero_vad
import sounddevice as sd
import numpy as np
import winsound
import subprocess
import json
import pyttsx3
import requests
import serial
class Jarvis:
   def __init__(self):
        self.speaker=pyttsx3.init()
        self.arduino=serial.Serial("com3",9600)
        self.commands={'notepad':'start Notepad.exe','browser':'start chrome.exe','terminal':'start cmd.exe','youtube':'start chrome.exe https://youtube.com',
                       'call agent':'start chrome.exe https://chatgpt.com','github':'start chrome.exe https://github.com/Python-devloper-student','manager':'explorer'
                       ,'code':'code','linux':'wsl','shut down':'shutdown /s /t 20','stop shut down':'shutdown /a'}
        self.model=WhisperModel('base','cpu',compute_type='float32')
        self.vad=silero_vad.load_silero_vad()
        self.Chat=True
        self.url='http://localhost:11434/api/chat'
        self.header={'Content-Type':'application/json'}
        self.message={'model':'jarvis','messages':[],'stream':True}
   def serial_communication(self,task):
          
          self.arduino.write((task+'<').encode())
          self.arduino.write((task+'<').encode())
   def speak(self,text):
       self.speaker.say(text)
       self.speaker.runAndWait()
   def command_execution(self,command):
       subprocess.run(command,text=True,shell=True)
   def listener(self):
       self.serial_communication('listening')
       spoke=False
       audio_file=[]
       while True:
            audio=sd.rec(48000,16000,1)
            sd.wait()
            speech=silero_vad.get_speech_timestamps(audio.flatten(),self.vad)
            if speech:
                spoke=True
                audio_file.extend(audio.flatten())
                print('speech detected')
            else:
                if spoke==True:
                 self.serial_communication('ide')
                 return np.array(audio_file,dtype='float32')
   def transcriber(self):
       audio=self.listener()
       text=[]
       data,info=self.model.transcribe(audio,language='en')
       for i in data:
           text.append(i.text)
       text=(''.join(text)).lower()
       return text
   def assistant(self):
       send=True
       text=self.transcriber()
       if 'exit' in text:
           self.serial_communication('speak')
           self.speak('jarvis deactivated')
           self.serial_communication('ide')
           self.Chat=False
           
       if self.Chat:
        for command in self.commands:
            if command in text:
               send=False
               try:
                self.serial_communication('thinking')
                self.command_execution(self.commands[command])
                self.serial_communication('ide')
               except Exception as e:
                  self.serial_communication('speak')
                  self.speak(e)
                  self.serial_communication('ide')
        if send:
          try:
            self.serial_communication('thinking')
            print('you: ',text,'\nAI: ')
            message={'role':'user','content':text}
            self.message['messages'].append(message)
            response=requests.post(self.url,headers=self.header,json=self.message,stream=True)
            ai_response=[]
            ai_response2=[]
            for lines in response.iter_lines():
                line=json.loads(lines)
                response=line['message']['content']
                print(response,end='',flush=True)
                ai_response.append(response)
                ai_response2.append(response)
                if '.' in response or '?' in response or '!' in response:
                    read=''.join(ai_response2)
                    self.serial_communication('speak')
                    self.speak(read)
                    ai_response2.clear()
            ai_message={'role':'assistant','content':''.join(ai_response)}
            self.message['messages'].append(ai_message)
            self.serial_communication('ide')
          except Exception as e:
             self.serial_communication('speak')
             self.speak(e)
             self.serial_communication('ide')
   def main(self):
     winsound.PlaySound('c:/users/deepk/PROGRAMMING/python codes/killer.wav',winsound.SND_FILENAME)
     self.serial_communication('speak')
     self.speak('jarvis initiated ')
     self.serial_communication('ide')
     while True:
       text=self.transcriber()
       print(text)
       if 'kill' in text:break
       if 'jarvis' in text or 'activate' in text:
           winsound.PlaySound('c:/users/deepk/PROGRAMMING/python codes/killer.wav',winsound.SND_FILENAME)
           self.serial_communication('speak')
           self.speak('jarvis activated')
           self.serial_communication('ide')
           self.Chat=True
           while self.Chat:
               self.assistant()
     self.serial_communication('speak')
     self.speak('why did you do that i  was loyal to you')
     self.serial_communication('xxxxxxxxx')
ov=Jarvis()
ov.main()