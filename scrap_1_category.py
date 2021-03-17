import csv
import requests
from bs4 import BeautifulSoup
from pprint import pprint



def scrap_1_category(url):
    soup = BeautifulSoup(reponse.text, 'html.parser')
    while soup.find("li", {"class":"next"}) is not None:
        # récup liens produit (page1)
        product_url = soup.findAll("h3")
        for urls in product_url:
            a = urls.find("a")
            liens = a["href"][9:]
            liens_produits.append("http://books.toscrape.com/catalogue/" + liens)
        # recupère le bouton next de chaque page
        bouton_next= soup.find("li", {"class":"next"}).find("a").get("href")
        url_bouton_next = url[:-10] + bouton_next
        # entre dans le bouton next (page suivante)
        reponse_page2= requests.get(url_bouton_next)
        soup = BeautifulSoup(reponse_page2.text, 'html.parser')
        # récup le reste des liens produits (page 2, 3 ...)
        product_url = soup.findAll("h3")
        for urls in product_url:
            a = urls.find("a")
            liens = a["href"][9:]
            liens_produits.append("http://books.toscrape.com/catalogue/" + liens)
    return liens_produits

def infos_produits(lien):
    reponse_lien = requests.get(lien)
    soup = BeautifulSoup(reponse_lien.text, 'html.parser')
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
    recup_all_info.append([lien, table_list[0],
                           titre.text,
                           table_list[2][1:],
                           table_list[3][1:],
                           table_list[5],
                           description.text,
                           category.text,
                           table_list[6],
                           image_url + ' Tag: ' + alt_image])

    return recup_all_info


url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
reponse = requests.get(url)


liens_produits=[]
recup_all_info=[]




pprint(scrap_1_category(url))



#récup les infos produits de toute la catégorie
for lien in liens_produits:
    reponse_lien = requests.get(lien)
    soup = BeautifulSoup(reponse_lien.text, 'html.parser')
    infos_produits(lien)

pprint(recup_all_info)

csv_columns = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']



with open('produit_category.csv', 'w', encoding="utf-8", newline='') as csv_file:
    write = csv.writer(csv_file)
    write.writerow(csv_columns)
    for info in recup_all_info:
        write.writerow(info)




# # autre méthode pour écrire (trop de virgules)
# with open('produit_category.csv', 'w', encoding="utf-8") as csv_file:
#     write = csv.writer(csv_file, delimiter= " ")
#     for info in recup_all_info:
#         write.writerow(info)
#
#
# """for rec in recup_all_info:
# print(rec)"""
#
#
# with open('produit_category.csv', 'w', encoding="utf-8") as csv_file:
#     writer = csv.DictWriter(csv_file, delimiter=' ', fieldnames=csv_columns)
#     writer.writeheader()
#     for data in recup_all_info:
#         writer.writerow(data)