from flask import Flask, flash, request, redirect, url_for, render_template
import cv2, os, secrets
from PIL import Image
import cv2

START_FOLDER_PATH = "flaskface/static/start/"
FINISH_FOLDER_PATH = 'flaskface/static/finish/'

face_app = Flask(__name__)

ACCEPTED_MIMETYPES = set(["image/jpeg", "image/jpg", "image/png"])


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(
        form_picture.filename
    )  # _ underscore was used to throw away unused variable
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/start", picture_fn)
    
    # Resize image
    output_size = (1024, 768)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    # save picture
    i.save(picture_path)

    return picture_fn
    # write a code to delete previous avatar


def detect_face(img_to_detect):

    random_hex = secrets.token_hex(8)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    img = cv2.imread(START_FOLDER_PATH + img_to_detect)

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_img, scaleFactor=1.2, minNeighbors=6)

    for (x, y, w, h) in faces:
        img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
        roi_gray = gray_img[y : y + h, x : x + w]
        roi_color = img[y : y + h, x : x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            roi_gray = cv2.rectangle(
                roi_color, (ex, ey), (ex + ew, ey + eh), (255, 0, 0), 3
            )

    fnp = (random_hex + ".jpg")  # file name and path for detected  faces
    cv2.imwrite(FINISH_FOLDER_PATH + fnp, img)

    return fnp


