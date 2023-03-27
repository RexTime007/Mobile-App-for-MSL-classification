from flask import Flask, request
from flask import render_template
import main2 as principal
from flask import  render_template, jsonify, request
import os
import time

import webbrowser

from werkzeug.utils import secure_filename


app = Flask(__name__)

@app.before_first_request
def loadData():
    print('Preparing server to keep uploaded signs in server')
    global sign_recorder
    sign_recorder = principal.preproceso()
    


@app.route("/upload", methods=["POST"], strict_slashes=False)
def index2():
    if(request.method == "POST"):
        f =  request.files['file']
        print("Uploaded to server")
        filename = secure_filename(f.filename)
        f.save(os.path.join(filename))
        print("Starting preprocess")
       
        try:
            result = principal.proceso(sign_recorder)
        except:
            result = 'No hay puntos suficientes para determinar la seña'
        print(result)
          
        return result

@app.route("/test")
def testing():
    print('TESTING ZONE   ')
    
    
        
# your code here    

    result = principal.proceso(sign_recorder)
    print(result)
    return result

if __name__ == "__main__":
    app.run (host="0.0.0.0", port=5000,debug=True, use_reloader=False)