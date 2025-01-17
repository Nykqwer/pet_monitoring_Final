
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Frame, StringVar, Tk, Canvas, Entry, Text, Button, PhotoImage, messagebox
import controller as db_controller

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


def add_activity():
    AddActivity()
    

class AddActivity(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        
        self.data = {"type_act": StringVar(), "duration": StringVar(), "dt_act": StringVar(), "note": StringVar()}

        canvas = Canvas(
            self,
            bg = "#FFFFFF",
            height = 655,
            width = 1032,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)
        canvas.create_rectangle(
            0.0,
            0.0,
            1032.0,
            655.0,
            fill="#FFFFFF",
            outline="")

        canvas.create_rectangle(
            697.0,
            73.66256713867188,
            699.0,
            585.319091796875,
            fill="#EFEFEF",
            outline="")

        self.image_image_1 = PhotoImage(
            file=relative_to_assets("image_1.png"))
        image_1 = canvas.create_image(
            485.0,
            327.5029296875,
            image=self.image_image_1
        )

        self.button_image_1 = PhotoImage(
            file=relative_to_assets("button_1.png"))
        button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.save,
            relief="flat"
        )
        button_1.place(
            x=214.0,
            y=577.355712890625,
            width=231.0,
            height=54.74924087524414
        )

        self.button_image_2 = PhotoImage(
            file=relative_to_assets("button_2.png"))
        button_2 = Button(
            self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("view"),
            relief="flat"
        )
        button_2.place(
            x=720.0,
            y=184.156494140625,
            width=284.0,
            height=72.66717529296875
        )

        entry_image_1 = PhotoImage(
            file=relative_to_assets("entry_1.png"))
        entry_bg_1 = canvas.create_image(
            190.64930725097656,
            246.91891860961914,
            image=entry_image_1
        )
        entry_1 = Entry(
            self,
            textvariable=self.data["type_act"],
            bd=0,
            bg="#E6E6E6",
            fg="#000716",
            highlightthickness=0
        )
        entry_1.place(
            x=64.2464599609375,
            y=232.0,
            width=252.80569458007812,
            height=27.83783721923828
        )

        canvas.create_text(
            64.0,
            234.0,
            anchor="nw",
            text="Running",
            fill="#000000",
            font=("Montserrat SemiBold", 17 * -1)
        )

        entry_image_2 = PhotoImage(
            file=relative_to_assets("entry_2.png"))
        entry_bg_2 = canvas.create_image(
            508.64942932128906,
            246.91891860961914,
            image=entry_image_2
        )
        entry_2 = Entry(
            self,
            textvariable=self.data["dt_act"],
            bd=0,
            bg="#E6E6E6",
            fg="#000716",
            highlightthickness=0
        )
        entry_2.place(
            x=382.24658203125,
            y=232.0,
            width=252.80569458007812,
            height=27.83783721923828
        )

        canvas.create_text(
            382.0,
            234.0,
            anchor="nw",
            text="Oct 25 12 A.M",
            fill="#767272",
            font=("RobotoRoman SemiBold", 18 * -1)
        )

        entry_image_3 = PhotoImage(
            file=relative_to_assets("entry_3.png"))
        entry_bg_3 = canvas.create_image(
            190.64930725097656,
            360.91891860961914,
            image=entry_image_3
        )
        entry_3 = Entry(
            self,
            textvariable=self.data["duration"],
            bd=0,
            bg="#E6E6E6",
            fg="#000716",
            highlightthickness=0
        )
        entry_3.place(
            x=64.2464599609375,
            y=346.0,
            width=252.80569458007812,
            height=27.83783721923828
        )

        canvas.create_text(
            64.0,
            348.0,
            anchor="nw",
            text="20 mins",
            fill="#767272",
            font=("RobotoRoman SemiBold", 18 * -1)
        )

        entry_image_4 = PhotoImage(
            file=relative_to_assets("entry_4.png"))
        entry_bg_4 = canvas.create_image(
            510.5,
            418.5,
            image=entry_image_4
        )
        self.entry_4 = Text(
            self,
            bd=0,
            bg="#E6E6E6",
            fg="#000716",
            highlightthickness=0
        )
        self.entry_4.place(
            x=384.0,
            y=333.0,
            width=253.0,
            height=169.0
        )

        canvas.create_text(
            393.0,
            342.0,
            anchor="nw",
            text="gasdgdsgsgsdgsdgsdg",
            fill="#767272",
            font=("RobotoRoman SemiBold", 18 * -1)
        )
        
           
  # Save the data to the database
    def save(self):
         # Get the text content from the Text widget
        note_content = self.entry_4.get("1.0", "end-1c")
        
        self.data["note"].set(note_content)
        
        # check if any fields are empty
        for val in self.data.values():
            if val.get() == "":
                messagebox.showinfo("Error", "Please fill in all the fields")
                return

        # Save the room
        result = db_controller.add_activity(
            *[self.data[label].get() for label in ("type_act", "duration", "dt_act","note")]
        )

        if result:
            messagebox.showinfo("Success", "activity added successfully")
            self.parent.navigate("view")
            self.parent.windows.get("view").handle_refresh()
       
            # Clear the data in the Text widget
            self.entry_4.delete("1.0", "end")
            # clear all fields
            for label in self.data.keys():
                self.data[label].set('')
        else:
            messagebox.showerror(
                "Error", "Unable to activity. Please make sure the data is validated"
            )
            

