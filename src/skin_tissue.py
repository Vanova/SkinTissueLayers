import csv
import PIL
import gzip
from PIL import Image
import lib.data_manager as dm
import cPickle
import numpy as np
import random

IMAGE_URLS = "data/img_urls.csv"
IMAGE_SAVE_PATH = "data/images/"
FEATURES_PATH = "data/features/"

### parse xml meta data
# TODO refactor and add later

### fetch the images
# parse image urls and labels
url_labs = {}
with open(IMAGE_URLS) as f:
    cf = csv.reader(f)
    for row in cf:
        url = row[1]
        label = row[3].strip()
        if url in url_labs:
            print "[INFO] there is already such a link: " + url
        else:
            url_labs[url] = label

# load images
is_load = False
if is_load:
    number_samples = len(url_labs)
    for url in url_labs:
        dm.fetch_image(url, IMAGE_SAVE_PATH + dm.url2name(url))

    # save name and labels to csv
    with open(IMAGE_SAVE_PATH + "name_lab.csv", 'w') as out:
        csv_out = csv.writer(out)
        for url in url_labs:
            csv_out.writerow((dm.url2name(url), url_labs[url]))

### prepare datasets
# prepare labels
num_smp_thresh = 20
class_stat = dm.labels_distribution(url_labs.values())
thresh_class = dict((k, v) for k, v in class_stat.items() if v > num_smp_thresh)
classes = thresh_class.keys()
# filter url and labels list
thresh_labs = dict((k, v) for k, v in url_labs.items() if v in thresh_class.keys())
url_dig_labs = dict((k, classes.index(v)) for k, v in thresh_labs.items())

# scale images
resize = (512, 512)
data_set_pairs = []
i = 0
for u, l in url_dig_labs.items()[:10]:
    img = Image.open(IMAGE_SAVE_PATH + dm.url2name(u))
    img = img.resize(resize, PIL.Image.ANTIALIAS)
    arr_gray = dm.image2array(img, channel=3)
    img.close()
    # append (smp, label)
    data_set_pairs.append((np.reshape(arr_gray, resize[0] * resize[1]), l))
    i = i+1
    print str(i)

random.shuffle(data_set_pairs)
# split data
ratios = (60, 30, 10)
n = len(data_set_pairs)
n_train = (n * ratios[0]) // 100
n_test = (n * ratios[1]) // 100
n_val = n - n_train - n_test
train_pairs = data_set_pairs[:n_train]
test_pairs = data_set_pairs[n_train:n_train + n_test]
val_pairs = data_set_pairs[n_train + n_test:n_train + n_test + n_val]
# transform to tuple (smps_arr, lab_arr)
x = np.array(zip(*train_pairs)[0])
y = np.array(zip(*train_pairs)[1])
train_data = (x, y)
x = np.array(zip(*test_pairs)[0])
y = np.array(zip(*test_pairs)[1])
test_data = (x, y)
x = np.array(zip(*val_pairs)[0])
y = np.array(zip(*val_pairs)[1])
val_data = (x, y)

print("Saving expanded data. This may take a few minutes.")
f = gzip.open(FEATURES_PATH + "images_%d_%d.pkl.gz"%resize, "w")
cPickle.dump((train_data, val_data, test_data), f)
f.close()