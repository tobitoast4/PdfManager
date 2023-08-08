# PDF Manager

## Introduction

Maybe you are used to the following scenario: You have two PDF documents, 
and you want to merge them into one. You don't have Adobe Acrobat or similar 
installed and because the content should be kept secret, you don't want to use 
some suspicious *online pdf merger tool*. Or you have scanned a handwritten 
document into a PDF file, but the pages are rotated wrongly. 

## Use cases

This PDF manager application allows you to
- Merge multiple PDF files into one
- Split one PDF file into a new one (remove unwanted pages)
- Rotate selected pages by 90°, 180° or 270°

## Build the executable out of the python modules

1. Create a virtual environment
2. Install the requirements `pip install -r requirements.txt`
3. Install PyInstaller within the venv `pip install pyinstaller`
4. Create the executable `pyinstaller --noconfirm --onedir --windowed  "[...]/PdfManager/app/pdf_editor.py"`
5. Find the output in the `/dist` folder. Feel free to remove unneeded files