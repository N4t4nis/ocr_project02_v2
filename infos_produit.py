from pprint import pprint
import requests
from bs4 import BeautifulSoup



url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
recup_all_info=[]

def infos_produits(url):
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.text, 'html.parser')
    titre = soup.find('h1')
    scrap_image_url = soup.find("div", {"class":"item active"}).find("img")
    image_url = "http://books.toscrape.com" + scrap_image_url.get("src")[5:]
    alt_image = scrap_image_url.get("alt")
    info_table = [info.text for info in soup.find("table", {"class": "table-striped"}).findAll("td")]
    description = soup.findAll("p")[3]
    category = soup.findAll("a")[3]

    table_list = []
    for info in info_table:
        table_list.append(info)
    recup_all_info.append([url, table_list[0],
                           titre.text,
                           table_list[2][1:],
                           table_list[3][1:],
                           table_list[5],
                           description.text,
                           category.text,
                           image_url + ' Tag: ' + alt_image,
                           table_list[6]])

    return recup_all_info

csv_columns = ['product_page_url', 'universal_ product_code (upc)', 'title', 'price_including_tax',
'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']

infos_produits(url)
for info in recup_all_info:
    pprint(info)





"""with open('info_produit.csv', 'w', encoding="utf-8", newline='') as csv_file:
    write = csv.writer(csv_file)
    write.writerow(csv_columns)
    for info in recup_all_info:
        write.writerow(info)"""






# with open('info_produit.csv', 'w') as csv_file:
#     writer = csv.DictWriter(csv_file, delimiter=' ', fieldnames=csv_columns)
#     writer.writeheader()
#     for data in recup_all_info:
#         writer.writerow(data)
#


# """with open('info_produit.csv', 'w') as csv_file:
# for key in dict.keys():
# csv_file.write("{}, {}\n".format(key, dict[key]))"""
#
#
#
#
# dict= [{"product_page_url": url},
# {"universal_ product_code (upc)": table_list[0]},
# {"title": titre.text},
# {"price_including_tax": table_list[2]},
# {"price_excluding_tax": table_list[3]},
# {"number_available": table_list[5]},
# {"product_description": description.text},
# {"category": category.text},
# {"image_url": image_url + ' Tag: ' + alt_image},
# {"review_rating": table_list[6]},
#
# ]
#
# recup_all_info.append({
#                        "product_page_url": url,
#                        "universal_ product_code (upc)": table_list[0],
#                        "title": titre.text,
#                        "price_including_tax": table_list[2],
#                        "price_excluding_tax": table_list[3],
#                        "number_available": table_list[5],
#                        "product_description": description.text,
#                        "category": category.text,
#                        "image_url": image_url + ' Tag: ' + alt_image,
#                        "review_rating": table_list[6]
#                        })