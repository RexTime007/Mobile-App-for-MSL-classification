from flask import Flask, request
from flask import render_template
import cv2
import main2 as principal
from flask import  render_template, jsonify, request
import os
from werkzeug.utils import secure_filename
import random
import time

app = Flask(__name__)


@app.route("/upload", methods=["POST"], strict_slashes=False)

def index2():
    list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    c = (random.choice(list1))
    if(request.method == "POST"):
        f =  request.files['file']
        print("Uploaded to server")
        filename = secure_filename(f.filename)
        f.save(os.path.join(filename))
        print("Starting preprocess")
        print(c)
        print('sleep ended')
        return str(c)


if __name__ == "__main__":
    app.run (host="0.0.0.0", port=5000,debug=True)