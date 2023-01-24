# import the necessary packages
import requests
import cv2
# define the URL to our face detection API
url = "http://localhost:8000/app/face_detect/"
# use our face detection API to find faces in images via image URL
image = cv2.imread(r"D:\iMake_flutter\obama.jpg")
payload = {"url": "https://pyimagesearch.com/wp-content/uploads/2015/05/obama.jpg"}
r = requests.post(url, data=payload).json()
# print('r.json() :', r.json())
print("obama.jpg: {}".format(r))

# loop over the faces and draw them on the image
for (startX, startY, endX, endY) in r["faces"]:
	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
print('r["faces"] :',r["faces"])

# show the output image
# cv2.imshow("obama.jpg", image)
# cv2.waitKey(0)

# load our image and now use the face detection API to find faces in
# images by uploading an image directly
image = cv2.imread(r"D:\iMake_flutter\people.jpg")
payload = {"image": open(r"D:\iMake_flutter\people.jpg", "rb")}
r = requests.post(url, files=payload).json()
print("people.jpg: {}".format(r))

# loop over the faces and draw them on the image
for (startX, startY, endX, endY) in r["faces"]:
	cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)

# show the output image
cv2.imshow("people.jpg", image)
cv2.waitKey(0)
cv2.destroyAllWindows()