from client.Application.Manager.RequestHandler import RequestHandler
from client.Application.Account.AccountWindow import AccountWindow

import customtkinter as ctk
import threading
import multiprocessing

class App:
    def __init__(self, requestQueue, outputQueue):
        self.requestQueue = requestQueue
        self.outputQueue = outputQueue

        ctk.set_appearance_mode('dark')
        ctk.FontManager.load_font('Myriad Pro Light.ttf')

        thread = threading.Thread(target=self.outputThread, daemon=True) # im sure theres probably a better way to do
        thread.start()                                                   # this but im tired and running out of time

        self.accountWindow = AccountWindow(self.requestQueue)
        self.accountWindow.mainloop()

        #self.token = self.accountWindow.token
        #print(self.token)

    def outputThread(self):
        while True:
            if not self.outputQueue.empty():
                serverResponse, tokenBool = self.outputQueue.get()
                self.accountWindow.alerts.setText(serverResponse)
                print(serverResponse)

                #if tokenBool:
                    #self.accountWindow.master.destroy()


if __name__ == '__main__':
    rq = multiprocessing.Queue()
    oq = multiprocessing.Queue()

    rh = RequestHandler(rq, oq)
    rh.start()

    app = App(rq, oq)



"""
structure

define token
present login page
    do login things
    once token recieved close this page

open editor page

TODO
====

multithreading
platform independed



multithreading -> well multiprocessing cuz of gil (just incase)

have request handler running in its own process in a loop with a queue in shared memory here
how return data such as server responses?
    -> for loging in etc we can just have it spawn a messagebox mayb idk
    -> when typing shouldnt be too much of an issue i dont think we just need a label that notifies of wether
       file is backed up or not
    -> when loggingin in we will need the token in shared memory anyway - can i close a program from a seprate process?
       ooooo have the request handler running in the main thread and uis in their own process
       we ball
       
multiprocessing!
start file and launch login ui as own process
then we start the request handler loop 

im so stupid i fully wrote this then started to do it the wrong way
fun challenge then ig lmao
tbf it kinda makes more sense to have the ui etc in the main thread and the rh in the background kinda thing

"""