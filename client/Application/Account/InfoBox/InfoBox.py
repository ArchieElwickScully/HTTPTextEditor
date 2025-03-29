import customtkinter as ctk
from tkinter import StringVar
from sys import platform

import math


class InfoBox(ctk.CTkToplevel):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.iconify()

        self.transparent = 'transparent'

        if platform.lower() == 'darwin':
            self.transparent = 'systemTransparent'
            self.configure(fg_color='systemTransparent')
            self.wm_attributes("-transparent", True)
        elif platform.lower() == 'windows':
            self.wm_attributes("-topmost", True)
            self.wm_attributes("-disabled", True)
            self.wm_attributes("-transparentcolor", "white")


        self.message = StringVar()
        self.lastClick = (0, 0)

        self.mainFrame = ctk.CTkFrame(master = self, corner_radius = 15)
        self.mainFrame.pack(expand = 'true', fill = 'both')

        self.textBox = ctk.CTkLabel(self.mainFrame, textvariable = self.message,
                                  font = ctk.CTkFont('Myriad Pro Light', 25, 'normal'),
                                  text_color = '#DDDDDD', corner_radius = 15)
        self.textBox.pack(side = ctk.LEFT, expand = 'true', padx = 10, pady = 20)

        self.mainFrameBG = self.mainFrame.cget('fg_color')
        self.exitButton = ctk.CTkButton(self.mainFrame, text = 'close',
                                        fg_color = self.mainFrame.cget('fg_color'), bg_color= self.transparent,
                                        background_corner_colors = (self.mainFrameBG, self.transparent,
                                                                    self.transparent, self.mainFrameBG),
                                        corner_radius = 15, command = self.close)
        self.exitButton.pack(expand = 'true', fill = 'y')

        self.protocol("WM_DELETE_WINDOW", self.close)
        self.bind('<Button-1>', self.registerClick)
        self.bind('<B1-Motion>', self.drag)

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

    def setText(self, text):
        if self.winfo_viewable():
            self.close()
            self.setText(text)

        self.message.set(text)

        self.update_idletasks()
        self.deiconify()

        self.overrideredirect(False)
        self.focus_set()
        self.overrideredirect(True)

        self.centre()


    def centre(self):
        x = math.trunc((self.winfo_screenwidth() / 2) - (self.winfo_width() / 2))
        y = math.trunc((self.winfo_screenheight() / 2) - (self.winfo_height() / 2))

        self.geometry(f'+{x}+{y}')

    def close(self):
        self.withdraw()
        self.master.overrideredirect(False)     # this looks really strange but ive found it fixes an issue
        self.master.focus_set()                 # with tkinter where windows with overrideredirect dont properly
        self.master.overrideredirect(True)      # refocus
        self.master.update_idletasks()


"""
class InfoBox(ctk.CTkToplevel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

        self.title('Clide InfoBox')

        self.mainFrame = ctk.CTkFrame(master=self)
        self.mainFrame.pack(expand = 'true', fill = 'both')

        self.textBox = ctk.CTkLabel(self.mainFrame, text=self.text,
                                  font=ctk.CTkFont('Myriad Pro Light', 25, 'normal'),
                                  text_color='#DDDDDD')
        self.textBox.pack(side = ctk.BOTTOM, expand='true')

        self.exitButton = ctk.CTkButton(self.mainFrame, text = 'Close',
                                        width = 10, height = 10, command = self.close)
        self.exitButton.pack(side = ctk.LEFT)

        # window adjustments
        self.textBox.update()
        self.width = self.textBox.winfo_width() + 30
        self.height = self.textBox.winfo_height() + 40

        self.geometry(f'{self.width}x{self.height}')
        self.centre()

        # on close method
        #self.protocol("WM_DELETE_WINDOW", self.onClose())

    def centre(self):
        x = math.trunc((self.winfo_screenwidth() / 2) - (self.width / 2))
        y = math.trunc((self.winfo_screenheight() / 2) - (self.height / 2))

        self.geometry(f'+{x}+{y}')

    def close(self):
        self.withdraw()
        self.quit()

def newInfoBox(text):
    InfoBox(text)
"""