from client.Application.Account.AccountWindow import AccountWindow
from client.Application.Manager.RequestHandler import RequestHandler

import customtkinter as ctk


class App:
    def __init__(self):
        self.token = ''

        self.rq = RequestHandler()

        ctk.set_appearance_mode('dark')
        ctk.FontManager.load_font('Myriad Pro Light.ttf')

        self.accountWindow = AccountWindow(fg_color='systemTransparent')
        self.accountWindow.mainloop()

        self.token = self.accountWindow.token
        print(self.token)


if __name__ == '__main__':
    app = App()



"""
structure

define token
present login page
    do login things
    once token recieved close this page

open editor page
"""