import numpy as np
import os
import nhandien
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
import pickle, sqlite3
import themnguoidung
import cv2
from PIL import Image
from datetime import date
import time
import datetime
from threading import Thread
import threading
import time
# khoi tao firebase
cred = credentials.Certificate('building-tracking-system-firebase-adminsdk-znxh0-88a74d7b0e.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
doc_ref = db.collection(u'Command')
def Run():
    print("chay lai run")
    

    def on_snapshot (doc_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                print(u'New cmd: {}'.format(change.document.id))
                print(u'data add: {}'.format(change.document.to_dict()['cmd']))
                if change.document.to_dict()['cmd'] == "TRAIN":
                    if change.document.to_dict()['state'] == "CONNECT" :
                        
                        themnguoidung.themNguoi(change.document.to_dict()['userId'],change.document.to_dict()['userName'],change.document.id,db)
                if change.document.to_dict()['cmd'] == "ONALL":
                    if change.document.to_dict()['state'] == "CONNECT" :
                        doc_ref.document(change.document.id).update({
                            'state':'DONE'
                            })
                        listFunc = []
                        rooms_ref = db.collection(u'rooms').stream()
                        for room in rooms_ref:
                            print(u'{} => {}'.format(room.id, room.to_dict()))
                            data = room.to_dict()
                            t = threading.Thread(target=nhandien.NhanDien, args=(data['cameraId'],room.id,change.document.id,db,data['name']))
                            listFunc.append(t)
                        k =threading.Thread(target = Run,args=())
                        
                        listFunc.append(k)
                        for func in listFunc:
                            func.start()
                        for func in listFunc:
                            func.join()

                            
                   
            elif change.type.name == 'MODIFIED':
                print(u'Modified cmd: {}'.format(change.document.id))
                print(u'data change: {}'.format(change.document.to_dict()['cmd']))
            elif change.type.name == 'REMOVED':
                print(u'Removed cmd: {}'.format(change.document.id))
                delete_done.set()

    doc_watch = doc_ref.on_snapshot(on_snapshot)
if __name__ == '__main__':
    Run()
