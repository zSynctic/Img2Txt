import webbrowser
import customtkinter
import os
import sys
import tkinter
from CTkToolTip import *
import pytesseract as pyt
from PIL import Image, ImageTk


class App(customtkinter.CTk):
    WIDTH = 900
    HEIGHT = 600

    IMAGE_WIDTH = 450
    IMAGE_HEIGHT = 450

    ICON_WIDTH = 50
    ICON_HEIGHT = 50

    global resource

    def resource(relative_path):
        base_path = getattr(sys, "_MEIPASS", os.path.dirname(
            os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")

    def __init__(self):
        super().__init__()

        self.title("Img2Txt")
        self.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.p1 = ImageTk.PhotoImage(file=resource("Assets/icon.ico"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.p1)

        self.sidebarframe = customtkinter.CTkFrame(
            master=self, width=300, height=602, corner_radius=30
        )
        self.sidebarframe.place(x=-19, y=-1)

        self.imageframe = customtkinter.CTkFrame(
            master=self, width=500, height=500, corner_radius=30
        )
        self.imageframe.place(x=340, y=50)

        self.image = customtkinter.CTkImage(
            dark_image=Image.open(resource("Assets/icon.png")),
            size=(self.ICON_WIDTH, self.ICON_HEIGHT),
        )
        self.button = customtkinter.CTkButton(
            master=self.sidebarframe,
            text="Img2Txt",
            image=self.image,
            width=300,
            height=150,
            bg_color="transparent",
            fg_color="transparent",
            hover_color="#2B2B2B",
            cursor="hand2",
            font=("Roboto Bold", -30),
        )
        self.button.place(x=3, y=-25)

        self.button.bind(
            "<Button-1>",
            lambda event: webbrowser.open_new_tab(
                "https://github.com/zSynctic/Img2Txt"),
        )

        self.tooltip = CTkToolTip(
            self.button,
            message="Star me on GitHub ⭐",
            delay=0,
        )

        self.tabview = customtkinter.CTkTabview(
            master=self.sidebarframe,
            fg_color="#2B2B2B",
            corner_radius=30,
            width=290,
            height=480,
        )
        self.tabview.place(x=10, y=90)
        self.tabview.add("Home")
        self.tabview.add("Result")
        self.tabview.set("Home")

        self.tabview._segmented_button._buttons_dict["Home"].configure(
            width=70, height=30, font=("Roboto Medium", -14)
        )
        self.tabview._segmented_button._buttons_dict["Result"].configure(
            width=70, height=30, font=("Roboto Medium", -14)
        )

        self.step1 = customtkinter.CTkLabel(
            master=self.tabview.tab("Home"),
            text="Step 1",
            text_color="#A6ADAE",
            font=("Roboto Bold", -16),
        )
        self.step1.place(x=0, y=20)

        self.ChooseFileButton = customtkinter.CTkButton(
            master=self.tabview.tab("Home"),
            text="SELECT IMAGE",
            width=110,
            height=45,
            corner_radius=8,
            font=("Roboto Bold", -14),
            command=self.open_FileImage,
        )
        self.ChooseFileButton.place(x=0, y=50)

        self.step2 = customtkinter.CTkLabel(
            master=self.tabview.tab("Home"),
            text="Step 2",
            text_color="#A6ADAE",
            font=("Roboto Bold", -16),
        )
        self.step2.place(x=0, y=180)

        self.ExtractButton = customtkinter.CTkButton(
            master=self.tabview.tab("Home"),
            text="EXTRACT",
            width=100,
            height=45,
            corner_radius=8,
            font=("Roboto Bold", -14),
            command=self.ExtractToText,
        )
        self.ExtractButton.place(x=0, y=210)

        self.ExtractedLabel = customtkinter.CTkLabel(
            master=self.tabview.tab("Result"),
            text="Extracted Text:",
            font=("Roboto Medium", -15),
        )
        self.ExtractedLabel.place(x=60, y=0)

        self.ExtractedTextBox = customtkinter.CTkTextbox(
            master=self.tabview.tab("Result"),
            width=220,
            height=340,
            activate_scrollbars=True,
        )
        self.ExtractedTextBox.place(x=8, y=40)

        self.ExtractLabel = customtkinter.CTkLabel(
            master=self.imageframe,
            text="Select an Image to Extract",
            text_color="#A6ADBA",
            font=("Roboto Bold", -16),
        )
        self.ExtractLabel.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)

        self.copyright = customtkinter.CTkButton(
            master=self.sidebarframe,
            text="""Copyright (C) 2023 - Img2Txt
By zSynctic""",
            text_color="#686F7A",
            bg_color="transparent",
            fg_color="transparent",
            hover_color="#2B2B2B",
            cursor="hand2",
            font=("Roboto Medium", -13),
        )
        self.copyright.place(x=70, y=560)

        self.copyright.bind(
            "<Button-1>",
            lambda event: webbrowser.open_new_tab(
                "https://github.com/zSynctic/Img2Txt"),
        )

    def open_FileImage(self):
        global file
        file = tkinter.filedialog.askopenfilename(
            filetypes=[
                ("Images", ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp"]),
                ("All Files", "*.*"),
            ]
        )
        self.loadImage()

    def loadImage(self):
        global file
        loadedimage = customtkinter.CTkImage(
            dark_image=Image.open(os.path.join(file)),
            size=(self.IMAGE_WIDTH, self.IMAGE_HEIGHT),
        )
        self.ExtractLabel.destroy()
        image_label = customtkinter.CTkLabel(
            master=self.imageframe,
            image=loadedimage,
            text="",
        )
        image_label.place(x=26, y=25)

    def ExtractToText(self):
        global file, txt
        try:
            txt = pyt.image_to_string(file)
        except:
            pass
        self.ExtractedTextBox.delete(1.0, tkinter.END)
        self.ExtractedTextBox.insert(tkinter.END, txt)

    def on_close(self, event=0):
        self.destroy()

    def start(self):
        self.mainloop()


if __name__ == "__main__":
    app = App()
    app.resizable(False, False)
    app.update()
    app.start()
