import firebase_admin
from firebase_admin import db
from firebase_admin import credentials
import os
import json


def connectRef():
    if not firebase_admin._apps:
        key = os.environ["FIREBASE_KEY"]
        cred = credentials.Certificate(json.loads(key,strict=False))
        firebase_admin.initialize_app(cred, {'databaseURL': 'https://mksokuji-default-rtdb.firebaseio.com/'})
    ref = db.reference('user')
    return ref

def update(upDict):
    ref = connectRef()
    ref.update(upDict)

def clear():
    ref = connectRef()
    ref.set({'test':{'teams':['AA','BB','CC'],'scores':[200,100,50],'left':10}})

if __name__ == '__main__':
    clear()