import tkinter as tk
from tkinter import filedialog, scrolledtext, font as tkfont, Frame, Scrollbar
from pypdf import PdfReader
from PIL import Image, ImageTk
import io
import threading

# Constants for image grid layout
IMAGE_SIZE = 200
SPACING = 10

def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        start_loading_animation()
        threading.Thread(target=display_pdf_content, args=(file_path,)).start()

def display_pdf_content(file_path):
    # Clear previous content
    text_box.delete(1.0, tk.END)
    for widget in image_frame.winfo_children():
        widget.destroy()

    # Extract images from PDF
    reader = PdfReader(file_path)
    images.clear()  # Clear previous images
    for page_num, page in enumerate(reader.pages):
        # Add page header
        text_box.insert(tk.END, f"--- Page {page_num + 1} ---\n", "header")

        
        # Extract and display text
        text_content = page.extract_text()
        if text_content:
            text_box.insert(tk.END, text_content + "\n\n")

        # Extract and process images from the page
        for image_file in page.images:
            image_data = image_file.data
            pil_image = Image.open(io.BytesIO(image_data))
            pil_image.thumbnail((IMAGE_SIZE, IMAGE_SIZE))  # Resize to 200x200
            img = ImageTk.PhotoImage(pil_image)
            images.append(img)  # Append to keep reference

    # Display images in a grid layout within image_frame
    x, y = 0, 0
    for idx, img in enumerate(images):
        label = tk.Label(image_frame, image=img)
        label.grid(row=y, column=x, padx=SPACING // 2, pady=SPACING // 2)

        # Move to the next column
        x += 1
        if ( x * (IMAGE_SIZE + SPACING * 2)) > image_canvas.winfo_width():
            x = 0  # Reset to first column
            y += 1  # Move to next row

    # Update scrollable area
    image_frame.update_idletasks()
    image_canvas.config(scrollregion=image_canvas.bbox("all"))
    stop_loading_animation()

def start_loading_animation():
    global loading_active
    loading_active = True
    loading_label.place(relx=0.5, rely=0.5, anchor="center")
    update_loading_animation()

def stop_loading_animation():
    global loading_active
    loading_active = False
    loading_label.place_forget()

def update_loading_animation():
    current_text = loading_label.cget("text")
    if current_text.endswith("..."):
        loading_label.config(text="Loading")
    else:
        loading_label.config(text=current_text + ".")
    if loading_active:
        root.after(500, update_loading_animation)

def setup_styles():
    text_box.tag_configure("header", font=("Helvetica", 12, "bold"), foreground="blue")

# Initialize main GUI window
root = tk.Tk()
root.title("PDF Image Grid Viewer")

# Font and color customization
header_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
button_font = tkfont.Font(family="Helvetica", size=10)

root.configure(bg="#f5f5f5")
open_button = tk.Button(root, text="Open PDF", command=open_pdf, font=button_font, bg="#4caf50", fg="white")
open_button.pack(pady=10)

# Scrollable text box for PDF text
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Helvetica", 10), bg="#e8f0fe", fg="#333333")
text_box.pack(padx=10, pady=10, fill="both", expand=True)
setup_styles()

# Scrollable frame for images
image_frame_container = Frame(root)
image_frame_container.pack(padx=10, pady=10, fill="both", expand=True)

# Canvas for displaying images
image_canvas = tk.Canvas(image_frame_container, width=800, height=400, bg="white")
image_canvas.pack(side="left", fill="both", expand=True)

# Scrollbars for the image canvas
v_scrollbar = Scrollbar(image_frame_container, orient="vertical", command=image_canvas.yview)
v_scrollbar.pack(side="right", fill="y")
image_canvas.config(yscrollcommand=v_scrollbar.set)

# Frame to hold images inside the canvas
image_frame = Frame(image_canvas)
image_canvas.create_window((0, 0), window=image_frame, anchor="nw")

# Track images to prevent garbage collection
images = []

# Loading animation label
loading_active = False
loading_label = tk.Label(root, text="Loading", font=("Helvetica", 12), fg="blue", bg="#f5f5f5")

root.mainloop()
