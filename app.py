from app import uface
from flask import Flask, flash, request, redirect, url_for, render_template
from app import ACCEPTED_MIMETYPES
from app import save_picture, detect_face


@uface.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file.mimetype == "application/octet-stream":
            message = "Please Select a File."
            return render_template("index.html", message=message)
        if file.mimetype not in ACCEPTED_MIMETYPES:
            message = "Only JPG / PNG image files"
            return render_template("index.html", message=message)
        if file:
            filename = save_picture(file)
            print(filename)
            processed_img = detect_face(filename)
            return render_template("index.html", processed_img=processed_img)

    return render_template("index.html")


if __name__ == "__main__":
    uface.debug = True
    uface.run()

