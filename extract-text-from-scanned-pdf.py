# https://pythonguides.com/extract-text-from-pdf-python/
# https://stackoverflow.com/questions/62040294/extracting-text-from-scanned-pdf-images-using-python-pypdf2
# https://pdf2image.readthedocs.io/en/latest/installation.html
#
# https://github.com/madmaze/pytesseract
# https://tesseract-ocr.github.io/tessdoc/Home.html
# https://anaconda.org/conda-forge/pytesseract
# https://pytesseract.readthedocs.io/en/latest/
# tesseract D:\Dico_Francais_Baoule_Extrait/dico_fr_bci_1.png D:\Dico_Francais_Baoule_Extrait/eurotext-eng -l lat+eng pdf
# tesseract D:\Dico_Francais_Baoule_Extrait/dico_fr_bci_1.png D:\Dico_Francais_Baoule_Extrait/dico_fr_bci_1 -l lat+eng pdf
from PyPDF2 import PdfFileReader
import pdf2image
from tkinter import *
from tkinter import filedialog
import pytesseract
from pytesseract import Output, TesseractError

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
# D:\Dico_Francais_Baoule_Extrait\pytesseract\pytesseract

ws = Tk()
ws.title('TEXT FROM (SCANNED) PDF FILES')
ws.geometry('400x300')
ws.config(bg='#D9653B')

def choose_pdf():
      filename = filedialog.askopenfilename(
            initialdir = "/",   # for Linux and Mac users
          # initialdir = "C:/",   for windows users
            title = "Select a File",
            filetypes = (("PDF files","*.pdf*"),("all files","*.*")))
      if filename:
          return filename


def read_pdf():
    filename = choose_pdf()
    #filename = "D:\Dico_Francais_Baoule_Extrait\Dico_FR_BCI.pdf"
    print("filename: ", filename)
    #reader = PdfFileReader(filename)
    #pageObj = reader.getNumPages()
    images = pdf2image.convert_from_path(filename)
    #for page_count in range(pageObj):
    #    page = reader.getPage(page_count)
    #    page_data = page.extractText()
    #    textbox.insert(END, page_data)
    print("len(images): ", len(images))
    text = ""
    final_text = ""
    i=1
    for page_count in range(len(images)):
        page = images[page_count]
        # ocr_dict now holds all the OCR info including text and location on the image
        ocr_dict = pytesseract.image_to_data(page, lang='lat', output_type=Output.DICT)
        #pil_im = images[0]
        text = " ".join(ocr_dict['text'])
        text = text.split("  ")
        #print("Content text KKJC :", text)
        #break
        for elt in text:
            #print("Content text KKJC :", elt)
            if i==1 and len(elt)>0:
                final_text = elt
            elif len(elt)>0 and i%2==0:
                final_text += " | " + elt + "\n"
            elif len(elt)>0 and i%2!=0 and i!=1:
                final_text += elt
            else:
                continue
            i=i+1
        textbox.insert(END, final_text)

def copy_pdf_text():
    content = textbox.get(1.0, "end-1c")
    with open("Extracted text from provided PDF file.txt", 'w') as f:
        f.write(content)
        f.close()
    ws.withdraw()
    ws.clipboard_clear()
    ws.clipboard_append(content)
    ws.update()
    #textbox.destroy()
    #ws.info("Successful Extraction, go to the extracted file please.")
    ws.destroy()


textbox = Text(
    ws,
    height=13,
    width=40,
    wrap='word',
    bg='#D9BDAD'
)
textbox.pack(expand=True)

Button(
    ws,
    text='Choose Pdf File',
    padx=20,
    pady=10,
    bg='#262626',
    fg='white',
    command=read_pdf
).pack(expand=True, side=LEFT, pady=10)

Button(
    ws,
    text="Copy Text",
    padx=20,
    pady=10,
    bg='#262626',
    fg='white',
    command=copy_pdf_text
).pack(expand=True, side=LEFT, pady=10)


ws.mainloop()
