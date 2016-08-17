import csv
import lib.data_manager as dm

IMAGE_URLS = "data/img_urls.csv"
IMAGE_SAVE_PATH = "data/images/"

### parse xml meta data
# TODO refactor and add later

### fetch the images
# parse image urls and labels
number_samples = 10
url_label = []
with open(IMAGE_URLS) as f:
    cf = csv.reader(f)
    for row in cf:
        url = row[1]
        label = row[3]
        url_label.append((url, label))

# load images
for smp in url_label[:number_samples]:
    dm.fetch_image(smp[0], IMAGE_SAVE_PATH + dm.url2name(smp[0]))

# save name and labels to csv
with open(IMAGE_SAVE_PATH + "name_lab.csv",'w') as out:
    csv_out=csv.writer(out)
    for row in url_label[:number_samples]:
        url = row[0]
        lab = row[1]
        csv_out.writerow((dm.url2name(url), lab))

