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
recipeDB = client["final_recipeDB"]
recipesCol = recipeDB["recipes"]

df = DataFrame(list(recipesCol.find({})))
print(df.head())
print(len(df))
##

######

## Precent
#
#Calculating the precentage of the ingredient from the recipe whole
# Finds whole for each recipe by calculating the sum of the teaspoons for every recipe
# this will normalize the data for clustering so its on the right distance from center of cluster
lastIngredientCol = df.columns.get_loc("zucchini")
print(df.iloc[:, 17:lastIngredientCol+1])
ingredients = df.iloc[:, 17:lastIngredientCol+1]
print(ingredients.head())
df["sum"] = ingredients.sum(axis=1)
print(df.head())

# function to find the precent of something out of the recipe whole
def find_precent(value,whole):
    return round((value/whole) * 100, 3)

#getting names of the ingredient columns for the iteration
ingredients_names = []
for col in ingredients.columns:
    ingredients_names.append(col)

#iterates over every row and ingredient and calculates its precentage from the whole
for i, row in df.iterrows():
    whole = row["sum"]
    for ingredient in ingredients_names:
        value = row[ingredient]
        if(value != 0.0):
            precent = find_precent(value,whole)
            df.at[i,ingredient] = precent

#delete sum column
df = df.iloc[: , :-1]
print(df.head())
#

## Saving the dataframe to new db in MongoDB
#
#Creates a new db with a new collection, saves the df as dictionary in records format
#and inserts into the collection
new_recipeDB = client["precent_recipeDB"]
new_recipesCol = new_recipeDB["recipes"]
data = df.to_dict("records")
for recipe in data:
    new_recipesCol.insert_one(recipe)
#