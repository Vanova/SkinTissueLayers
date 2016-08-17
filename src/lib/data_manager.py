import urllib


def fetch_image(url, save_name):
    urllib.urlretrieve(url, save_name)


def url2name(url):
    chunks = url.split("/")
    return chunks[-1]
