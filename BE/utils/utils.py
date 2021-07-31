import base64
import cv2
import os
import shutil


def resize_img(img_dir, height=1, width=1, s_h=0, s_w=0, save=False):
    img = cv2.imread(img_dir)
    h, w, _ = img.shape
    img = img[int(h * s_h):int(h * height), int(w * s_w):int(w * width)]
    if save:
        cv2.imwrite(img_dir, img)
    return img


# s_h: Start height
# s_w: Start width
def get_base64_image_from_dir(img_dir, height=1, width=1, s_h=0, s_w=0):
    img = resize_img(img_dir, height=1, width=1, s_h=0, s_w=0)
    encoded_string = base64.b64encode(cv2.imencode('.jpg', img)[1])
    return encoded_string


def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


def remove_folder(dir_name):
    if os.path.exists(dir_name):
        shutil.rmtree(dir_name, ignore_errors=True)
