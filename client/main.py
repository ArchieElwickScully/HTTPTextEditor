from client.Application.Manager.RequestHandler import RequestHandler
from client.Application.Account.AccountWindow import AccountWindow
from multiprocessing import Queue


import customtkinter as ctk
import threading

class App:
    def __init__(self, requestQueue: Queue, outputQueue: Queue):
        self.requestQueue: Queue = requestQueue
        self.outputQueue: Queue = outputQueue

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
    rq = Queue()        # initialising request and output queue in order to pass data to the request handler running in
    oq = Queue()        # a separate process, this is because these queues will be stored in shared memory and therefore
                        # accessible from the request handler running in that seprate process

    rh = RequestHandler(rq, oq)     # instantiating the request handler with the queues in shared memory as arguments
    rh.start()                      # starting the request handler in seprate process

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



todo now

end to end encryption
    okay
    
    serverside
        when we create token we also create encryption key and store it in token with also public key
        we send pub key over w token
    clientside
        we do same but send pub key w login request, this is then also stored in token class serverside
        also return an encrypted token
"""
