# import the necessary packages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import numpy as np
import urllib.request
import json
import cv2
import os
import datetime
import base64

from time import process_time

from django.shortcuts import render, HttpResponse

# Create your views here.
def hello_django(request):
    return HttpResponse("Hello Django!")

def date_time():
    x = datetime.datetime.now()
    return x.strftime("%d %b %Y %X")

# define the path to the face detector
FACE_DETECTOR_PATH = "{base_path}/cascades/haarcascade_frontalface_default.xml".format(
 base_path=os.path.abspath(os.path.dirname(__file__)))
@csrf_exempt
def detect(request):
    minneighbors =  request.POST.get("minneighbors",None)
    
    t_start = process_time()
    # initialize the data dictionary to be returned by the request
    data = {"success": False}
    # check to see if this is a post request
    if request.method == "POST":
        # grab the URL from the request
        url = request.POST.get("url", None)
        # if the URL is None, then return an error
        if url is None:
            data["error"] = "No URL provided."
            return JsonResponse(data)
        # load the image and convert
        image = _grab_image(url=url)
        
        # convert the image to grayscale, load the face cascade detector,
        # and detect faces in the image
        # global op_img
        # op_img = image
        dt = date_time()
        colorImg = image.copy()
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detector = cv2.CascadeClassifier(FACE_DETECTOR_PATH)
        rects = detector.detectMultiScale(image, scaleFactor=1.1, minNeighbors=int(minneighbors), minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)
        # construct a list of bounding boxes from the detection
        rects = [(int(x), int(y), int(x + w), int(y + h)) for (x, y, w, h) in rects]
        for (startX, startY, endX, endY) in rects:
            cv2.rectangle(colorImg, (startX, startY), (endX, endY), (0, 255, 0), 2)
        
        ret, buffer = cv2.imencode('.jpg', colorImg)
        jpg_as_text = base64.b64encode(buffer)

        t_stop = process_time()
        total = t_stop-t_start
        # update the data dictionary with the faces detected
        data.update({"image": str(jpg_as_text)[2:-1], "face": len(rects), "date": str(dt), "pro_time": str(total), "success": True})
    
    # return a JSON response
    return JsonResponse(data)


def _grab_image(url=None):
    if url is not None:
        resp = urllib.request.urlopen(url)
        data = resp.read()
        
    image = np.asarray(bytearray(data), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    
    return image