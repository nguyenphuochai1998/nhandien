import numpy as np
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pickle, sqlite3
import cv2
from PIL import Image
from datetime import date
import time
import datetime 
#----------- ---------------------------------------------------------
# CODE KET NOI DU LIEU NHAN DIEN HINH ANH KHUON MAT
# khoi tao firebase 

#------------------------------------------------------
def NhanDien(cam,docIdPhong,docIdCmd,db,tieude):
    face_cascade = cv2.CascadeClassifier('thuvien/khuon_mat.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("huanluyen/huanluyen.yml")
    # ket noi voi database va lay du lieu thong qua id dc nhan dien tu file yml
    def getProfile(Id):
        conn=sqlite3.connect("FaceBase.db")
        query="SELECT * FROM People WHERE ID="+str(Id)
        cursor=conn.execute(query)
        profile=None
        for row in cursor:
            profile=row
        conn.close()
        return profile
    def updateNhanDien(idUser,nameUser) :
        doc_ref = db.collection(u'rooms').document(docIdPhong).collection(u'room-accessed-history').document()
        
        doc_ref.set({
            'Name':nameUser,
            'Id User':idUser,
            'TimeToRoom':datetime.datetime.utcnow()
        })
        doc_ref_his = db.collection(u'room-accessed-history').document()
        doc_ref_his.set({
            "accessType":"face_system",
            "accessedAt":datetime.datetime.now().isoformat(),
            "action":"open",
            "displayName":nameUser,
            "roomId":docIdPhong,
            "userId":idUser
        })
        doc_ref_room = db.collection(u'rooms').document(docIdPhong)
        
        doc_ref_room.update({
            'doorStatus':"open",
            
        })
        time.sleep(5)
        doc_ref_room.update({
            'doorStatus':"closed",
            
        })
        
        doc_ref_his.set({
            "accessType":"face_system",
            "accessedAt":datetime.datetime.now().isoformat(),
            "action":"closed",
            "displayName":nameUser,
            "roomId":docIdPhong,
            "userId":idUser
        })
        
    #mo cam....
    cap = cv2.VideoCapture(cam)
    font = cv2.FONT_HERSHEY_COMPLEX
    k = 0
    while True:
        #comment the next line and make sure the image being read is names img when using imread
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #nhan ra khuon mat va ve hinh vuong
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w, y+h), (204,219, 33), 2)
            roi_gray = gray[y:y+h, x:x+w]

            roi_color = img[y:y+h, x:x+w]

            nbr_predicted, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 70:
                profile=getProfile(nbr_predicted) 
                if profile != None:
                    cv2.putText(img, ""+str(profile[1])+str(profile[0]), (x+10, y), font, 1, (204,219, 33), 1);
                    updateNhanDien(str(profile[2]),str(profile[1]))
                    
            else:
                cv2.putText(img, "Unknown", (x, y + h + 30), font, 0.4, (204,219, 33), 1);
                today = date.today()
                if not os.path.exists('data'):
                    os.makedirs('data')
                
                cv2.imwrite('data/Unknown.'+str(today.strftime("%b%d%Y"))+str(k)+'.jpg',  img[y:y+h,x:x+w])
                print('data/Unknown.'+str(today.strftime("%b%d%Y"))+'.jpg')
                k = k + 1 


        cv2.imshow(tieude, img)
        if(cv2.waitKey(1) == ord('q')):
            break
    cap.release()
    cv2.destroyAllWindows()

