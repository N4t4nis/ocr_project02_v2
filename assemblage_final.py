# Script permettant de scraper tout le site booktoscrap.com et d'en exporter les 50 catégories dans
# un fichier csv différent pour chaque catégorie et de télécharger toutes les images de chaque produit dans un seul fichier.
import csv
import requests
from bs4 import BeautifulSoup
from pprint import pprint



def all_category():
    url = 'http://books.toscrape.com'
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, "html.parser")
    i = 0
    url_category= soup.find('ul', {'class':'nav nav-list'}).findAll("a")
    for url in url_category:
        if i != 0 and i < 6:
            list_all_category.append("http://books.toscrape.com/" + url.get("href"))
        i += 1
    return list_all_category

def scrap_1_category(category):
    reponse_lien_category = requests.get(category)
    soup = BeautifulSoup(reponse_lien_category.text, "html.parser")
    # récup liens produit (page1)
    product_url = soup.findAll("h3")
    for urls in product_url:
        a = urls.find("a")
        liens = a["href"][9:]

        liens_produits.append("http://books.toscrape.com/catalogue/" + liens)
    # while soup.find("li", {"class":"next"}) is not None:
    #     # recupère le bouton next de chaque page
    #     bouton_next= soup.find("li", {"class":"next"}).find("a").get("href")
    #     url_bouton_next = lien_category[:-10] + bouton_next
    #     # entre dans le bouton next (page suivante)
    #     reponse_page2= requests.get(url_bouton_next)
    #     soup = BeautifulSoup(reponse_page2.text, 'html.parser')
    #     # récup le reste des liens produits (page 2, 3 ...)
    #     product_url = soup.findAll("h3")
    #     for urls in product_url:
    #         a = urls.find("a")
    #         liens = a["href"][9:]
    #         liens_produits.append("http://books.toscrape.com/catalogue/" + liens)
    return liens_produits

def infos_produits(lien):
    reponse_lien_prod = requests.get(lien)
    soup = BeautifulSoup(reponse_lien_prod.text, "html.parser")
    # global titre
    # global scrap_image_url
    # global image_url
    titre = soup.find('h1')
    scrap_image_url = soup.find("div", {"class":"item active"}).find("img")
    image_url = "http://books.toscrape.com" + scrap_image_url.get("src")[5:]
    alt_image = scrap_image_url.get("alt")
    info_table = [info.text for info in soup.find("table", {"class": "table-striped"}).findAll("td")]
    #récupere uniquement la 4ème balise "p" et "a"
    description = soup.findAll("p")[3]
    category = soup.findAll("a")[3]

    table_list = []
    for info in info_table:
        table_list.append(info)
    recup_all_info = [lien, table_list[0],
                           titre.text,
                           table_list[2][1:],
                           table_list[3][1:],
                           table_list[5],
                           description.text,
                           category.text,
                           table_list[6],
                           image_url + ' Tag: ' + alt_image]

    return recup_all_info


def csv_category(category):
    liste = scrap_1_category(category)
    nom = category[51:-11]
    dossier = 'C:/Users/N4t4nistorus/Documents/ocr_parcours/ocr_project02/csv_category/'
    with open(dossier + nom + '.csv', 'w', encoding="utf-8", newline='') as csv_file:
        write = csv.writer(csv_file)
        write.writerow(csv_columns)
        #REUSSIR a lui dire = pour 1 seule chatégorie, tu écrit tout les infos produits, puis retour boucle

        for lien in liste:
            infos = infos_produits(lien)
            write.writerow(infos)
            pass
    return liste


list_all_category = []
liens_produits = []

csv_columns = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

for category in all_category():
    csv_objet = csv_category(category)
    pprint(len(csv_objet))
    liens_produits.clear()







# for lien_prod in liens_produits:
#     reponse_lien_prod = requests.get(lien_prod)
#     soup = BeautifulSoup(reponse_lien_prod.text, "html.parser")
#     infos_produits(lien_prod)
# csv_category(lien_category)
    # télécharge toutes les images dans un dossier, avec leurs nom
    # dossier = b'C:/Users/N4t4nistorus/Documents/ocr_parcours/ocr_project02/images_download/' + str.encode(titre.text) + b'.jpg'
    # r = requests.get(image_url, stream=True)
    # with open(dossier, "wb") as jpg_test:
    #     write = jpg_test.write(r.content)
    #     pprint(titre.text)




#
# pprint(list_all_category)
# pprint(len(liens_produits))
# pprint(recup_all_info)

# for lien_category in list_all_category:
#     nom = lien_category[51:-11]
#     dossier = 'C:/Users/N4t4nistorus/Documents/ocr_parcours/ocr_project02/csv_category/'
#     with open(dossier + nom + '.csv', 'w', encoding="utf-8", newline='') as csv_file:
#         write = csv.writer(csv_file)
#         write.writerow(csv_columns)
#         #REUSSIR a lui dire = pour 1 seule chatégorie, tu écrit tout les infos produits, puis retour boucle
#         for lien_prod in liens_produits:
#             reponse_lien_prod = requests.get(lien_prod)
#             soup = BeautifulSoup(reponse_lien_prod.text, "html.parser")
#         for info in infos_produits():
#             write.writerow(info)






#récup les infos produits de toute la catégorie
# for lien in liens_produits:
#     reponse_lien = requests.get(lien)
#     soup = BeautifulSoup(reponse_lien.text, 'html.parser')
#     infos_produits()
#
# pprint(recup_all_info)