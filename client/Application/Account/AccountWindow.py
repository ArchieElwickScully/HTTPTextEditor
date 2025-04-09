from multiprocessing.queues import Queue
from tkinter import Event

import customtkinter as ctk
from sys import platform
import math

from client.Application.Account.InfoBox.InfoBox import InfoBox
from client.Application.Account import Frames


class AccountWindow(ctk.CTk):
    def __init__(self, requestQueue: Queue, **kwargs):
        super().__init__(**kwargs)
        self.alerts = InfoBox()

        # vars
        self.requestQueue: Queue = requestQueue     # request queue so that frames can access to send data to rh
        self.lastClick = (0, 0)                     # storing pos of last click for use in window movement
        self.HEIGHT = 400
        self.WIDTH = 650

        # window attributes etc
        self.geometry('650x400')
        self.overrideredirect(True)     # <- this makes the os window manager ignore this window this is cool because it
                                        # removes the top bar at the window allowing for a more sleek look, but creates
                                        # some issues with dragging and focusing window which we fix in code later
        match platform.lower():
            case 'darwin':                                      # we need this here as unfortunately creating a
                self.configure(fg_color='systemTransparent')    # transparent window is entirely platform dependent
                self.wm_attributes("-transparent", True)        # and works differently if at all on separate platforms
            case 'windows':
                self.wm_attributes("-topmost", True)
                self.wm_attributes("-disabled", True)
                self.wm_attributes("-transparentcolor", "white")


        self.centre()

        # setting up binds for window dragging
        self.bind('<Button-1>', self.registerClick)     # binding clicking the left mouse button to registerClick()
        self.bind('<B1-Motion>', self.drag)             # binding dragging mouse while left mouse is down to drag()

        # window stuff
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.mainFrame = Frames.MainFrame(self, width=650, height=400, corner_radius=15)
        self.mainFrame.grid(row=0, column=0)

    # window methods
    def drag(self, e: Event):
        diff = (e.x_root - self.lastClick[0],
                e.y_root - self.lastClick[1])

        # print(diff)
        self.geometry(f'+{diff[0]}+{diff[1]}')

    def registerClick(self, e: Event):
        self.lastClick = (e.x_root - self.winfo_rootx(),    # calculates the last click relative to the window by
                          e.y_root - self.winfo_rooty())    # subtracting the distance from the cursor to the leftmost
                                                            # and topmost of screen from the leftmost and topmost of win
        # print(self.lastClick)
        # print(self.lastClick[0], e.x_root, self.winfo_pointerx(), self.winfo_rootx())

    def centre(self):
        x = math.trunc((self.winfo_screenwidth() / 2) - (self.WIDTH / 2))       # kinda self explanitory i hope
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
