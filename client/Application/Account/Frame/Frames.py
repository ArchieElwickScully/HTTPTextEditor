import hashlib
import json
from tkinter import StringVar
import customtkinter as ctk
from itertools import cycle

import requests


class MainFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.textFrame = TextFrame(self, fg_color='transparent')
        self.textFrame.grid(column=0, row=0, sticky=ctk.N)

        self.buttonFrame = ButtonFrame(self, corner_radius=15)
        self.buttonFrame.grid(pady=25, padx=(0, 25),
                              column=1, row=0, sticky=ctk.NSEW)

        self.grid_propagate(False)

        self.framePool = cycle([])


class TextFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.title = ctk.CTkLabel(self, text='Clide',
                                  font=ctk.CTkFont('Myriad Pro Light', 35, 'normal'))
        self.title.pack(pady=(15, 0), side=ctk.TOP)

        self.seperator = ctk.CTkProgressBar(self, height=3, width=280,
                                            progress_color='gray', fg_color='gray')
        self.seperator.pack(side=ctk.TOP, pady=(5, 0))

        self.welcome = ctk.CTkLabel(self, text='Welcome to Clide.', font=('Myriad Pro Light', 25))
        self.welcome.pack(side=ctk.TOP, anchor=ctk.NW,
                          pady=(20, 0), padx=(15, 0))

        self.info = ctk.CTkLabel(self, text='A cloud based IDE with a focus on security, simplicity and transparency',
                                 font=('Myriad Pro Light', 16, 'normal'), wraplength=350, justify='left')
        self.info.pack(side=ctk.LEFT, anchor=ctk.NW,
                       pady=(10, 0), padx=(15, 0))

        self.grid_propagate(False)


class ButtonFrame(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        self.states = cycle(['Login', 'Create'])
        self.switchButtonStates = cycle(['Dont have an account?', 'Already have an account?'])

        self.stateStringVar = StringVar(value=next(self.states))
        self.switchButtonText = StringVar(value=next(self.switchButtonStates))

        self.title = ctk.CTkLabel(self, textvariable=self.stateStringVar,
                                  font=ctk.CTkFont('Myriad Pro Light', 30, 'normal'),
                                  text_color='#DDDDDD')
        self.title.pack(pady=(15, 0), padx=0)

        self.usernameEntry = ctk.CTkEntry(master=self, placeholder_text='Username',
                                          fg_color='transparent',
                                          width=250, height=35, corner_radius=10)
        self.usernameEntry.pack(pady=(100, 0), padx=20)

        self.passwordEntry = ctk.CTkEntry(master=self, placeholder_text='Password', show='*',
                                          fg_color='transparent',
                                          width=250, height=35, corner_radius=10)
        self.passwordEntry.pack(pady=(20, 0), padx=20)

        self.actionButton = ctk.CTkButton(master=self, textvariable=self.stateStringVar,
                                          width=80, command=self.doActionButton)
        self.actionButton.pack(pady=(20, 0))

        self.switchButton = ctk.CTkButton(master=self, textvariable=self.switchButtonText,
                                          font=('Myriad Pro Light', 12),
                                          text_color='gray',
                                          border_width=0, fg_color='transparent',
                                          command=self.swapState)

        self.switchButton.pack(pady=5, side=ctk.BOTTOM)

    def swapState(self):
        self.stateStringVar.set(next(self.states))
        self.switchButtonText.set(next(self.switchButtonStates))

    def doActionButton(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()

        match self.stateStringVar.get():
            case 'Login':
                self.login(username, password)

            case 'Create':
                self.createAccount(username, password)

            case _:
                print('uhoh(something has gone terribly wrong\n(goodluck)')

    def login(self, username, password):
        hashobj = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        sendData = {'command': "SignIn",
                    "args": {'username': username, 'password': password}}

        r = requests.post("http://localhost:8000/", json=sendData)
        response = json.loads(r.text)

        print(f'Response from server: {response['writtenResponse']}\nToken: {response['token']}')

    def createAccount(self, username, password):
        hashobj = hashlib.sha256(str.encode(password))
        password = hashobj.hexdigest()

        sendData = {'command': "CreateAccount",
             "args": {'username': username, 'password': password}}

        r = requests.post("http://localhost:8000/", json = sendData)
        response = json.loads(r.text)

        print(f'Response from server: {response['writtenResponse']}\nToken: {response['token']}')



