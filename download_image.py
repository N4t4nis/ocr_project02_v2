import requests
from bs4 import BeautifulSoup



url = 'http://books.toscrape.com/catalogue/sharp-objects_997/index.html'
reponse = requests.get(url)
soup = BeautifulSoup(reponse.text, "html.parser")

titre = soup.find('h1')
scrap_image_url = soup.find("div", {"class" :"item active"}).find("img")
image_url = "http://books.toscrape.com" + scrap_image_url.get("src")[5:]
dossier = b'../../../Desktop/images_download/' + str.encode(titre.text) + b'.jpg'
r = requests.get(image_url, stream=True)

with open(dossier, "wb") as jpg_test:
    write = jpg_test.write(r.content)


print('\n', dossier)
print(r.headers.get('content-type'))
print(image_url)