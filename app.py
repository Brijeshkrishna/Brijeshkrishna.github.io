from flask import Flask, render_template,send_file
import json
import os
from worker import *

# set environ
# IMAGES_COUNT=1
# PROCESS_IMG=400000



global CERTIFICATE_LIST
CERTIFICATE_LIST = json.loads(get_certificate())

app = Flask(__name__, template_folder="template", static_folder="static")

generate_img_init(int(os.environ.get("IMAGES_COUNT",2)))


print("Server started.. 👍")
@app.route("/")
def response():

    global CERTIFICATE_LIST

    img_id = "static/imgs/background" + str(remove_images()) + ".webp"
    if not os.path.exists(img_id):
        img_id = "static/imgs/back.jpg"

    return render_template("./index.html", img_id=img_id, cert_data=CERTIFICATE_LIST)

@app.route("/static/imgs/<img_id>")
def send_img(img_id):
    print(img_id)
    return send_file(f"./static/imgs/{img_id}")