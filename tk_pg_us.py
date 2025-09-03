from tkinter import *
from PIL import Image, ImageTk, ImageDraw
import customtkinter as ctk
import webbrowser

def make_rounded_image(img, radius):
    """Returns a rounded-corner version of the given PIL image."""
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([0, 0, img.size[0], img.size[1]], radius=radius, fill=255)
    img.putalpha(mask)
    return img

def round_rectangle(canvas, x1, y1, x2, y2, radius=35, **kwargs):
    """Draw a rounded rectangle on the canvas."""
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

class AboutUsApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("About Us Page")
        self.geometry("1920x1080")
        self.resizable(True, True)

        # Set background image
        bg_image = Image.open(r"D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\bg_image1.png")
        bg_image = bg_image.resize((1920, 1080))
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_navbar()
        self.create_content()

    def create_navbar(self):
        navbar = ctk.CTkFrame(self, height=80, fg_color="white", corner_radius=0)
        navbar.pack(fill="x", side="top")

        self.menu_button = ctk.CTkButton(navbar, text="≡", width=20, corner_radius=10, fg_color="black",
                                         text_color="white", hover_color="#333")
        self.menu_button.pack(side="left", padx=10, pady=10)

        logo_frame = ctk.CTkFrame(navbar, fg_color="transparent")
        logo_frame.place(relx=0.55, rely=0.5, anchor="center")

        logo_img = Image.open(r"D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\logo.png").resize((40, 40))
        self.logo = ImageTk.PhotoImage(logo_img)
        logo_label = ctk.CTkLabel(logo_frame, image=self.logo, text="")
        logo_label.pack(side="left", padx=(0, 10))

        logo_text = ctk.CTkLabel(logo_frame, text="CalciSketch", font=("Helvetica Neue", 20, "bold"), text_color="black")
        logo_text.pack(side="left")

    def create_content(self):
        image_paths = [
            r"D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\amal_Card.png",
            r"D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\shib_card.png",
            r"D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\dharsh_Card.png",
            r"D:\\Studies\\Mini Project 4\\Python\\Final\\final codes\\Assets\\rahul_Card.png",
        ]
        linkedin_urls = [
            "https://www.linkedin.com/in/raainal/",
            "https://www.linkedin.com/in/shib-sobhan-mohanty-53957b252/",
            "https://www.linkedin.com/in/dharshini-guruprasath/",
            "https://www.linkedin.com/in/rahul-gadhiraju-805542252/",
        ]
        profiles = [
            "Expert in model training and execution, ensuring robust machine learning performance.",
            "Versatile full stack developer, skilled in both frontend and backend, and seamless integration.",
            "UI specialist who transformed design concepts into functional, user-friendly code.",
            "Contributed creative design ideas to enhance the visual appeal of the project."
        ]

        self.card_images = []
        card_width = 300
        card_height = 340
        spacing = 160
        corner_radius = 35

        total_width = len(image_paths) * card_width + (len(image_paths) - 1) * spacing
        start_x = (1920 - total_width) // 2
        y = 300

        for i, (img_path, linkedin_url, profile) in enumerate(zip(image_paths, linkedin_urls, profiles)):
            img = Image.open(img_path).resize((card_width, card_height))
            rounded_img = make_rounded_image(img, corner_radius)
            photo = ImageTk.PhotoImage(rounded_img)
            self.card_images.append(photo)

            card_container = Canvas(
                self, 
                width=card_width, 
                height=card_height, 
                bg="white", 
                bd=0, 
                highlightthickness=0
            )
            x = start_x + i * (card_width + spacing)
            card_container.place(x=x, y=y)

            # Draw rounded rectangle as card background
            round_rectangle(card_container, 0, 0, card_width, card_height, radius=corner_radius, fill="white", outline="")

            # Place rounded image on canvas
            card_container.create_image(0, 0, anchor="nw", image=photo)

            # Profile label (no name label, slightly above the button)
            profile_label = Label(
                card_container,
                text=profile,
                font=("Arial", 12),
                bg="white",
                wraplength=card_width-20,
                justify="center"
            )
            profile_label.place(relx=0.5, rely=0.74, anchor="center")

            # LinkedIn button (moved up, still below profile)
            btn = Button(
                card_container,
                text="LinkedIn",
                fg="white",
                bg="#0077b5",
                font=("Arial", 12, "bold"),
                cursor="hand2",
                relief="flat",
                command=lambda url=linkedin_url: webbrowser.open_new(url)
            )
            btn.place(
                relx=0.5, 
                rely=0.90,   # <--- moved up from 0.96 to 0.85
                anchor="center", 
                width=100, 
                height=30
            )

if __name__ == "__main__":
    app = AboutUsApp()
    app.mainloop()
