import requests
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
import pytz

tz = pytz.timezone('CET') # central european timezone

tete_rousse_url = "https://caf.requea.com/rqdbs?dbId=850706c76b69cf56016b7891f8383693"
gouter_url = "https://caf.requea.com/rqdbs?dbId=850706c76b093896016b094adfd138e4"

gouter_old_img_id = "rqdshb3cd0a3b775dbe6c01775dbfaeea3b47"
gouter_img_id = "rqdshb3cd0a3b775dbe6c01775dbfaee73b42"
tete_rousse_img_id = "rqdshb3cd0a3b775dbe6c01775dbfacce3ae8"

def get_img_url(website_url, img_id):
    """ Retrieves the URL of an image given its id. """
    html = requests.get(website_url) # get the html code of a website
    soup = BeautifulSoup(html.content, "html.parser")
    img_url = soup.find(id=img_id).get("src") # get the img url from a website
    # print(img_url)
    return img_url

def save_img(img_url, subdirs=None):
    """ Saves an image given its URL. """
    img_data = requests.get(img_url).content # get bytes of an image
    name = datetime.now(tz).strftime('%H') # set image name to current hour

    if subdirs is not None:
        path = "./" + "/".join(subdirs)
        Path(path).mkdir(parents=True, exist_ok=True)
        name = path + "/" + name
        # print(name)

    with open(name + ".jpg", "wb+") as img_file:
        img_file.write(img_data)

# because local names might differ and I don't want to have separate, say, "january" and "styczeń" directories
# num2month = {
#     1:"january", 2:"february", 3:"march", 4:"april", 5:"may", 6:"june", 7:"july", 8:"august", 9:"september", 10:"october", 11:"november", 12:"december"
# }
# I don't want that actually :((

if __name__ == "__main__":
    # https://docs.python.org/3/library/datetime.html#datetime.datetime
    year = str(datetime.now(tz).year)
    month = str(datetime.now(tz).month)
    day = str(datetime.now(tz).day)

    img_urls = {}
    img_urls["tete_rousse"] = get_img_url(tete_rousse_url, tete_rousse_img_id)
    img_urls["gouter"] = get_img_url(gouter_url, gouter_img_id)
    img_urls["gouter_old"] = get_img_url(gouter_url, gouter_old_img_id)

    for name, url in img_urls.items():
        try:
            save_img(url, [name, year, month, day])
        except Exception: # in case the url is invalid (because, for example, the camera is broken)
            pass

    # save_img(tete_rousse_img_url, ["tete_rousse", year, month, day])
    # save_img(gouter_img_url, ["gouter", year, month, day])

# useful:
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
# https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir
