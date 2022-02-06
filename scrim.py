from datetime import *
from pymongo import MongoClient

# Database info removed for privacy
cluster = MongoClient(")
db = cluster[""]
collection = db[""]

class Scrim:
    """
    Represents a scrim object.

    Parameters:
    - opponent(str): Name of scrim opponent
    - date(datetime): Date of scrim ("%d/%m/%y %I:%M %p")
    """

    now = datetime.now()

    def __init__(self, opponent:str, date:datetime, team:str):
        self.opponent = opponent
        self.date = date
        self.team = team
        self.day = date.strftime("%#d %B, %Y")
        self.time = date.strftime("%#I:%M %p")
        
    def confirm_entry(self):
        '''Inserts scrim object into the scrim database'''
        timestamp = datetime.utcnow()
        entry = {"Team":self.team, "Opponent":self.opponent, "Date":self.day, "Time":self.time, "Timestamp":timestamp, "Object":self.date}
        collection.insert_one(entry)

    def get_scrims(team):
        '''Returns list of scrims sorted by date closest to now'''
        query = {"Team":{"$regex":team}}

        if query is None:
            return None

        results = collection.find(query)
        
        list = []
        for x in results:
            scrim=[]
            scrim.append(x["Opponent"])
            scrim.append(x["Date"])
            scrim.append(x["Time"])

            date = x["Object"]
            diff = date - datetime.now()
            scrim.append(diff.days)
            list.append(scrim)

        list = sorted(list, key=lambda x:x[3], reverse=False)
        return list

    def delete_scrim(team, opponent, date):
        '''Delete scrim given team, opponent, and date'''
        query = {"Opponent":{"$regex":opponent}, "Team":{"$regex":team}, "Date":{"$regex":date}}
        collection.delete_one(query)
        
    def update_opponent(team, old, new):
        '''Update scrim opponent name'''
        timestamp = datetime.utcnow()
        filter = {"Opponent":{"$regex":old}, "Team":{"$regex":team}}
        new_val = {"$set":{"Opponent":new}, "$set":{"Timestamp":timestamp}}
        collection.update_one(filter, new_val)
        
    def update_date(team, old, new_object:datetime):
        '''Update scrim date'''
        timestamp = datetime.utcnow()
        filter = {"Team":{"$regex":team}, "Date":{"$regex":old}}
        new_date = new_object.strftime("%#d %B, %Y")
        new_time = new_object.strftime("%#I:%M %p")
        #No idea why, but db wouldn't update date value in one call. Using update_one multiple times is bandaid fix
        new_val = {"$set":{"Timestamp":timestamp},"$set":{"Object":new_object}}
        collection.update_one(filter,new_val)
        new_val = {"$set":{"Time":new_time}}
        collection.update_one(filter,new_val)
        new_val = {"$set":{"Date":new_date}}
        collection.update_one(filter, new_val)
        

    def get_past_scrims(team):
        '''Returns list of scrims that have passed'''
        pass

    def clean_scrims(team):
        '''Deletes scrims that have passed'''
        pass

