import Image
import pytesseract
print(pytesseract.image_to_string(Image.open('File_000.jpeg'),config='-psm 10'))
