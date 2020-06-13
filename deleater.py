import pymongo #yDGTNy2WK52Bqsm


client = pymongo.MongoClient("mongodb+srv://lol:yDGTNy2WK52Bqsm@cluster0-gijx9.mongodb.net/bcdata?retryWrites=true&w=majority")

db = client["bcdata"]

dlong = db["60d"]
dshort = db["kd"]
dsupershort = db["kd1d"]

query = {
    "scrape_id": {
        "$regex":"06_05_2020"
    }
}

dlong.delete_many(query)

dshort.delete_many(query)

dsupershort.delete_many(query)