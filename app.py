import argparse
from PIL import Image
import ocrmypdf
from PyPDF2 import PdfReader
from docquery import document, pipeline
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "E:\Programs\Tesseract\tesseract.exe"

parser = argparse.ArgumentParser()
parser.add_argument('-doc', required=True, help='Path to the document to be processed (pdf, png, jpg, jpeg)')

args = parser.parse_args()

## First, convert the scanned file (if it is an image) to a PDF format
extension = args.doc[len(args.doc) - 4:]
fileName = args.doc[:len(args.doc) - 4]

if extension != '.pdf':
     image = Image.open(args.doc)
     image.convert('RGB').save("{}.pdf".format(fileName))

filePath = fileName + '.pdf'

## Make the PDF file searchable, meaning that it is possible to select the text within the file. 
# To make it work, you need to install Ghostscript and add '...\gs\gsx.x\bin' to the system's PATH."
resultPDF = fileName + 'processed.pdf'
ocrmypdf.ocr(filePath, resultPDF, skip_text=True)

## Extract text from the PDF file.
reader = PdfReader(resultPDF)
page = reader.pages[0]
text = page.extract_text()
print(text)

## Now we can use a LLM model to extract info from the document
p = pipeline('document-question-answering');
doc = document.load_document(resultPDF);
for q in ['What is the name of the company ?', 'What is the total invoice amount?']:
     print(q, p(question=q, **doc.context));
