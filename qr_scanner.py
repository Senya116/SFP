import cv2
from pyzbar.pyzbar import decode

def scan_qr_code(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray)

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f"Scanned product info: {barcode_data}")
        return barcode_data

    return None