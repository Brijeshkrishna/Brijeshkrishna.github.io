from flask import Flask, render_template
import json
import os
from asgiref.wsgi import WsgiToAsgi
from worker import *

# set environ
# IMAGES_COUNT=1
# PROCESS_IMG=400000



global CERTIFICATE_LIST
CERTIFICATE_LIST = json.loads(get_certificate())

app = Flask(__name__, template_folder="template", static_folder="static")

generate_img_init(int(os.environ.get("IMAGES_COUNT",25)))


print("Server started.. 👍")
@app.route("/")
async def response():

    global CERTIFICATE_LIST

    img_id = "static/imgs/background" + str(remove_images()) + ".webp"
    if not os.path.exists(img_id):
        img_id = "static/imgs/background.webp"

    return render_template("./index.html", img_id=img_id, cert_data=CERTIFICATE_LIST)

app = WsgiToAsgi(app)