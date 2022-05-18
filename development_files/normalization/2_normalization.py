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
recipeDB = client["new_recipeDB"]
recipesCol = recipeDB["recipes"]

df = DataFrame(list(recipesCol.find({})))
print(df.head())
print(len(df))
##

######

#
#Using get dummies to turn list colums into numerical columns
#
# For ingredients, will create colums with all the ingredient names, put 0 where the ingredients don't exist and 1 where they do.
# Will do the same thing for directions keywords

#Because get_dummies doesn't work on lists, explode seperates the values in each list of ingredients. This ceates a row per ingredient, 
# so there are multiple rows for each recipe. 
# using get_dummies turns each ingredient into a column, and puts 1 where it exists and 0 where it doesn't exist. But since there are multiple
# rows per recipe, this creates a multi-level index, where every ingredient adds a new row to each recipe. 
# sum merges the rows that should be one row, so each recipe returns to one row, with all the ingredients it has.
# does the same thing for directions_keywords

final_df = df

for column in ["normalized_ingredients", "directions_keywords"]:
         dummies = pd.get_dummies(df[column].explode()).groupby(level = 0).sum()
         final_df[dummies.columns] = dummies
print(final_df.head())

# the get dummies above also marks containing values
# like for bread crumbs, it will mark that the recipe has both bread and breadcrumbs because bread is in bread crumbs
# this function finds which ingredients are falsly marked like that in the db and turns them back to 0

# zucchini is the last possible ingredient, uses it to find where ingredients end and directions begin
lastIngredientCol = final_df.columns.get_loc("zucchini")
print(final_df.iloc[:, 20:lastIngredientCol+1])

for i, row in final_df.iterrows():
    ingredients = row["normalized_ingredients"]
    all_ingredients = list(final_df.iloc[:, 20:lastIngredientCol+1].columns.values)
    for ingredient in all_ingredients:
        if row[ingredient] == 1:
            if (ingredient not in ingredients):
                final_df.at[i,ingredient] = 0
        


#
## Amounts normalize
#This part will change the df created by dummies to show the amount of each ingredient
#instead of just if it exists or not

# using two excel tables for conversion rates in the convert_to_tablespoons function
weight_conv_df = pd.read_excel('VolumeTotbs_weight.xlsx')
unit_conv_df = pd.read_excel('VolumeTotbs_units.xlsx')

# function converts every ingredient amount to tablespoons
def convert_to_tablespoons(amount,ingredient):
    tbs_amount = 1.0
    # This function has 4 cases;
    #   case 1: ingredient is measured in volume, so it will directly convert it to tablespoons
    #   case 2: ingredient is measured in weight, so it will convert it to grams, and then use the conversion rate from the excel table to get its measurement in tablespoons
    #   case 3: ingredient is measured in unit, so it will use the unit conversion excel table to get how many tablespoons the unit is
    #   case 4: ingredient has no measurement or amount, like in case of pinch of salt or cooking spray. Will return ingredient as 0.021 since it's roughly a pinch in tablespoons. Will do the same for ingredients it didn't find to make them no significant.

    # options for volume and weight conversion
    vol_measurements = ["tbsp","tsp","fl","qt","pt","gal","ml","cup","liter"]
    vol_convert = [1.0, 0.333, 1.9, 64.0, 32.0, 256.0, 0.067, 19.215, 67.628]
    weight_measurements = ["gram","oz","ounce","lb","kg","pound"]
    weight_convert = [1.0,28.3495,28.3495,453.592,1000,453.592]

    #creates a list of amount, measurement from the amount column
    amount_list = amount.split()

    #if amount exists, goes to the cases.
    if amount != "":
        amount_num = amount_list[0] #gets the number from the list
        if(len(amount_list) > 1): #if list is longer than 1, measurement exists and its only case 1 or 2
            amount_measurement = amount_list[1]
            #checks if measurement is weight or volume, and does appropriate conversion 
            if amount_measurement in vol_measurements:
                index = vol_measurements.index(amount_measurement)
                tbs_amount = float(amount_num) * vol_convert[index]
            elif amount_measurement in weight_measurements:
                index = weight_measurements.index(amount_measurement)
                try:
                    #tries to find the conversion rate for the ingredient from the conversion rate by weights df
                    conv_rate = weight_conv_df.loc[weight_conv_df['Ingredient'] == ingredient]['tbs'].values[0]
                except:
                    #if didn't find the ingredient, the conversion rate is the average of all the rates
                    conv_rate = 0.1
                tbs_amount = float(amount_num) * weight_convert[index] * conv_rate
        elif (len(amount_list) == 1): #if list is exactly 1, only amount exists, and its case 3
            try:
                    #tries to find the amount of tablespoons for 1 unit of the ingredient from the excel
                    unit_tbs = unit_conv_df.loc[unit_conv_df['ingredient'] == ingredient]['tablespoon'].values[0]
            except:
                    #if didn't find the ingredient, the amount of tbs is the average of all the tbs amounts
                    unit_tbs = 19.212
            tbs_amount = float(amount_num) * unit_tbs
    else: #case 4
        tbs_amount = 0.021
    return tbs_amount



#Changes ingredients columns to float type to show the exact amount
final_df.iloc[:, 20:lastIngredientCol+1] =final_df.iloc[:, 20:lastIngredientCol+1].astype(float)

#Iterates over every row in the df, and for each row iterates all the ingredients in the names of the ingredients in that recipe
# it converts the ingredient's amount to tablespoons using convert_to_tablespoons function 
for i, row in final_df.iterrows():
    amount_num = 1
    for idx, ingredient in enumerate(row["normalized_ingredients"]):
        amount = row["normalized_amounts"][idx]
        amount_num = convert_to_tablespoons(amount,ingredient)
        final_df.at[i,ingredient] = row[ingredient] * amount_num
#


## Saving the dataframe to new db in MongoDB
#
#Creates a new db with a new collection, saves the df as dictionary in records format
#and inserts into the collection
new_recipeDB = client["final_recipeDB"]
new_recipesCol = new_recipeDB["recipes"]
data = final_df.to_dict("records")
for recipe in data:
    new_recipesCol.insert_one(recipe)
#