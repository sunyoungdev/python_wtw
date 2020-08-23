from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.wtw

print(db.film_list.count())

db.runCommand({"distinct": "film_list", "key": "title"})
