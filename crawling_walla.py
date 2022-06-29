import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize


def find_url():
    """this function finds all the url of the news and makes excle"""

    ######לשנות את החודש שעליו רצים
    current_page = "https://news.walla.co.il/archive/1?year=2019&month=1"
    lnk_lst = []
    city_and_url_dict = dict()

    num_page = 1

    for i in range(1, 6):
        print("page: " , i)
        main_page = requests.get(current_page)
        webpage_html = main_page.text
        soup = BeautifulSoup(webpage_html, 'html.parser')

        for li in soup.findAll('li'):
            for element in li:

                link = element.get("href")


                if "https://news.walla.co.il/item/" in str(link):
                   relevant_class = element.find_all(class_="css-19jbyn1")

                   for header in relevant_class:
                       header = header.find_all("h3")
                       print(header)

                       df = pd.read_excel('city_table.xlsx')
                       list_of_city = df["city"].tolist()

                       for city in list_of_city:
                           if len(list(city.split(" "))) > 1:
                               if city in str(header):
                                   print(link)
                                   print("found city: ", city)
                                   lnk_lst.append(link)
                                   if city not in city_and_url_dict:
                                       city_and_url_dict[city] = [link]
                                   else:
                                       city_and_url_dict[city].append(link)

                           else:
                               if city in nltk.word_tokenize(str(header)) or \
                                       ("מ" + str(city)) in nltk.word_tokenize(str(header)) or ("ל" + str(city)) in nltk.word_tokenize(str(header)) or ("ש" + str(city)) in str(header).split() or (
                                       "ב" + str(city)) in nltk.word_tokenize(str(header)) or ("ו" + str(city)) in nltk.word_tokenize(str(header)):
                                   print(link)
                                   print("found city: ", city)
                                   lnk_lst.append(link)

                                   if city not in city_and_url_dict:
                                       city_and_url_dict[city] = [link]
                                   else:
                                       city_and_url_dict[city].append(link)

        num_page +=1
        ######מספר העמודים באתר- לשנות את המספר פה
        current_page = "https://news.walla.co.il/archive/1?year=2019&month=1&page={}".format(num_page)

    print(city_and_url_dict)
    print(lnk_lst)

    dict_count = {}
    for key, val in city_and_url_dict.items():
        dict_count[key] = len(val)

    key = dict_count.keys()
    values= dict_count.values()

    df = pd.DataFrame({"city":key, "number of url": values})
    df.to_excel("number of url.xlsx", index=False)

    # dict = {}
    # dict["url"] = lnk_lst
    # df = pd.DataFrame(dict)
    # df.to_excel("./url.xlsx")

if __name__ == '__main__':
    find_url()
    # find_city()