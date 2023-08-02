from pypdf import PdfWriter, PdfReader

reader = PdfReader("x.pdf")
writer = PdfWriter()


pages_to_rotate = [0]

for page in range(len(reader.pages)):
    writer.add_page(reader.pages[page])
    if page in pages_to_rotate:
        writer.pages[page].rotate(180)

with open("x_rotate.pdf", "wb") as fp:
    writer.write(fp)