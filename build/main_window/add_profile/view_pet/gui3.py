from tkinter import Frame, Label, Tk, Canvas, Button, PhotoImage
from PIL import Image, ImageTk, ImageFile, ImageDraw
from io import BytesIO
import base64
from pathlib import Path
import controller as db_controller
import textwrap

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def decode_base64(encoded_str):
    try:
        if isinstance(encoded_str, str):
            encoded_str = encoded_str.encode('utf-8')

        padding = b'=' * (4 - (len(encoded_str) % 4))
        encoded_str += padding

        decoded_data = base64.b64decode(encoded_str)
        return decoded_data
    except base64.binascii.Error as e:
        print(f"Error decoding base64: {e}")
        return None

class AddProfile(Frame):
    def __init__(self, parent, controller=None, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.selected_rid = None

        self.retrieve_data_fromDb()
        self.photo = self.image_retrieve()
        self.recommendation()

        self.setup_ui()
        
        self.auto_refresh_interval = 5000  # 2 seconds
        self.auto_refresh()

    def setup_ui(self):
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=655,
            width=1032,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0.0, 0.0, 1032.0, 655.0, fill="#FFFFFF", outline="")

        self.image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
        self.image_1 = self.canvas.create_image(332.9998779296875, 425.000244140625, image=self.image_image_1)

        self.button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
        self.button_1 = Button(
            self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.parent.navigate("edit"),
            relief="flat"
        )
        self.button_1.place(x=728.0, y=470.0, width=284.0, height=72.66717529296875)

        self.image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
        self.image_2 = self.canvas.create_image(494.0, 346.0, image=self.image_image_2)

        self.image_image_3 = PhotoImage(file=relative_to_assets("image_3.png"))
        self.image_3 = self.canvas.create_image(368.0, 67.0, image=self.image_image_3)

        self.image_image_4 = PhotoImage(file=relative_to_assets("image_4.png"))
        self.image_4 = self.canvas.create_image(355.0, 478.0, image=self.image_image_4)

        self.image_image_5 = PhotoImage(file=relative_to_assets("image_5.png"))
        self.image_5 = self.canvas.create_image(698.0, 328.6625671386719, image=self.image_image_5)

        self.name_text = self.canvas.create_text(118.0, 140.0, anchor="nw", text=self.pet_info_dict['name'], fill="#030303", font=("RobotoRoman SemiBold", 20 * -1))
        self.breed_text = self.canvas.create_text(451.0, 140.0, anchor="nw", text=self.pet_info_dict['breed'], fill="#030303", font=("RobotoRoman SemiBold", 20 * -1))

        pet_weight = self.pet_info_dict['weight']
        pet_age = self.pet_info_dict['age']
        pet_text_weight = ''
        pet_text_age = ''

        if pet_weight.lower() == 'no info yet' and pet_age.lower() == 'no info yet':
            pet_text_weight = pet_weight
            pet_text_age = pet_age
        else:
            pet_text_weight = pet_weight + ' KG'
            pet_text_age1 = float(pet_age)
            if pet_text_age1 <= 1:
                pet_text_age = pet_age + ' Year old'
            else:
                pet_text_age = pet_age + ' Years old'

        self.weight_text = self.canvas.create_text(451.0, 248.0, anchor="nw", text=pet_text_weight, fill="#030303", font=("RobotoRoman SemiBold", 20 * -1))
        self.age_text = self.canvas.create_text(119.0, 248.0, anchor="nw", text=pet_text_age, fill="#030303", font=("RobotoRoman SemiBold", 20 * -1))
        self.heal_con_text = self.canvas.create_text(118.0, 351.0, anchor="nw", text=self.pet_info_dict['heal_con'], fill="#030303", font=("RobotoRoman SemiBold", 20 * -1))

        self.recommendation_text = self.canvas.create_text(143, 523.0, anchor="nw", text=self.recommend, fill="#000000", font=("RobotoRoman SemiBold", 18 * -1))


        # Create the label only if it doesn't exist
        if not hasattr(self, 'image_label'):
            self.image_label = Label(self)

        # Configure the label with the default image
        self.image_label.configure(image=self.photo)
        self.image_label.image = self.photo  # To keep a reference

        # Place the label on your Tkinter window
        self.image_label.place(x=770, y=57)

    def image_retrieve(self):
        encoded_image = self.pet_info_dict['image']
        decoded_image = decode_base64(encoded_image)

        if encoded_image != '':
            image_stream = BytesIO(decoded_image)
            try:
                original_image = Image.open(image_stream)
                resized_image = original_image.resize((200, 200))
                mask = Image.new('L', (200, 200), 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 200, 200), fill=255)
                circular_image = Image.new('RGBA', (200, 200), 0)
                circular_image.paste(resized_image, mask=mask)
                self.photo = ImageTk.PhotoImage(circular_image)
            except Exception as e:
                print(f"Error processing image: {e}")
                self.photo = PhotoImage(file=relative_to_assets("def_img.png"))
        else:
            self.photo = PhotoImage(file=relative_to_assets("def_img.png"))
        return self.photo

    def recommendation(self):
        pet_weight_text = self.pet_info_dict['weight']
        pet_age_text = self.pet_info_dict['age']
        pet_type = self.pet_info_dict['breed']
        recommend = ''

        if  pet_weight_text == 'No Info yet' and pet_age_text == 'No Info yet':
            recommend = "there's no Info just yet"
        else:
            pet_weight = float(pet_weight_text)
            pet_age = float(pet_age_text)

            if pet_type.lower() == 'dog':
                if pet_age <= 1:
                    if pet_weight <= 10:
                        recommend = 'Adjust meal portions based on weight to ensure healthy growth.'
                    elif pet_weight <= 25:
                        recommend = 'Adjust meal portions based on weight to support steady growth'
                    else:
                        recommend = 'Adjust meal portions based on weight to support proper development'
                elif pet_age > 1:
                    if pet_weight <= 10:
                        recommend = 'Monitor weight and adjust portions to prevent obesity'
                    elif pet_weight <= 25:
                        recommend = 'Monitor weight and adjust portions to maintain a healthy body condition.'
                    else:
                        recommend = 'Monitor weight and adjust portions to prevent excessive strain on joints'
                elif pet_age > 7:
                    if pet_weight <= 10:
                        recommend = 'Monitor weight and adjust portions to prevent obesity and maintain a healthy weight'
                    elif pet_weight <= 25:
                        recommend = 'Regular veterinary check-ups become crucial for early detection of age-related health issues'
                    else:
                        recommend = 'Regular veterinary check-ups are essential for monitoring weight and addressing age-related concerns'
            elif pet_type.lower() == 'cat':
                if pet_age <= 1:
                    if pet_weight <= 3:
                        recommend = 'Adjust meal portions based on weight to ensure healthy growth.'
                    elif pet_weight <= 5:
                        recommend = 'Adjust meal portions based on weight to support steady growth.'
                    else:
                        recommend = 'Adjust meal portions based on weight to support proper development.'
                elif pet_age > 1:
                    if pet_weight <= 3:
                        recommend = 'Monitor weight and adjust portions to prevent obesity.'
                    elif pet_weight <= 5:
                        recommend = 'Monitor weight and adjust portions to maintain a healthy body condition.'
                    else:
                        recommend = 'Monitor weight and adjust portions to prevent excessive strain on joints.'
                elif pet_age > 7:
                    if pet_weight <= 3:
                        recommend = 'Monitor weight and adjust portions to prevent obesity and maintain a healthy weight.'
                    elif pet_weight <= 5:
                        recommend = 'Regular veterinary check-ups become crucial for early detection of age-related health issues.'
                    else:
                        recommend = 'Regular veterinary check-ups are essential for monitoring weight and addressing age-related concerns.'
            elif pet_type.lower() == 'bird':
                if pet_age <= 1:
                    if pet_weight <= 0.1:
                        recommend = 'Provide a balanced diet with seeds, nuts, and fresh produce to support healthy growth.'
                    elif pet_weight <= 0.5:
                        recommend = 'Ensure a diverse diet with pellets, seeds, and fresh fruits to support steady growth.'
                    else:
                        recommend = 'Offer a variety of foods, including pellets, seeds, nuts, and fresh vegetables, for proper development.'
                elif pet_age > 1:
                    if pet_weight <= 0.1:
                        recommend = 'Monitor weight and adjust diet to maintain a healthy body condition.'
                    elif pet_weight <= 0.5:
                        recommend = 'Maintain a balanced diet with a mix of pellets, seeds, and fresh produce to support overall health.'
                    else:
                        recommend = 'Regularly assess weight and adjust the diet as needed. Provide a variety of foods for optimal nutrition.'
                else:
                    recommend = "unknown type of age"
            else:
                recommend = "unknown type of pet"

        # Wrapping the recommendation text to fit within canvas width
        recommendation_wrapped = textwrap.fill(recommend, width=50)
        self.recommend = recommendation_wrapped
        return self.recommend

    def retrieve_data_fromDb(self):
        self.display_pet_info = db_controller.get_petInfo()

        if self.display_pet_info:
            column_names = ['name', 'breed', 'age', 'weight', 'heal_con', 'image']
            pet_info_dict = dict(zip(column_names, self.display_pet_info))
            self.pet_info_dict = pet_info_dict
        else:
            self.pet_info_dict = {'name': 'No Info yet', 'breed': 'No Info yet', 'age': 'No Info yet',
                                  'weight': 'No Info yet', 'heal_con': 'No Info yet', 'image': ''}

        return self.pet_info_dict

    def auto_refresh(self):
        self.retrieve_data_fromDb()
        self.recommendation()
        self.photo = self.image_retrieve()
        self.update_ui()
        self.after(self.auto_refresh_interval, self.auto_refresh)

    def update_ui(self):
        self.canvas.itemconfig(self.name_text, text=self.pet_info_dict['name'])
        self.canvas.itemconfig(self.breed_text, text=self.pet_info_dict['breed'])

        pet_weight = self.pet_info_dict['weight']
        pet_age = self.pet_info_dict['age']
        pet_text_weight = ''
        pet_text_age = ''

        if pet_weight.lower() == 'no info yet' and pet_age.lower() == 'no info yet':
            pet_text_weight = pet_weight
            pet_text_age = pet_age
        else:
            pet_text_weight = pet_weight + ' KG'
            pet_text_age1 = float(pet_age)
            if pet_text_age1 <= 1:
                pet_text_age = pet_age + ' Year old'
            else:
                pet_text_age = pet_age + ' Years old'

        self.canvas.itemconfig(self.weight_text, text=pet_text_weight)
        self.canvas.itemconfig(self.age_text, text=pet_text_age)
        self.canvas.itemconfig(self.heal_con_text, text=self.pet_info_dict['heal_con'])
        self.canvas.itemconfig(self.recommendation_text, text=self.recommend)
        self.image_label.configure(image=self.photo)
        self.image_label.image = self.photo  # To keep a reference


