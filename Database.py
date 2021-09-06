from IUCN_plot import db


class Bird_table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bird_name_col = db.Column(db.String(128),nullable=False)
    bird_count_col = db.Column(db.Integer,nullable=False)
    bird_location_col = db.Column(db.String(1024),nullable=False)
    bird_latitude_col = db.Column(db.String(256),nullable=True)
    bird_longitude_col = db.Column(db.String(256),nullable=True)

def add_data(bird_name:str,bird_count:int,bird_location:str):
    Bird_table(bird_name_col = bird_name,bird_count_col=bird_count,bird_location_col=bird_location)
    return {"Created":True}

def get_bird_data_by_location(location:str):
    object = Bird_table.quary.filter_by(bird_location_col=location).all()
    if object is None:
        return {"loc_not_found":True}
    if object !=  None:
        return {"data":object,"loc_not_found":False}

def make_json(location:str):
    dic_object = get_bird_data_by_location(location)
    bird_details = {}
    if dic_object["loc_not_found"] == True:
        return {"birds":{"bird_name":"not_found","bird_count":0}}
    if dic_object["loc_not_found"] == False:
        
        for x in range(0,len(dic_object["data"])):
            bird_details[str(dic_object["data"][x].bird_name_col)] = dic_object["data"][x].bird_count_col
            
        return {"data":bird_details}
    
    
    
    







