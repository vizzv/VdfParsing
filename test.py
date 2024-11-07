import tkinter as tk
from tkinter import filedialog, scrolledtext, font as tkfont, Frame, Scrollbar
from pypdf import PdfReader
from PIL import Image, ImageTk
import io
import threading

def open_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        start_loading_animation()
        threading.Thread(target=display_pdf_content, args=(file_path,)).start()

def display_pdf_content(file_path):
    # Clear previous content
    text_box.delete(1.0, tk.END)
    image_canvas.delete("all")
    
    # Wait for canvas to initialize width
    root.update_idletasks()
    canvas_width = image_canvas.winfo_width()
    
    reader = PdfReader(file_path)
    for page_num, page in enumerate(reader.pages):
        text_box.insert(tk.END, f"--- Page {page_num + 1} ---\n", "header")
        
        # Extract and display text
        text_content = page.extract_text()
        if text_content:
            text_box.insert(tk.END, text_content + "\n\n")

        # Initialize positions and row height for images
        x_offset, y_offset = 10, 10
        row_height = 0
        
        for image_index, image_file in enumerate(page.images):
            image_data = image_file.data
            pil_image = Image.open(io.BytesIO(image_data))
            print("pil-image",pil_image)
            pil_image.thumbnail((200, 200))  # Resize for display
            img = ImageTk.PhotoImage(pil_image)

            # Check if the image fits in the current row; if not, wrap to the next row
            if x_offset + img.width() > canvas_width:
                x_offset = 10  # Reset x position for new row
                y_offset += row_height + 10  # Move y down to new row
                row_height = 0  # Reset row height for new row

            # Place the image on the canvas
            image_canvas.create_image(x_offset, y_offset, anchor="nw", image=img)
            images.append(img)  # Keep reference to avoid garbage collection

            # Update x position for next image and row height for current row
            x_offset += img.width() + 10
            row_height = max(row_height, img.height())

    # Update the scroll region for canvas to enable scrolling
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
root.title("PDF Parser")

# Font and color customization
header_font = tkfont.Font(family="Helvetica", size=16, weight="bold")
button_font = tkfont.Font(family="Helvetica", size=10)

root.configure(bg="#f5f5f5")
open_button = tk.Button(root, text="Open PDF", command=open_pdf, font=button_font, bg="#4caf50", fg="white")
open_button.pack(pady=10)

# Scrollable text box for PDF text
text_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20, font=("Helvetica", 10), bg="#e8f0fe", fg="#333333")
text_box.pack(padx=10, pady=10)
setup_styles()

# Scrollable frame for images
image_frame = Frame(root)
image_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Canvas for displaying images
image_canvas = tk.Canvas(image_frame, width=650, height=400, bg="white")
image_canvas.pack(side="left", fill="both", expand=True)

# Scrollbars for the image canvas
v_scrollbar = Scrollbar(image_frame, orient="vertical", command=image_canvas.yview)
v_scrollbar.pack(side="right", fill="y")
image_canvas.config(yscrollcommand=v_scrollbar.set)

# Track images to prevent garbage collection
images = []

# Loading animation label
loading_active = False
loading_label = tk.Label(root, text="Loading", font=("Helvetica", 12), fg="blue", bg="#f5f5f5")

root.mainloop()
