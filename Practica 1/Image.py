from PIL import Image
import numpy as np
import array

def a():
    w, h = 750, 750 
    data = np.zeros((h, w, 3), dtype=np.uint8)
    data[0:256, 0:256] = [255, 0, 0] # red patch in upper left
    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()

def readFile(fileName):
    fileObj = open(fileName, "r") #opens the file in read mode
    words = fileObj.read().splitlines() #puts the file into an array
    fileObj.close()
    return words
def TextToArray(words):
    res = [word.split(",") for word in words]
    for x in res:
        for y in x:
            print(y, end=" ")
        print()

TextToArray(readFile("lab1.txt"))