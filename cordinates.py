import tkinter as tk
from tkinter import scrolledtext
import pymupdf  # PyMuPDF

def int_to_rgb(color_int):
    """Convert RGB integer to an (R, G, B) tuple."""
    r = (color_int >> 16) & 255
    g = (color_int >> 8) & 255
    b = color_int & 255
    return (r, g, b)

def extract_text_with_details_by_page(pdf_path):
    # Open the PDF file
    doc = pymupdf.open(pdf_path)
    text_details_by_page = {}

    for page_num in range(doc.page_count):
        page = doc[page_num]
        page_text_details = []

        # Extract text details (word by word with coordinates and styling)
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:  # This is a text block
                for line in block["lines"]:
                    for span in line["spans"]:
                        
                        text = span["text"]
                        font_size = span["size"]
                        font_name = span["font"]
                        color_rgb = int_to_rgb(span["color"])  # Convert color integer to RGB tuple
                        x0, y0, x1, y1 = span["bbox"]  # Bounding box coordinates

                        # Append each word's details to this page's list
                        page_text_details.append({
                            "text": text,
                            "font_size": font_size,
                            "font_name": font_name,
                            "color": color_rgb,
                            "x0": x0,
                            "y0": y0,
                            "x1": x1,
                            "y1": y1
                        })

        # Store text details for the current page
        text_details_by_page[page_num + 1] = page_text_details

    doc.close()
    return text_details_by_page

class PdfTextViewer:
    def __init__(self, root, pdf_path):
        self.root = root
        self.pdf_path = pdf_path

        # Extract text details from the PDF
        self.details_by_page = extract_text_with_details_by_page(pdf_path)

        # Create a canvas to draw the text with positions and styles
        self.canvas = tk.Canvas(root, width=800, height=1000, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Add a scrollbar
        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill="y")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        # Load and render the first page (can be extended for multi-page)
        self.render_page(1)

    def render_page(self, page_num):
        page_details = self.details_by_page.get(page_num)
        if not page_details:
            return

        # Clear canvas for new page rendering
        self.canvas.delete("all")

        # Loop through the text details and draw them with respective styles
        for detail in page_details:
            text = detail["text"]
            font_size = detail["font_size"]
            font_name = detail["font_name"]
            color = detail["color"]
            x0, y0, x1, y1 = detail["x0"], detail["y0"], detail["x1"], detail["y1"]

            # Convert the RGB tuple to hex color
            color_hex = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

            # Create font style
            font = (font_name, int(font_size))  # Tkinter font requires a tuple (name, size)

            # Draw text at the appropriate coordinates on the canvas
            self.canvas.create_text(x0, y0, text=text, font=font, fill=color_hex, anchor="nw")

def main(pdf_path):
    root = tk.Tk()
    root.title("PDF Text Display with Styles")

    viewer = PdfTextViewer(root, pdf_path)

    root.mainloop()

# Example usage
pdf_path = "test.pdf"  # Replace with your PDF file path
main(pdf_path)
