from flask import Flask
from flask_restful import Resource, Api,request
import cv2
import face_recognition
import json
import numpy as np
import requests, io
import urllib
import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


#defining app server
app=Flask(__name__)
#defining api
api=Api(app)


class FaceIdentification(Resource):

    def get(self):
        image_url1 = request.args.get('image_url1')
        image_url2 = request.args.get('image_url2')
        url_response1 = urllib.request.urlopen(image_url1)
        url_response2 = urllib.request.urlopen(image_url2)
        image = face_recognition.load_image_file(url_response1)
        image_test = face_recognition.load_image_file(url_response2)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_test = cv2.cvtColor(image_test, cv2.COLOR_BGR2RGB)
        facelocations = face_recognition.face_locations(image)[0]
        facelocations_test = face_recognition.face_locations(image_test)[0]
        if (len(facelocations)==0 or len(facelocations_test)==0):
            return {"exception":"No face detected"}
        else:
            faceencodings = face_recognition.face_encodings(image)[0]
            faceencodings_test = face_recognition.face_encodings(image_test)[0]
            results = face_recognition.compare_faces([faceencodings],faceencodings_test)
            res = ' '.join([str(elem) for elem in results])
            return {
                "key matched value":res
            }



api.add_resource(FaceIdentification,'/images/')
if __name__ == "__main__":
    app.run(port=5001)
