import requests
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize


def find_url():
    """this function finds all the url of the news and makes excle"""

    current_page = "https://www.ynet.co.il/home/0,7340,L-4269-116-429-201900-1,00.html"
    lnk_lst = []

    for i in range(15):
        print("page: " , i)
        main_page = requests.get(current_page)
        webpage_html = main_page.text
        soup = BeautifulSoup(webpage_html, 'html.parser')

        all_links = soup.find_all( class_ = "smallheader" )
        for element in all_links:
            lnk_lst.append("https://www.ynet.co.il/"+(element.get("href")))

        next_page_href = soup.find_all('td', text = re.compile('לעמוד הבא'))
        current_page = "https://www.ynet.co.il/"+(str(next_page_href)[39:83])
        print(current_page)

    dict = {}
    dict["url"] = lnk_lst
    df = pd.DataFrame(dict)
    df.to_excel("./url.xlsx")

def find_city():

    city_and_url_dict = {}

    df = pd.read_excel('url.xlsx')
    lst_of_url = df["url"].tolist()

    for url in lst_of_url: ##go on all link
        print(url)
        main_page = requests.get(url)
        webpage_html = main_page.text
        soup = BeautifulSoup(webpage_html, 'html.parser')

        header = soup.find_all( class_ = "art_header_title" )
        print(header)

        ##if we check all the text in page !!
        # for p in soup.find_all("p"):
        #     current_text = p.text
        #     df = pd.read_excel('city_table.xlsx')
        #     list_of_city = df["city"].tolist()
            # print(list_of_city)
        # for city in list_of_city:
        #     if city in current_text:
        #         if city not in city_and_url_dict:
        #             city_and_url_dict[city] = [url]
        #         else:
        #             city_and_url_dict[city].append(url)


        ##if we check only the header !!
        df = pd.read_excel('city_table.xlsx')
        list_of_city = df["city"].tolist()
        for city in list_of_city:
            if len(list(city.split(" "))) > 1:
                if city in str(header):
                    if city not in city_and_url_dict:
                        city_and_url_dict[city] = [url]
                    else:
                        city_and_url_dict[city].append(url)
            else:
                if city in str(header).split() or city in nltk.word_tokenize(str(header)) or ("מ" + str(city)) in str(header).split() or ("ל" + str(city)) in str(header).split() or ("ש" + str(city)) in str(header).split() or ("ב" + str(city)) in str(header).split() or ("ו" + str(city)) in str(header).split():
                    print("found city: ", city)
                    if city not in city_and_url_dict:
                        city_and_url_dict[city] = [url]
                    else:
                        city_and_url_dict[city].append(url)
        print(city_and_url_dict)

    print(city_and_url_dict)
    with open('url_dict.json', 'w') as f:
        json.dump(city_and_url_dict, f, indent=2)
        print("New json file is created from data.json file")

    dict_count = {}
    for key, val in city_and_url_dict.items():
        dict_count[key] = len(val)
    print(dict_count)

    key = dict_count.keys()
    values= dict_count.values()

    df = pd.DataFrame({"city":key, "number of url": values})
    df.to_excel("number of url.xlsx", index=False)

if __name__ == '__main__':
    find_url()
    find_city()


