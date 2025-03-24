import customtkinter as ctk


class InfoBox(ctk.CTkToplevel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text

        self.geometry('250x100')
        self.title('Clide InfoBox')

        self.mainFrame = ctk.CTkFrame(master=self)
        self.mainFrame.pack(expand = 'true', fill = 'both')

        self.textBox = ctk.CTkLabel(self.mainFrame, text=self.text,
                                  font=ctk.CTkFont('Myriad Pro Light', 25, 'normal'),
                                  text_color='#DDDDDD')
        self.textBox.pack(expand='true')

def newInfoBox(text):
    InfoBox(text)