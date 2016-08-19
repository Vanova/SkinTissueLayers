import urllib
from PIL import Image
import numpy as np
from collections import Counter


def fetch_image(url, save_name):
    urllib.urlretrieve(url, save_name)


def url2name(url):
    chunks = url.split("/")
    return chunks[-1]


def image2array(img, channel=3):
    """
    Isolate the nth channel from the image.
       n = 0: red, 1: green, 2: blue, 3: gray
    """
    if channel == 3:
        gray_img = img.convert('L')
        a = np.asarray(gray_img.getdata(), dtype=np.uint8).reshape(img.size)
    else:
        a = np.array(img)
        a = a[:, :, channel]

    return a / 256.


def array2image(arr, channel=3):
    """
    Isolate the nth channel from the image.
       n = 0: red, 1: green, 2: blue, 3: gray
    """
    if channel == 3:
        arr = np.asarray(arr * 255, dtype=np.uint8)
        im = Image.fromarray(arr, mode='L')
    else:
        w, h = arr.shape
        rgb = np.zeros((w, h, 3), 'uint8')
        rgb[:, :, channel] = arr * 256
        im = Image.fromarray(rgb)
    return im


def split_data(data, ratio):
    pass


def labels_distribution(labels):
    return Counter(labels)