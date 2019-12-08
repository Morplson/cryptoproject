import pymongo

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0-yaj6q.mongodb.net/test?retryWrites=true&w=majority")
#db = client.test

db = client["bla"]
col = db["schueler"]


kinder = [
	{ "name":"Kalian J", "jahr":2006, "klasse": "4dhit", "ampeln":[{"fach":"AM","farbe":"blau"},{"fach":"INSY","farbe":"gruen"}] },
	{ "name":"Richafrd", "jahr":2004, "klasse": "4dhit", "ampeln":[{"fach":"AM","farbe":"gruen"},{"fach":"INSY","farbe":"gruen"}] },
	{ "name":"Christoph Brein 2", "jahr":2003, "klasse": "4dhit", "ampeln":[{"fach":"AM","farbe":"rot"},{"fach":"INSY","farbe":"gruen"}] },
	{ "name":"Daniel Zemmermann", "jahr":2000, "klasse": "4dhit", "ampeln":[{"fach":"AM","farbe":"gelb"},{"fach":"INSY","farbe":"gelb"}] },
	{ "name":"Rudolf Schank", "jahr":2002, "klasse": "4dhit", "ampeln":[{"fach":"AM","farbe":"gruen"},{"fach":"INSY","farbe":"rot"}] },
	{ "name":"Gregor Donerbude", "jahr":2001, "klasse": "4dhit", "ampeln":[{"fach":"AM","farbe":"gruen"},{"fach":"INSY","farbe":"rot"}] }
]


#x = col.insert_many(kinder)
#print(x.inserted_ids) 




print("\n\nall")
data = col.find({})

for x in data:
	print(x) 


print("\n\nj2000")
data = col.find({"jahr":2000})

for x in data:
	print(x) 


print("\n\nj2000+")
data = col.find({"jahr":{"$gt":2000}})

for x in data:
	print(x) 


print("\n\nj200&4d")
data = col.find({"jahr":2000,"klasse":"4dhit"})

for x in data:
	print(x) 



print("\n\n4d&red")
data = col.find({"klasse":"4dhit","ampeln":{ "$elemMatch" : { "fach":"AM", "farbe":"rot"}}})

for x in data:
	print(x) 