from pathlib import Path
from tkinter import Tk, Canvas, Button, Scale, HORIZONTAL, PhotoImage, Text, Scrollbar, Frame, filedialog, messagebox
from PIL import ImageGrab
import google.generativeai as genai
import ollama
import tempfile
import os
import pickle

# ================== REMOTE OLLAMA CONFIGURATION ==================
ollama_client = ollama.Client(host="http://localhost:11450") # Client for remote server
# ================================================================

api_key = "insert your api key"
genai.configure(api_key=api_key)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\\Studies\\Mini Project 4\\Python\\GUI\\Assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

root = Tk()
root.geometry("1920x1080")
root.configure(bg="#FFFFFF")

brush_color = "black"
brush_size = 5
eraser_on = False
last_x = None
last_y = None
solution_frame = None
drawing_actions = []

canvas = Canvas(
    root,
    bg="#FFFFFF",
    height=880,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

image_refs = {}

def paint(event):
    global last_x, last_y, brush_color, brush_size, eraser_on, drawing_actions
    x1, y1 = (event.x - brush_size), (event.y - brush_size)
    x2, y2 = (event.x + brush_size), (event.y + brush_size)
    color = "white" if eraser_on else brush_color
    
    drawing_actions.append({
        'x1': x1,
        'y1': y1,
        'x2': x2,
        'y2': y2,
        'color': color,
        'size': brush_size
    })
    
    canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)
    last_x, last_y = event.x, event.y

def reset(event):
    global last_x, last_y
    last_x = last_y = None

def change_color(new_color):
    global brush_color
    brush_color = new_color
    use_brush()

def change_size(value):
    global brush_size
    brush_size = int(value)

def use_brush():
    global eraser_on
    eraser_on = False

def use_eraser():
    global eraser_on
    eraser_on = True

def clear_canvas():
    global solution_frame, drawing_actions
    canvas.delete("all")
    drawing_actions.clear()
    if solution_frame:
        solution_frame.destroy()
        solution_frame = None

def display_solution_box(steps):
    global solution_frame
    if solution_frame:
        solution_frame.destroy()
    solution_frame = Frame(canvas, bg="white", bd=2, relief="solid")
    canvas.create_window(960, 700, window=solution_frame, anchor="n", width=1820, height=180)

    text_widget = Text(solution_frame, wrap="word", font=("Helvetica", 20), bg="white")
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(solution_frame, command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")

    text_widget.config(yscrollcommand=scrollbar.set)

    for step in steps:
        text_widget.insert("end", step + "\n")

def evaluate_expression():
    global last_x, last_y
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()

    image = ImageGrab.grab().crop((x, y, x1, y1))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        image.save(temp_file.name)
        temp_image_path = temp_file.name

    try:
        # Use Gemini for image recognition
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content([
            genai.upload_file(temp_image_path),
            "Identify the expression from the input image and rewrite it using standard mathematical symbols (like ∫, ×, ², ³, fractions), avoiding LaTeX notations. Ensure the expression is clear and easy to read."
        ])

        if response and response.text:
            parsed_expression = response.text.strip()
            
            # Use Remote Ollama/Mistral for solving
            ollama_response = ollama_client.chat(
                model='mistral',
                messages=[{
                    "role": "user",
                    "content": f"""Solve this expression step-by-step: {parsed_expression}. Provide a clear, concise breakdown of the solution, avoiding any LaTeX or verbose explanations. 
                                Rules:
                                1. Use only standard math symbols
                                2. Show intermediate steps
                                3. No LaTeX or markdown
                                4. Keep explanations concise"""
                }]
            )
            
            steps = ollama_response['message']['content'].split("\n")
            display_solution_box(steps)
            
    except Exception as e:
        messagebox.showerror("Error", f"Evaluation failed: {str(e)}")
    finally:
        os.remove(temp_image_path)

def save_work():
    global drawing_actions
    file_path = filedialog.asksaveasfilename(
        defaultextension=".pkl",
        filetypes=[("Drawing Files", "*.pkl"), ("All Files", "*.*")],
        initialdir=os.path.expanduser("~\\Documents")
    )
    if file_path:
        try:
            with open(file_path, 'wb') as f:
                pickle.dump(drawing_actions, f)
            messagebox.showinfo("Success", "Drawing saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")

def load_work():
    global drawing_actions
    file_path = filedialog.askopenfilename(
        filetypes=[("Drawing Files", "*.pkl"), ("All Files", "*.*")],
        initialdir=os.path.expanduser("~\\Documents")
    )
    if file_path:
        try:
            with open(file_path, 'rb') as f:
                loaded_actions = pickle.load(f)
            
            clear_canvas()
            
            for action in loaded_actions:
                canvas.create_oval(
                    action['x1'], action['y1'],
                    action['x2'], action['y2'],
                    fill=action['color'],
                    outline=action['color']
                )
                drawing_actions.append(action)
            
            messagebox.showinfo("Success", "Drawing loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")

def load_image(name):
    image = PhotoImage(file=relative_to_assets(name))
    image_refs[name] = image
    return image

canvas.create_image(960.0, 440.0, image=load_image("image_1.png"))

# Toolbar buttons
Button(image=load_image("button_1.png"), borderwidth=0, highlightthickness=0,
       command=lambda: print("button_1 clicked"), relief="flat").place(x=190.0, y=906.0, width=1540.0, height=123.0)

colors = ["red", "yellow", "yellow", "blue", "white", "black"]
x_positions = [224.0, 288.0, 353.0, 417.0, 481.0, 545.0]
for i, color in enumerate(colors):
    Button(image=load_image(f"button_{i+2}.png"), borderwidth=0, highlightthickness=0,
           command=lambda c=color: change_color(c), relief="flat").place(x=x_positions[i], y=937.0, width=63.0, height=63.0)

# Tools section
Button(image=load_image("button_8.png"), borderwidth=0, highlightthickness=0,
       command=use_eraser, relief="flat").place(x=883.0, y=928.0, width=83.0, height=83.0)

Button(image=load_image("button_9.png"), borderwidth=0, highlightthickness=0,
       command=use_brush, relief="flat").place(x=749.0, y=934.0, width=69.0, height=69.0)

# File operations
Button(image=load_image("button_12.png"), borderwidth=0, highlightthickness=0,
       command=save_work, relief="flat").place(x=1600.0, y=938.0, width=68.0, height=68.0)

Button(image=load_image("button_13.png"), borderwidth=0, highlightthickness=0,
       command=load_work, relief="flat").place(x=1670.0, y=938.0, width=68.0, height=68.0)

# Evaluation tools
Button(image=load_image("button_10.png"), borderwidth=0, highlightthickness=0,
       command=evaluate_expression, relief="flat").place(x=1450.0, y=920.0, width=97.0, height=97.0)

Button(image=load_image("button_11.png"), borderwidth=0, highlightthickness=0,
       command=clear_canvas, relief="flat").place(x=1350.0, y=938.0, width=68.0, height=68.0)

Scale(from_=1, to=10, orient=HORIZONTAL, command=change_size).place(x=1060, y=938.0, width=300, height=50)

canvas.bind("<B1-Motion>", paint)
canvas.bind("<ButtonRelease-1>", reset)

root.resizable(False, False)
root.mainloop()

