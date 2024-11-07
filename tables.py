import pymupdf  # PyMuPDF

def extract_text_structure(pdf_path):
    doc = pymupdf.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc[page_num]
        print(f"Page {page_num + 1}")
        
        # Iterate over blocks in the page
        for block in page.get_text("dict")["blocks"]:
            print("\n  Block:")
            print(f"    Type: {block['type']}")
            print(f"    Bounding Box: {block['bbox']}")

            # Check if block contains text (type 0)
            if block["type"] == 0:
                for line in block["lines"]:
                    print("    Line:")
                    print(f"      Bounding Box: {line['bbox']}")

                    # Iterate over spans in the line
                    for span in line["spans"]:
                        print("      Span:")
                        print(f"        Text: {span['text']}")
                        print(f"        Font: {span['font']}")
                        print(f"        Font Size: {span['size']}")
                        print(f"        Color: {span['color']}")
                        print(f"        Ascender: {span['ascender']}")
                        print(f"        Descender: {span['descender']}")
                        print(f"        Origin: {span['origin']}")
                        print(f"        Bounding Box: {span['bbox']}")
                        print(f"        Flags: {span['flags']}")
    doc.close()

# Usage example
pdf_path = "test.pdf"  # Replace with your PDF file path
extract_text_structure(pdf_path)
