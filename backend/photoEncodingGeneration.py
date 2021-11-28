import face_recognition
import numpy
from os import listdir
from os.path import isfile, join
import json

dict128VectorPhotos = {}
dirRoot = "lfw"
dirList = listdir(dirRoot)
for dirName in dirList:
    dirPhoto = join(dirRoot, dirName)
    photoList = listdir(dirPhoto)
    for photo in photoList:
        img = face_recognition.load_image_file(join(dirPhoto, photo))
        imgEncoding = face_recognition.face_encodings(img)
        if len(imgEncoding) != 0:
            arrayKey = str(tuple(imgEncoding[0]))
            if arrayKey in dict128VectorPhotos:
                print("Vector repetido en", dirName, photo)
            else:
                dict128VectorPhotos[arrayKey] = join(dirPhoto, photo)

with open('data.json', 'a', encoding="utf-8") as file:
    file.write(json.dumps(dict128VectorPhotos, ensure_ascii=False))
    file.close()
