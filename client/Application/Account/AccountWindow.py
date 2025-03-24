from client.Application.Account.Frame import Frames

import customtkinter as ctk
import math


class AccountWindow(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # vars
        self.lastClick = (0, 0)
        self.HEIGHT = 400
        self.WIDTH = 650
        self.token = ''

        # window attributes etc
        self.geometry('650x400')
        self.overrideredirect(True)
        self.wm_attributes("-transparent", True)

        self.centre()

        # setting up binds for window dragging
        self.bind('<Button-1>', self.registerClick)
        self.bind('<B1-Motion>', self.drag)

        # window stuff
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.mainFrame = Frames.MainFrame(self, width=650, height=400, corner_radius=15)
        self.mainFrame.grid(row=0, column=0)

    # window methods
    def drag(self, e):
        diff = (e.x_root - self.lastClick[0],
                e.y_root - self.lastClick[1])

        # print(diff)
        self.geometry(f'+{diff[0]}+{diff[1]}')

    def registerClick(self, e):
        self.lastClick = (e.x_root - self.winfo_rootx(),
                          e.y_root - self.winfo_rooty())
        # print(self.lastClick)
        # print(self.lastClick[0], e.x_root, self.winfo_pointerx(), self.winfo_rootx())

    def centre(self):
        x = math.trunc((self.winfo_screenwidth() / 2) - (self.WIDTH / 2))
        y = math.trunc((self.winfo_screenheight() / 2) - (self.HEIGHT / 2))

        self.geometry(f'+{x}+{y}')

    # talk about issues with just drag in the docs
    # talk about using event.x not event.root_x
    # nvm should use winfo rootx and rooty
    # to get the real last click relative to main window we do e.xroot - winfo_rootx
    """
    because origionally we were doing e.x which returns the location relative to start of widget
    this is all good aslong as the widget touches the left of the window
    if it dosent however we get the wrong coordinats

    instead of this we can use:

    winfo_rootx() - this gets the distance from the leftmost of the window to the left of the screen
    e.x_root - this returns the position of the pointer from the leftmost of the windo
    winfo_pointerx() - same as e.x_root will have to test to see which is faster later

    now we have the distance from the left of the window to the left of screen
    and the distance from the cursor to the left of the screen.

    to move the window from the cursor itself and not have the left of the screen jump to the cursor we must find
    the distance of the cursor from the left of the window, for this we do:
    take awak dist from sreen to win to get win to cursor

    then take away win to cursor from screen to cursor to get pos when dragged

    timing 

    """

"""
ctk.set_appearance_mode('dark')
ctk.FontManager.load_font('Myriad Pro Light.ttf')

b = AccountWindow(fg_color='systemTransparent')
b.mainloop()

"""
