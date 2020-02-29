import json
import os, sys, re
import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-yaj6q.mongodb.net/test?retryWrites=true&w=majority")
#db = client.test

db = client["bla"]
col = db["crypto"]


os.chdir(os.path.dirname(os.path.abspath(__file__)))

file = open(r'D:\xampp\htdocs\node\cryptoproject\crypto_datadump.json-plus', "r");

for line in file.readlines():
	
	for j in re.split(''';(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', line ):
		json = json.dumps(j)
		
		x = col.insert_many(json)
		
		print(x.inserted_ids)


