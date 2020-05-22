import numpy as np
import os
import sqlite3
import cv2
import training


#--------------------------------------------------------------------
# CODE NHAP DU LIEU HINH ANH VA DAT TEN KET NOI CO SO DU LIEU
#nhap  du lieu vao db
def insertOrUpdate(id, name,uuid):
    #connecting to the db
    conn =sqlite3.connect("FaceBase.db")
    #check if id already exists
    query = "SELECT * FROM People WHERE ID="+str(id)
    #returning the data in rows
    cursor = conn.execute(query)
    isRecordExist=0
    for row in cursor:
        isRecordExist=1
    if isRecordExist==1:
        query="UPDATE People SET Name="+str(name)+" WHERE ID="+str(id)
    else:
        query="INSERT INTO People(ID, Name,UUID) VALUES("+str(id)+","+str(name)+","+str(uuid)+")"
    conn.execute(query)
    conn.commit()
    conn.close()

def getidNew():
    conn =sqlite3.connect("FaceBase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM People")
    results = cursor.fetchall()
    return len(results)+10;
    
def themNguoi(id,name,docid,db):
    print(id)
    
    ngoac='"'
    idLay = id;
    name =  ngoac + name.split()[-1] + ngoac
    id = getidNew()
    doc_ref = db.collection(u'Command').document(docid)
    face_cascade = cv2.CascadeClassifier('thuvien/khuon_mat.xml')
    doc_ref.update({"state":"READY"})
    #CAMMMMM
    cap = cv2.VideoCapture(0)
    doc_ref.update({"state":"CONNECT CAMERA"})
    insertOrUpdate(id, name,ngoac + idLay + ngoac)
    sample_number = 0
    doc_ref.update({"state":"GET FACE"})
    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            sample_number += 1

            if not os.path.exists('data_face'):
                os.makedirs('data_face')

            cv2.imwrite('data_face/User.'+str(id)+"."+str(sample_number)+".jpg",  img[y:y+h,x:x+w])
            cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0), 2)

        cv2.imshow("img", img)
        cv2.waitKey(1);
        if(sample_number>100):
            cap.release()
            break;
    doc_ref.update({"state":"TRAINING"})
    training.Training()
    db.collection(u'users').document(idLay).update({"hasAddedFace":True})
    doc_ref.update({"state":"DONE"})
    cv2.destroyAllWindows()
def testFunc():
    print("test")
