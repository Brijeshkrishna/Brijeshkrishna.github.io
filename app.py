from flask import Flask, render_template
import threading
from PIL import Image
import numpy as np
import json
from tqdm import tqdm
import requests
import time
import dotenv
import os

dotenv.load_dotenv()

app = Flask(__name__, template_folder="template", static_folder="static")


global img_stack
global img_stack_progress
global repos_list
global requests_ss
global certificate_list


def get_certificate():
    with open("cert.json", "r") as f:
        return f.read()


repos_list = []
img_stack = []
img_stack_progress = []
requests_ss = requests.Session()
certificate_list=json.loads(get_certificate())




def generate_img(filename="background.webp", dir="./", id=None, width=2400, height=1350):

    global img_stack_progress
    img_stack_progress.append(id)
    filename = dir + filename

    gen = np.random.default_rng(int(time.perf_counter_ns()))
    img = Image.new(
        "RGB",
        (width, height),
        (gen.integers(0, 255), gen.integers(0, 255), gen.integers(0, 255)),
    )
    # img = Image.new(
    #     "RGB",
    #     (width, height),
    #     (30, 30,32),
    # )

    for _ in tqdm(
        range(0, gen.integers(0, height) * gen.integers(0, width)),
        desc=f"Generating Image... [{id}]",
        leave=1
     
    ):
        img.putpixel(
            (gen.integers(0, width - 1), gen.integers(0, height - 1)),
            (gen.integers(0, 255), gen.integers(0, 255), gen.integers(0, 255)),
        )

    img.save(filename, format="webp")
    img_stack_progress.remove(id)




def generate_img_thread(id):
    img_id = "background" + str(id) + ".webp"
    f = threading.Thread(target=generate_img, args=(img_id, "static/imgs/", id))
    f.start()


def generate_img_init(no):
    global img_stack
    for i in range(0, no):
        generate_img( "background" + str(i) + ".webp","static/imgs/",i)
        img_stack.append(i)


def remove_images():
    global img_stack
    img_id = np.random.default_rng(int(time.perf_counter_ns())).integers(0, img_stack.__len__())
   

    if not (img_id in img_stack_progress):
        generate_img_thread(img_id)

    return img_id



print("Running")
generate_img_init(int(os.environ['IMAGES_COUNT']))
print("Running")




@app.route("/")
def response():
    global certificate_list

    img_id = "static/imgs/background" + str(remove_images()) + ".webp"

    return render_template(
        "./index.html",
        img_id=img_id,
        cert_data=certificate_list)


# import requests



# def get_repos(requests_session: requests.Session, repos_list):
#     for items in requests_session.get(
#         "https://api.github.com/users/brijeshkrishna/repos"
#     ).json():
#         if items not in repos_list:
#             repos_list.append(items['name'])


#     return repos_list