import requests
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import math
import pandas as df

"""read city from excel"""
df = pd.read_excel('city_table.xlsx')
list_of_single_column = df["city"].tolist()
print(list_of_single_column)

# lst_city = []
# CITY="מג'דל שמס"
# response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyCqijMcVIo0-gK0oBeUEtLhFNIowMxHI-4'.format(CITY))
# resp_json_payload = response.json()
# lst_city.append(resp_json_payload['results'][0]['geometry']['location'])
# print(lst_city)

"""save the lan&lng of the city """
error_city = []
big_lst = []
for i in list_of_single_column:
    lst_city = []
    CITY = i
    lst_city.append(CITY)
    try:
        response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json?address={}&key=AIzaSyCqijMcVIo0-gK0oBeUEtLhFNIowMxHI-4'.format(
                CITY))
        resp_json_payload = response.json()
        lst_city.append(resp_json_payload['results'][0]['geometry']['location'])
        big_lst.append(lst_city)
        print(lst_city)
    except:
        error_city.append(CITY)
print(big_lst)

"""calculate euclidean distance"""
# big_lst=[["hadera", {'lat': 32.4340458, 'lng': 34.9196518}],["jerus", {'lat': 31.760922159468983, 'lng': 35.21021080409111}],["tel_aviv", {'lat': 32.08410859825, 'lng': 34.79062355059065}],["eilat", {'lat': 29.82286374199033, 'lng': 34.91377299115014}]]
len_lst = len(big_lst)
city_and_distance_lst = []
city1_lst = []
city2_lst = []
distance_lst = []
number = -1
for city_data in big_lst:
    number += 1
    if number == len_lst - 1:
        break
    main_city = city_data[0]
    px = city_data[1]["lat"]
    py = city_data[1]["lng"]
    for item in range(number + 1, len(big_lst)):
        city1_lst.append(main_city)
        city2 = big_lst[item][0]
        city2_lst.append(city2)
        qx = big_lst[item][1]["lat"]
        qy = big_lst[item][1]["lng"]
        e = math.dist([px, py], [qx, qy])
        distance_lst.append(e)
        city_and_distance_lst.append([main_city, city2, e])
# print(distance_lst)
# print([main_city, px, py], [city2, qx, qy],e)

"""convert data to excel"""
dict = {}
dict["city1"] = city1_lst
dict["city2"] = city2_lst
dict["distance"] = distance_lst
df = pd.DataFrame(dict)
df.to_excel("./distance.xlsx")
