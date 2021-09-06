from typing import Dict, Set
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt 
import requests
import xlsxwriter
import numpy as np


#world = requests.get("https://ebird.org/region/world?yr=all").text
#rajasthan2021 = requests.get("https://ebird.org/region/IN-RJ?yr=all").text
#udaipur = requests.get("https://ebird.org/region/IN-RJ-UD?yr=all&m=&rank=mrec").text
#netherland2021 = requests.get("https://ebird.org/region/NL?yr=cur&m=&rank=mrec").text
#netherland2020 = requests.get("https://ebird.org/region/NL?yr=BIGDAY_2020a").text
#netherland2019 = requests.get("https://ebird.org/region/NL?yr=BIGDAY_2019b").text
#netherland2018 = requests.get("https://ebird.org/region/NL?yr=BIGDAY_2018b").text
#netherland2017 = requests.get("https://ebird.org/region/NL?yr=BIGDAY_2017a").text

def make_xlsx_file():
    workbook = xlsxwriter.Workbook("Book 2.xlsx")
    worksheet = workbook.add_worksheet("Udaipur Bird Data")

    worksheet.write("A1","Name of Birds")
    worksheet.write("B1","Bird Count")

    #dic_of_birds["name"].reverse()
    #dic_of_birds["count"].reverse()

    #for x in range(0,len(bd_name)):
     #   worksheet.write(x, 0, bd_name[x])
      #  worksheet.write(x, 1, bd_count[x])

    workbook.close()

class Graph_Maker():
    def __init__(self,html_object,title:str,xlable:str,ylable:str):
        self.soup_content = BeautifulSoup(html_object)
        self.tag = self.soup_content.body
        self.title = title
        self.xlable = xlable
        self.ylable = ylable
        
    def get_bird_name_object(self):
        all_span_object_list = self.tag.find_all("span",attrs={"class":"Heading-main"})
        list_of_objects = list(all_span_object_list) #convert to python list
        return list_of_objects

    def get_bird_count_object(self):
        all_span_object_list = self.tag.find_all("span",attrs={"class":"Observation-meta-count-label Color-text-neutral-4"}) 
        list_of_objects = list(all_span_object_list) 
        return list_of_objects
    
    def get_bird_location_object(self):
        all_span_object_list = self.tag.find_all("span",attrs={"class":"Observation-meta-location-label"}) 
        list_of_objects = list(all_span_object_list) 
        all_span_object_list2 = self.tag.find_all("a",attrs={"class":"Observation-meta-location-label"}) 
        list_of_objects = list(all_span_object_list) 
        list_of_objects.extend(all_span_object_list2)
        return list_of_objects
    
    def get_bird_count(self):
        bird_count = []
    
        list_of_object = self.get_bird_count_object()
        for x in range(0,len(list_of_object)):
            bird_count.append(list_of_object[x].string)
        for y in range(0,len(bird_count)):
            a = str(bird_count[y])
            bird_count[y] = a.replace("\n\t\t\t\t\t\t\t\t\t\t","")
        return bird_count

    def get_bird_name(self):
        bird_name = []
        list_object = self.get_bird_name_object()
        for x in range(0,len(list_object)):
            bird_name.append(str(list_object[x].string))

        bird_name.pop(0)
        bird_name.pop(len(bird_name)-1)
    
        return bird_name
    
    def get_bird_location(self):
        bird_location = []
        list_object = self.get_bird_location_object()
        for x in range(0,len(list_object)):
            bird_location.append(str(list_object[x].string))
        return bird_location
    
    def get_dic_of_birds(self):
        udaipur_birds = {}
        for x in range(0,len(self.get_bird_name())):
            udaipur_birds[str(self.get_bird_name()[x])] = []
            a = udaipur_birds[str(self.get_bird_name()[x])]
            a.append(self.get_bird_count()[x]) 
        return udaipur_birds

    def arrenge_data(self):
        b = self.get_bird_name()
        a = self.get_bird_count()
        l = self.get_bird_location()
        b.append("n")
        a.append("0") 
        l.extend(["l","n","n","n","n"])
        
        g = []
        c = []
        d = []
        for x in range(0,len(a)):
            for y in range(0,len(a)):
                if a[y] == str(x):
                    c.append(a[y])
                    d.append(b[y])
                    g.append(l[y])
        return {"count":c,"name":d,"location":g}

    def make_plot(self):
        data_to_plot = self.arrenge_data()
        plt.barh(data_to_plot["name"],data_to_plot["count"])
        plt.title(self.title)
        plt.xlabel(self.xlable)
        plt.ylabel(self.ylable)
        plt.show()

#Need Dynamically Work In Progress
def Make_Compaire_Graph():
    netherland2021_graph = Graph_Maker("netherland2021","2021 chart","Bird Name","Bird Count")
    data_2021 = netherland2021_graph.arrenge_data()
    netherland2020_graph = Graph_Maker("netherland2020","2020 chart","Bird Name","Bird Count")
    data_2020 = netherland2020_graph.arrenge_data()
    netherland2019_graph = Graph_Maker("netherland2019","2019 chart","Bird Name","Bird Count")
    data_2019 = netherland2019_graph.arrenge_data()
    netherland2018_graph = Graph_Maker("netherland2018","2018 chart","Bird Name","Bird Count")
    data_2018 = netherland2018_graph.arrenge_data()
    netherland2017_graph = Graph_Maker("netherland2017","2017 chart","Bird Name","Bird Count")
    data_2017 = netherland2017_graph.arrenge_data()

    dic_of_all_value = {}
    a = ""
    for x in range(0,len(data_2021)):
        a = set(data_2021["name"])
    for x in range(0,len(data_2020)):
        a.update(data_2020["name"])
    for x in range(0,len(data_2019)):
        a.update(data_2019["name"])
    for x in range(0,len(data_2018)):
        a.update(data_2018["name"])
    for x in range(0,len(data_2017)):
        a.update(data_2017["name"])
    list_of_keys = list(a)
    
    
    for x in range(0,len(list_of_keys)):
        for y in range(0,len(data_2021["name"])):
            if list_of_keys[x] == data_2021["name"][y]:
                dic_of_all_value[list_of_keys[x]] = ["0","0","0","0","0"]
                a = dic_of_all_value[list_of_keys[x]]
                a[4] = data_2021["count"][y]
        for y in range(0,len(data_2020["name"])):
            if list_of_keys[x] == data_2020["name"][y]:
                if data_2020["name"][y] not in dic_of_all_value.keys():
                    dic_of_all_value[list_of_keys[x]] = ["0","0","0","0","0"]
                    a = dic_of_all_value[list_of_keys[x]]
                    a[3] = data_2020["count"][y]
                if data_2020["name"][y] in dic_of_all_value.keys():
                    a = dic_of_all_value[list_of_keys[x]]
                    a[3] = data_2020["count"][y]
        for y in range(0,len(data_2019["name"])):
            if list_of_keys[x] == data_2019["name"][y]:
                if data_2019["name"][y] not in dic_of_all_value.keys():
                    dic_of_all_value[list_of_keys[x]] = ["0","0","0","0","0"]
                    a = dic_of_all_value[list_of_keys[x]]
                    a[2] = data_2019["count"][y]
                if data_2019["name"][y] in dic_of_all_value.keys():
                    a = dic_of_all_value[list_of_keys[x]]
                    a[2] = data_2019["count"][y]
        for y in range(0,len(data_2018["name"])):
            if list_of_keys[x] == data_2018["name"][y]:
                if data_2018["name"][y] not in dic_of_all_value.keys():
                    dic_of_all_value[list_of_keys[x]] = ["0","0","0","0","0"]
                    a = dic_of_all_value[list_of_keys[x]]
                    a[1] = data_2018["count"][y]
                if data_2018["name"][y] in dic_of_all_value.keys():
                    a = dic_of_all_value[list_of_keys[x]]
                    a[1] = data_2018["count"][y]
        for y in range(0,len(data_2017["name"])):
            if list_of_keys[x] == data_2017["name"][y]:
                if data_2017["name"][y] not in dic_of_all_value.keys():
                    dic_of_all_value[list_of_keys[x]] = ["0","0","0","0","0"]
                    a = dic_of_all_value[list_of_keys[x]]
                    a[0] = data_2017["count"][y]
                if data_2017["name"][y] in dic_of_all_value.keys():
                    a = dic_of_all_value[list_of_keys[x]]
                    a[0] = data_2017["count"][y]

    b = dic_of_all_value["Gadwall"]

    for x in range(0,len(b)):
        b[x] = int(b[x])

    plt.bar(["2017","2018","2019","2020","2021"],b)
    plt.title("Gadwall")
    plt.show()


class Single_Geolocation():
    def __init__(self,url:str,html_tag_list:list,data_key:list):
        self.response = url
        self.tag_list = html_tag_list
        
        self.dic_key_list = data_key
    def get_html_response(self):
        response = requests.get(self.response).text
        return response
    def get_finded_tags(self):
        response = self.get_html_response()
        soup = BeautifulSoup(response)
        html_body = soup.body
        all_tag_list_dic = {}
        for x in range(0,len(self.tag_list)):
            all_tag_list_dic[str(self.dic_key_list[x])] = html_body.find_all(str(self.tag_list[x]))
        return all_tag_list_dic


#dica = Single_Geolocation("https://www.latlong.net/category/cities-102-15.html",["a","td"],["location Name","location corrdinate"])
#a = dica.get_finded_tags()
#print(a)

#Indian = Graph_Maker(rajasthan2021,"Indian Bird","Bird Name","Bird Count")
#bird_dic = Indian.arrenge_data()

#data = requests.get("https://restcountries.eu/rest/v2/all")
#list_data = data.json()

#code = []
#for x in range(0,len(list_data)):
 #   code.append(list_data[x]["alpha2Code"])








