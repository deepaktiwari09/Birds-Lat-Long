from flask import Flask
from flask_sqlalchemy import SQLAlchemy,request
import requests
import calendar as cd


app = Flask(__name__)

app.config["SECRET_KEY"] = "asdfghjkl"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.db"

db = SQLAlchemy(app)

class Bird_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bird_name_col = db.Column(db.String(128),nullable=False)
    bird_country_col = db.Column(db.String(32),nullable=False)
    bird_location_col = db.Column(db.String(1024),nullable=False)
    bird_latitude_col = db.Column(db.String(256),nullable=True)
    bird_longitude_col = db.Column(db.String(256),nullable=True)


def add_Data_to_Bird_Table(bird_name,country,location,latitude,longitude):
    object = Bird_table(
        bird_name_col = bird_name,
        bird_country_col = country,
        bird_location_col = location,
        bird_latitude_col = latitude,
        bird_longitude_col = longitude
    )
    db.session.add(object)
    db.session.commit()
    print("data added")
    
def change_country():
    object = Bird_table.query.filter_by(bird_country_col="NLD").all()
    for x in range(0,len(object)):
        object[x].bird_country_col  = "IND"
        db.session.commit()
        print(str(len(object))+" of  " +str(x))

def bird_data_by_Code_and_locaion(code:str,location:str):
    data_to_send = {}
    object = Bird_table.query.filter_by(bird_country_col=code).all()
    if object != None:
        for x in range(0,len(object)):
            if object[x].bird_location_col.find(location) != -1:
                data_to_send[str(object[x].bird_name_col)] = {}
                a =  data_to_send[object[x].bird_name_col]
                a["location"] = str(object[x].bird_location_col)
                a["latitude"] = str(object[x].bird_latitude_col)
                a["longitude"] = str(object[x].bird_longitude_col)
                print("data Searched " + str(len(object)) + " data selected " + str(x))
            if object[x].bird_location_col.find(location) == -1:
                continue
        return data_to_send
    if object == None:
        data_to_send["bird_name"] = {"location":"No Data","latitude":"0","longitude":"0"}
        return data_to_send

def bird_data_by_Code(Code:str):
    data_to_send = {}
    object = Bird_table.query.filter_by(bird_country_col=Code).all()
    if object != None:
        for x in range(0,len(object)):
            data_to_send[object[x].bird_name_col] = {}
            a = data_to_send[object[x].bird_name_col]
            a["location"] = object[x].bird_name_col
            a["latitude"] = object[x].bird_latitude_col
            a["longitude"] = object[x].bird_longitude_col
            print("data Searched " + str(len(object))+ " data selected "+ str(x) )
        return data_to_send
    if object == None:
        return data_to_send

def add_to_database(): 
    january_data = []
    conty_code = ["IN"]
    conty_name = ["India"]
    list_data = []
    
    '''data = requests.get("https://restcountries.eu/rest/v2/all")
    list_data = data.json()
    for index in range(0,len(list_data)): 
            conty_code.append(list_data[index]["alpha2Code"])
            conty_name.append(list_data[index]["name"])'''
    
    for contry_code_index in range(0,len(conty_code)):
        print("Now: "+str(conty_name[contry_code_index]))
        for y in range(1,13):
            month_data = cd.monthrange(2020, y) # 5 month 7 days Complited
            dayes = month_data[1] 
            for x in range(1,dayes+1):
                january_date_data = requests.get("https://api.ebird.org/v2/data/obs/" + str(conty_code[contry_code_index])  + "/historic/2020/1/" + str(x),headers={"X-eBirdApiToken": "l54b0ne8lvjb"})
                data = january_date_data.json()
                print("Month "+ str(y) +" Date: " + str(x))
                print("total data found " + str(len(data)))
                for index in range(0,len(data)):
                    print("Month "+ str(y) +" Date: " + str(x) + " Entry Number " + str(index))
                    add_Data_to_Bird_Table(
                        bird_name = data[index]["comName"],
                        country = "IND",
                        location = data[index]["locName"],
                        latitude = data[index]["lat"],
                        longitude = data[index]["lng"]
                        )

def bird_data_by_latlong(lat:str,long:str):
    data_to_send = {}
    list_data = []
    object = Bird_table.query.all()
    if object != None:
        for x in range(0,len(object)):
            if object[x].bird_longitude_col.find(long) != -1 or object[x].bird_latitude_col.find(lat) != -1:
                list_data.append(object[x].bird_name_col) 
                print("Total Data: " + str(len(object))+" Matched Data: "+str(x))
            if object[x].bird_longitude_col.find(long) == -1 or object[x].bird_latitude_col.find(lat) == -1:
                continue
        data_to_send["Birds Name"] = list_data
        return data_to_send
    if object == None:
        return data_to_send

def bird_data_by_bird_name(bird_name:str):
    data_to_send = {}
    list_of_data = []
    object = Bird_table.query.filter_by(bird_name_col=bird_name).all()
    if object != None:
        for x in range(0,len(object)):
            a = {}
            a["location"] = object[x].bird_location_col
            a["latitude"] = object[x].bird_latitude_col
            a["longitude"] = object[x].bird_longitude_col
            list_of_data.append(a)
            
        data_to_send["Bird Location Details"] = list_of_data
        return data_to_send
    if object == None:
        data_to_send["Bird Location Deatils"] = list_of_data
        return data_to_send

def bird_data_all():
    data_to_send = {}
    list_of_data =[]
    object = Bird_table.query.all()
    for x in range(0,len(object)):
        list_of_data.append(object[x].bird_name_col)
    data_to_send["Bird Name"] = list_of_data
    return data_to_send
        
@app.route("/api/bird-name/country-code/<Code>/<location>")
def bird_data_by_Code_and_locaion_view(Code,location):
    data = bird_data_by_Code_and_locaion(Code," "+str(location).capitalize())    
    return data

@app.route("/api/bird-name/country-code/<Code>")
def bird_data_by_Code_view(Code):
    data = bird_data_by_Code(Code)
    return data
    
@app.route("/api/bird-name/lat.-long./<Lat>/<Long>")
def bird_data_by_latlong_view(Lat,Long):
    data = bird_data_by_latlong(Lat,Long)
    return data

@app.route("/api/bird-name/<bird_name>")
def bird_data_by_bird_name_view(bird_name):
    data = bird_data_by_bird_name(bird_name)
    return data

@app.route("/api/bird-name")
def bird_data_all_view():
    data = bird_data_all()
    return data


if __name__=="__main__":
    db.create_all()
    app.run()
    





 