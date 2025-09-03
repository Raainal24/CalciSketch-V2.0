import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas, Button, Scale, HORIZONTAL, PhotoImage, filedialog, messagebox
from pathlib import Path
import pickle
import os
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

class CalciSketchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CalciSketch")
        self.geometry("1920x1080")
        self.minsize(1280, 720)
        self.configure(fg_color="white")

        # Load assets
        self.bg_image = Image.open("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\bg img.png").resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        logo_img = Image.open("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\logo.png").resize((40, 40))
        self.logo = ImageTk.PhotoImage(logo_img)

        self.about_img = Image.open("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\ABOUT US!!.png").resize((280, 75))
        self.about_photo = ImageTk.PhotoImage(self.about_img)

        self.start_img = Image.open("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\START DRAWING.png").resize((280, 75))
        self.start_photo = ImageTk.PhotoImage(self.start_img)

        # Main container
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.create_navbar()

        for F in (HomePage, AboutPage, DrawingPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            frame.place(relwidth=1, relheight=1)
            self.frames[page_name] = frame

        self.show_frame("HomePage")

    def create_navbar(self):
        navbar = ctk.CTkFrame(self, height=70, fg_color="white")
        navbar.place(relx=0, rely=0, relwidth=1)

        center_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        logo_label = tk.Label(center_frame, image=self.logo, bg="white", bd=0, cursor="hand2")
        logo_label.pack(side="left", padx=(0, 10))
        logo_label.bind("<Button-1>", lambda e: self.show_frame("HomePage"))

        app_name = tk.Label(center_frame, text="CalciSketch", font=("Helvetica Neue", 20, "bold"), fg="black", bg="white")
        app_name.pack(side="left")

    def show_frame(self, page_name):
        for name, frame in self.frames.items():
            frame.place_forget()
        self.frames[page_name].place(relwidth=1, relheight=1)

class HomePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        self.canvas = tk.Canvas(self, width=1920, height=1080, highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)
        self.bg_photo = controller.bg_photo
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

        self.canvas.create_text(960, 440, text="CalciSketch", font=("Helvetica Neue", 48, "bold"), fill="black")
        self.canvas.create_text(960, 500, text="Draw. Solve. Understand. 🚀", font=("Helvetica Neue", 24), fill="black")

        about_btn_id = self.canvas.create_image(880, 570, image=controller.about_photo, anchor="center")
        start_btn_id = self.canvas.create_image(1040, 570, image=controller.start_photo, anchor="center")

        self.canvas.tag_bind(about_btn_id, "<Button-1>", lambda e: controller.show_frame("AboutPage"))
        self.canvas.tag_bind(start_btn_id, "<Button-1>", lambda e: controller.show_frame("DrawingPage"))

class AboutPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller
        self.image={}
        label = ctk.CTkLabel(self, text="About Us Page", font=("Helvetica Neue", 36, "bold"), text_color="black")
        label.place(relx=0.5, rely=0.5, anchor="center")

class DrawingPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="white")
        self.controller = controller

        self.brush_color = "black"
        self.brush_size = 5
        self.eraser_on = False
        self.last_x = None
        self.last_y = None
        self.solution_frame = None
        self.drawing_actions = []
        self.image_refs = {}

        self.create_canvas()
        self.create_toolbar()
        self.bind_canvas_events()
    def show_frame(self, page_name):
        for name, frame in self.frames.items():
            frame.place_forget()
            self.frames[page_name].place(relwidth=1, relheight=1)

    # Dynamic navbar background for DrawingPage
        if page_name == "DrawingPage":
            self.create_navbar(bg_color="#ADD8E6", text_color="black")  # Light blue navbar
        else:
            self.create_navbar(bg_color="white", text_color="black")   # Default white navbar

    def create_navbar(self, bg_color="white", text_color="black"):
        navbar = ctk.CTkFrame(self, height=70, fg_color=bg_color)
        navbar.place(relx=0, rely=0, relwidth=1)

        center_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        logo_label = tk.Label(center_frame, image=self.logo, bg=bg_color, bd=0, cursor="hand2")
        logo_label.pack(side="left", padx=(0, 10))
        logo_label.bind("<Button-1>", lambda e: self.show_frame("HomePage"))

        app_name = tk.Label(center_frame, text="CalciSketch", font=("Helvetica Neue", 20, "bold"),
                        fg=text_color, bg=bg_color)
        app_name.pack(side="left")
    

    def create_canvas(self):
        self.canvas = tk.Canvas(
            self,
            bg="#E0FFFF",
            height=880,
            width=1920,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.pack(side="top")

        # Optional: background image
        try:
            bg_img = tk.PhotoImage(file=self.relative_to_assets("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\image_1.png"))
            self.image_refs["bg"] = bg_img
            self.canvas.create_image(960.0, 440.0, image=bg_img)
        except Exception:
            pass

    def create_toolbar(self):
        from tkinter import Button, Scale, HORIZONTAL, filedialog, messagebox

        toolbar_bg = Button(self, image=self.load_image("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\button_1.png"), borderwidth=0, highlightthickness=0,
                            command=lambda: None, relief="flat")
        toolbar_bg.place(x=190.0, y=906.0, width=1540.0, height=123.0)

        colors = ["red", "yellow", "green", "blue", "white", "black"]
        x_positions = [224.0, 288.0, 353.0, 417.0, 481.0, 545.0]
        for i, color in enumerate(colors):
            Button(self, image=self.load_image(f"D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\button_{i+2}.png"), borderwidth=0, highlightthickness=0,
                   command=lambda c=color: self.change_color(c), relief="flat").place(
                x=x_positions[i], y=937.0, width=63.0, height=63.0)

        Button(self, image=self.load_image("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\button_8.png"), borderwidth=0, highlightthickness=0,
               command=self.use_eraser, relief="flat").place(x=695.0, y=928.0, width=83.0, height=83.0)
        Button(self, image=self.load_image("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\button_9.png"), borderwidth=0, highlightthickness=0,
               command=self.use_brush, relief="flat").place(x=830.0, y=934.0, width=69.0, height=69.0)

        Button(self, image=self.load_image("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\button_12.png"), borderwidth=0, highlightthickness=0,
               command=self.save_work, relief="flat").place(x=1435.0, y=938.0, width=68.0, height=68.0)
        Button(self, image=self.load_image("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\button_13.png"), borderwidth=0, highlightthickness=0,
               command=self.load_work, relief="flat").place(x=1550.0, y=938.0, width=68.0, height=68.0)

        Button(self, image=self.load_image("D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\button_11.png"), borderwidth=0, highlightthickness=0,
               command=self.clear_canvas, relief="flat").place(x=1300.0, y=938.0, width=68.0, height=68.0)

        Scale(self, from_=1, to=10, orient=HORIZONTAL, command=self.change_size).place(x=950, y=938.0, width=300, height=50)

    def bind_canvas_events(self):
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<ButtonRelease-1>", self.reset)

    def paint(self, event):
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        color = "white" if self.eraser_on else self.brush_color

        self.drawing_actions.append({
            'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2,
            'color': color, 'size': self.brush_size
        })
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
        self.last_x, self.last_y = event.x, event.y

    def reset(self, event):
        self.last_x = self.last_y = None

    def change_color(self, new_color):
        self.brush_color = new_color
        self.use_brush()

    def change_size(self, value):
        self.brush_size = int(value)

    def use_brush(self):
        self.eraser_on = False

    def use_eraser(self):
        self.eraser_on = True

    def clear_canvas(self):
        self.canvas.delete("all")
        self.drawing_actions.clear()
        if self.solution_frame:
            self.solution_frame.destroy()
            self.solution_frame = None

    def save_work(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("Drawing Files", "*.pkl"), ("All Files", "*.*")],
            initialdir=os.path.expanduser("~\\Documents")
        )
        if file_path:
            try:
                with open(file_path, 'wb') as f:
                    pickle.dump(self.drawing_actions, f)
                messagebox.showinfo("Success", "Drawing saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")

    def load_work(self):
        from tkinter import filedialog, messagebox
        file_path = filedialog.askopenfilename(
            filetypes=[("Drawing Files", "*.pkl"), ("All Files", "*.*")],
            initialdir=os.path.expanduser("~\\Documents")
        )
        if file_path:
            try:
                with open(file_path, 'rb') as f:
                    loaded_actions = pickle.load(f)
                self.clear_canvas()
                for action in loaded_actions:
                    self.canvas.create_oval(
                        action['x1'], action['y1'],
                        action['x2'], action['y2'],
                        fill=action['color'],
                        outline=action['color']
                    )
                    self.drawing_actions.append(action)
                messagebox.showinfo("Success", "Drawing loaded successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")

    def load_image(self, path):
        try:
            image = tk.PhotoImage(file=path)
            self.image_refs[path] = image  # Keep a reference so it's not garbage collected
            return image
        except Exception as e:
            print(f"Failed to load {path}: {e}")
            blank = tk.PhotoImage(width=68, height=68)
            self.image_refs[path] = blank
            return blank



if __name__ == "__main__":
    app = CalciSketchApp()
    app.mainloop()