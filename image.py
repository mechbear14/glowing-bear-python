from PIL import Image
from os import path
import numpy

image = None
current_path = path.abspath(path.curdir)

while image is None:
    image_path_input = input("Image path: ")
    image_path = None
    if image_path_input[0] == "/":
        image_path = image_path_input
    else:
        image_path = path.join(current_path, image_path_input)
    try:
        image = Image.open(image_path)
    except OSError:
        print(image_path)
        print("Sorry, try again")

brightness = numpy.array(image.convert("L")) / 255
rows, cols = brightness.shape
row = numpy.flip(numpy.arange(0, rows)).reshape((rows, 1)).repeat(cols, axis=1)
col = numpy.arange(0, cols).reshape((1, cols)).repeat(rows, axis=0)
buffer_data = numpy.array([row, col, brightness])
buffer = buffer_data.reshape(rows * cols * 3, order='F').astype(numpy.float)
