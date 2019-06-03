import pymongo
from bson import ObjectId

class DBHelper:
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client['animals']

    def get_all_animals(self):
        return self.db.animals.find().sort('created_at',pymongo.DESCENDING)

    def get_animals(self,type):
        return self.db.animals.find({"type":type}).sort('created_at',pymongo.DESCENDING)

    def add_animal(self,name,type,description,image_url):
        return self.db.animals.insert({'name':name,'type':type,'description':description,'image_url':image_url})

    def get_animal(self, animal_id):
        return self.db.animals.find({'_id':ObjectId(animal_id)})

    def update_animal(self,id,name,type,description,image_url):
        return self.db.animals.update({'_id':ObjectId(id)},{'name':name,'type':type,'description':description,'image_url':image_url})

    def add_vote(self,id,vote):
        return self.db.votes.insert({'_id':ObjectId(id),"votes":vote})

    def update_vote(self,id,vote):
        return self.db.votes.update({'_id':ObjectId(id)},{"votes":vote})

    def get_vote(self,id):
        return self.db.votes.find({"_id":ObjectId(id)})

    def get_votes(self):
        return self.db.votes.find()
