import requests
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path

tete_rousse_url = "https://caf.requea.com/rqdbs?dbId=850706c76b69cf56016b7891f8383693"
gouter_url = "https://caf.requea.com/rqdbs?dbId=850706c76b093896016b094adfd138e4"
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
    name = datetime.today().strftime('%Y-%m-%d--%H:%M:%S') # set image name to current date

    if subdirs is not None:
        path = "./" + "/".join(subdirs)
        Path(path).mkdir(parents=True, exist_ok=True)
        name = path + "/" + name
        # print(name)

    with open(name + ".jpg", "wb+") as img_file:
        img_file.write(img_data)

# because local names might differ and I don't want to have separate, say, "january" and "styczeń" directories
num2month = {
    1:"january", 2:"february", 3:"march", 4:"april", 5:"may", 6:"june", 7:"july", 8:"august", 9:"september", 10:"october", 11:"november", 12:"december"
}

if __name__ == "__main__":
    month_name = num2month[datetime.now().month]
    tete_rousse_img_url = get_img_url(tete_rousse_url, tete_rousse_img_id)
    gouter_img_url = get_img_url(gouter_url, gouter_img_id)
    save_img(tete_rousse_img_url, ["tete_rousse", month_name])
    save_img(gouter_img_url, ["gouter", month_name])

# useful:
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
# https://docs.python.org/3/library/pathlib.html#pathlib.Path.mkdir