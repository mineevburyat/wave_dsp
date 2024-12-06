import cv2
import numpy as np
z = np.zeros((3,), dtype=np.uint8)

# Включаем первую камеру
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    print("get frame from web camera is ok!")
else:
    quit()
# Отключаем камеру
cap.release()

def create24bitsBMP(frame):
    "фрейм это numpy массив пикселей где пиксель занимает матрицу 3 байта"
    count_pixels = len(frame) * len(frame[0])
    with open("test1.bmp","w+b") as f:
        # BITMAPFILEHEADER 14 байт
        # сигнатура ID field (42h, 4Dh)
        f.write(b'BM')
        #Size of the BMP file
        f.write((count_pixels * 3 + 14 + 40).to_bytes(4,byteorder="little"))
        f.write((0).to_bytes(2,byteorder="little"))#Unused
        f.write((0).to_bytes(2,byteorder="little"))#Unused
        #54 bytes (14+40) Offset where the pixel array (bitmap data) can be found
        f.write((54).to_bytes(4,byteorder="little"))
        # BITMAPINFO версия BITMAPV4HEADER
        f.write((49).to_bytes(4, byteorder="little"))
        f.write((len(frame[0])).to_bytes(4,byteorder="little"))#Width of the bitmap in pixels
        f.write((len(frame)).to_bytes(4,byteorder="little"))#Height of the bitmap in pixels
        f.write((1).to_bytes(2, byteorder="little"))
        f.write((24).to_bytes(2, byteorder="little"))
        f.write((0).to_bytes(4, byteorder="little"))
        f.write((count_pixels * 4).to_bytes(4,byteorder="little"))#32 bytes Size of the raw bitmap data (including padding)
        f.write((2835).to_bytes(4,byteorder="little"))#2835 pixels/metre horizontal Print resolution of the image,
        f.write((2835).to_bytes(4,byteorder="little"))#2835 pixels/metre vertical   72 DPI × 39.3701 inches per metre yields 2834.6472
        f.write((0).to_bytes(4,byteorder="little"))#0 colors Number of colors in the palette
        f.write((0).to_bytes(4,byteorder="little"))#0 important colors 0 means all colors are important
        # BITMAPINFO
        f.write(b'\x00\x00\xFF')#00FF0000 in big-endian Red channel bit mask (valid because BI_BITFIELDS is specified)
        f.write(b'\x00\xFF\x00')#0000FF00 in big-endian Green channel bit mask (valid because BI_BITFIELDS is specified)
        f.write(b'\xFF\x00\x00')#000000FF in big-endian Blue channel bit mask (valid because BI_BITFIELDS is specified)
        for line in frame:
            for pixel in line:
                f.write(pixel.tobytes())
        f.close()

create24bitsBMP(frame)