########################## LIBRARY ###############################

from reportlab.pdfgen import canvas

##################################################################


def createLocalPDF(pdf_data, file_path):
    # Create a canvas object
    c = canvas.Canvas(file_path)

    # Set the font and font size
    c.setFont("Helvetica", 12)

    # Set the position to start writing the text
    x = 50
    y = 750

    # Split the string into lines
    lines = pdf_data.split("\n")

    # Write each line to the PDF
    for line in lines:
        c.drawString(x, y, line)
        y -= 20

    # Save the PDF file
    c.save()
