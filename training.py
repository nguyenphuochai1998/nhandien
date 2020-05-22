import os
import shutil
import cv2
import numpy as np
from PIL import Image

# CODE TRAINING (HUAN LUYEN) HINH ANH NHAN DIEN
def Training():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'data_face'
    recognizer.read("huanluyen/huanluyen.yml")
    def getImagesWithID(path):
        imagePaths=[os.path.join(path, f) for f in os.listdir(path)]
        faces=[]
        IDs=[]
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID= int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow('training', faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.update(faces, Ids)

    if not os.path.exists('trainer'):
        os.makedirs('trainer')
    shutil.rmtree('data_face', ignore_errors=True)
    recognizer.write('huanluyen/huanluyen.yml')

