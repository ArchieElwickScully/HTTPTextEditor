import customtkinter as ctk

from client.Application.Account.AccountWindow import AccountWindow


def main():
    token = ''

    ctk.set_appearance_mode('dark')
    ctk.FontManager.load_font('Myriad Pro Light.ttf')

    accountWindow = AccountWindow(fg_color='systemTransparent')
    accountWindow.mainloop()


if __name__ == '__main__':
    main()



"""
structure

define token
present login page
    do login things
    once token recieved close this page

open editor page
"""