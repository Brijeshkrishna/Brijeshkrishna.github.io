from flask import Flask, render_template
import threading
from PIL import Image
import numpy as np
import json
from tqdm import tqdm
import time
import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__, template_folder="template", static_folder="static")


global IMG_STACK
global IMG_STACK_PROGRESS
global REPOS_LIST
global CERTIFICATE_LIST
global PROCESS_IMG


def get_certificate():
    with open("cert.json", "r") as f:
        return f.read()


REPOS_LIST = []
IMG_STACK = []
IMG_STACK_PROGRESS = []
CERTIFICATE_LIST = json.loads(get_certificate())
PROCESS_IMG = int(os.environ["PROCESS_IMG"])


def generate_img(filename="background.webp", dir="./", id=None):

    global IMG_STACK_PROGRESS
    IMG_STACK_PROGRESS.append(id)
    filename = dir + filename

    width = 2400
    height = 1350

    gen = np.random.default_rng(int(time.perf_counter_ns()))
    img = Image.new(
        "RGB",
        (width, height),
        (gen.integers(0, 255), gen.integers(0, 255), gen.integers(0, 255)),
    )
    total = (
        PROCESS_IMG  # gen.integers(0, height) * gen.integers(0, width) % PROCESS_IMG
    )
    for _ in tqdm(range(0, total), desc=f"Generating Image... [{id}]", leave=1):
        img.putpixel(
            (gen.integers(0, width - 1), gen.integers(0, height - 1)),
            (gen.integers(0, 255), gen.integers(0, 255), gen.integers(0, 255)),
        )

    img.save(filename, format="webp")
    IMG_STACK_PROGRESS.remove(id)


def generate_img_thread(id):
    img_id = "background" + str(id) + ".webp"
    f = threading.Thread(
        target=generate_img, args=(img_id, "static/imgs/", id), daemon=True
    )
    f.start()


def generate_img_init(no):
    global IMG_STACK
    for i in range(0, no):
        generate_img("background" + str(i) + ".webp", "static/imgs/", i)
        IMG_STACK.append(i)


def remove_images():
    global IMG_STACK
    img_id = np.random.default_rng(int(time.perf_counter_ns())).integers(
        0, IMG_STACK.__len__()
    )
    if not (img_id in IMG_STACK_PROGRESS):
        generate_img_thread(img_id)
    return img_id


generate_img_init(int(os.environ["IMAGES_COUNT"]))


print("Server started.. 👍")


@app.route("/")
def response():
    global CERTIFICATE_LIST

    img_id = "static/imgs/background" + str(remove_images()) + ".webp"
    if not os.path.exists(img_id):
        img_id = "static/imgs/background.webp"

    return render_template("./index.html", img_id=img_id, cert_data=CERTIFICATE_LIST)

