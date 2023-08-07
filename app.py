from re import DEBUG, sub
from flask import Flask, render_template, request, redirect, send_file, url_for
from werkzeug.utils import secure_filename, send_from_directory
import os
import subprocess
import threading

app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')

os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def hello_world1():
    return render_template('login.html')

@app.route("/exam")
def hello_world():
    return render_template('index.html')


@app.route("/detect", methods=['POST'])
def detect():
    if not request.method == "POST":
        return
    video = request.files['video']
    video.save(os.path.join(uploads_dir, secure_filename(video.filename)))
    print(video)
    subprocess.run("ls", shell=True)
    subprocess.run(['py', 'detect.py', '--source', os.path.join(uploads_dir, secure_filename(video.filename))], shell=True)

    obj = secure_filename(video.filename)
    return obj

@app.route("/opencam", methods=['GET'])
def opencam():
    print("Camera starting")
    threads = []
    # Define the number of webcams to open
    num_webcams = 1
    # Launch a separate thread for each webcam
    for i in range(num_webcams):
        t = threading.Thread(target=run_detection, args=(i,))
        threads.append(t)
        t.start()
    # Wait for all threads to complete before returning response
    for t in threads:
        t.join()
    return "done"

def run_detection(cam_index):
    subprocess.run(['py', 'detect.py', '--source', str(cam_index)], shell=True)

@app.route('/return-files', methods=['GET'])
def return_file():
    obj = request.args.get('obj')
    loc = os.path.join("runs/detect", obj)
    print(loc)
    try:
        return send_file(os.path.join("runs/detect", obj), attachment_filename=obj)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)