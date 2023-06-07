import argparse
from PIL import Image
import ocrmypdf
from PyPDF2 import PdfReader

parser = argparse.ArgumentParser()
parser.add_argument('-doc', required=True, help='Path to the document to be processed (pdf, png, jpg, jpeg)')

args = parser.parse_args()

## primeiro transformar arquivo escaneado (se for imagem) para um formato pdf
extension = args.doc[len(args.doc) - 4:]
fileName = args.doc[:len(args.doc) - 4]

if extension != '.pdf':
     image = Image.open(args.doc)
     image.convert('RGB').save("{}.pdf".format(fileName))

filePath = fileName + '.pdf'

## fazer com que o arquivo pdf possa ser "buscavel", ou seja, que seja possível selecionar os textos do arquivo
## para que funcine, é preciso instalar Ghostscript e colocar "...\gs\gsx.x\bin" no PATH do sistema.
resultPDF = fileName + 'processed.pdf'
ocrmypdf.ocr(filePath, resultPDF, skip_text=True)

## Extrair texto do arquivo pdf
reader = PdfReader(resultPDF)
page = reader.pages[0]
text = page.extract_text()
print(text)

## aplicar algo para compreender o que se encontra no texto
## pode enviar para alguma ia. O exemplo abaixo é usando o hugchat (free)