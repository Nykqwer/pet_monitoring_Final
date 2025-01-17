# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Frame, Tk, Canvas, Entry, Text, Button, PhotoImage
from build.main_window.activity.add_act.gui4 import AddActivity
from build.main_window.activity.view_act.gui1 import ViewActivity
from build.main_window.activity.up_act.gui8 import UpActivity
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


#window = Tk()

#window.geometry("1032x655")
#window.configure(bg = "#FFFFFF")


def activity():
    Activity()
    

class Activity(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_rid = None
        
        self.configure(bg="#FFFFFF")
        
        self.windows = {
            "add": AddActivity(self),
            "view": ViewActivity(self),
            "up": UpActivity(self),
       
        }
        
        self.current_window = self.windows["add"]
        self.current_window.place(x=0, y=0, width=1032.0, height=655.0)
        
        self.current_window.tkraise()

    def navigate(self, name):
        # Hide all screens
        for window in self.windows.values():
            window.place_forget()

        # Show the screen of the button pressed
        self.windows[name].place(x=0, y=0, width=1032.0, height=655.0)