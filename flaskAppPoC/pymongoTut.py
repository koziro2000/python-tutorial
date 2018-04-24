import pymongo
import pprint
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')

db = client.conquer
radocs = db.radoc
multiple_ras = [
    {"assetname":"oh yeah2", "address": "555 street"},
    {"assetname":"oh yeah3", "address": "555 street"}]
ras = {"assetname":"oh yeah1", "address": "555 street"}
ras_id = radocs.insert_one(ras).inserted_id

pprint.pprint(radocs.find_one(filter={"assetname":"oh yeah1"} ))
pprint.pprint(radocs.find_one_and_delete({"_id": ras_id}))

results = radocs.insert_many(multiple_ras)
pprint.pprint(results.inserted_ids)

for ras in radocs.find():
    pprint.pprint(ras)