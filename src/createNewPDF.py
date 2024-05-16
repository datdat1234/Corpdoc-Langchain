########################## LIBRARY ###############################

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

##################################################################

def createLocalPDF(pdf_data, file_path):
    pdf_data = remove_duplicates(pdf_data)
    
    # Create a canvas object with letter-sized pages
    c = canvas.Canvas(file_path, pagesize=letter)

    # Register a Vietnamese font
    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    # Set the font and font size
    c.setFont("Arial", 12)

    # Split the string into lines
    lines = pdf_data.split("\n")

    # Set the position to start writing the text
    x = 50
    y = 750

    for line in lines:
        if y < 50:
            # Create a new page
            c.showPage()
            y = 750
            # Set the font and font size for each new page
            c.setFont("Arial", 12)

        c.drawString(x, y, line)
        y -= 20

    # Save the PDF file
    c.save()

def remove_duplicates(string):
    lines = string.split("\n")
    unique_lines = list(dict.fromkeys(lines))
    result = "\n".join(unique_lines)
    return result