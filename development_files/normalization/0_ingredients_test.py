#imports
from os import name
from typing import final
import pymongo
import numpy as np
import pandas as pd
from pandas import DataFrame

## Get database for normalization
#
#Using pymongo gets the db and the collection 
#before it's normalized from mongoDB
#Saves the collection as pandas dataframe
client = pymongo.MongoClient()
#recipeDB = client["final_recipeDB"]
recipeDB = client["final_recipeDB"]
recipesCol = recipeDB["recipes"]

#df = DataFrame(list(recipesCol.aggregate([ { "$sample": { "size": 10 } } ])))
#df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": "cake","$options" :'i'}, "rating": { "$gte": 4.5 } }).limit(5)))
df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": "chicken","$options" :'i'}}).limit(5)))
print(df.head())
print(len(df))

ingredients = []

for i, row in df.iterrows():
    ingredients = row["normalized_ingredients"]
    all_ingredients = list(df.iloc[:, 21:].columns.values)
    print(row["recipe_title"])
    print(row["ingredients"])
    print(row["total_tbs"])
    print(row["normalized_ingredients"])
    print(row["normalized_amounts"])
    for ingredient in all_ingredients:
        if row[ingredient] != 0:
            print(row[ingredient],ingredient)