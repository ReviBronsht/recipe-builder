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
lastIngredientCol = final_df.columns.get_loc("zucchini")
print(final_df.iloc[:, 17:lastIngredientCol+1])

for i, row in final_df.iterrows():
    ingredients = row["normalized_ingredients"]
    all_ingredients = list(final_df.iloc[:, 17:lastIngredientCol+1].columns.values)
    for ingredient in all_ingredients:
        if row[ingredient] == 1:
            if (ingredient not in ingredients):
                final_df.at[i,ingredient] = 0
        


#
## Amounts normalize
#This part will change the df created by dummies to show the amount of each ingredient
#instead of just if it exists or not

#convert to teaspoons function used to unify ingredients based on their measurements
# it will convert all other measurements to teaspoons, and if there is no measurement will
# just return a float value of the amount
# this will mostly work because items measured without a measurement will be compared to the same item without a measurement
# (like eggs, most recipes will say 1 or 2 eggs, not 0.23 gram of egg), and the opposite is also true.


df = pd.read_excel('measurements.xlsx')
# data = pd.read_excel(open('density_DB_v2_0_final-1__1_.xlsx','rb'), sheet_name='Density DB', index_col=0)

def create_excel_df():
    column_names = ["ingredient", "spoons"]
    excel_df = pd.DataFrame([["",0]], columns = column_names)

    for i in range(285):
        ingredient = df.loc[i, 'Ingredient']
        volume = df.loc[i, 'Volume']
        grams = df.loc[i, 'Grams']
        teaSpoon = 0
        if 'cup' in volume:
            if volume == '1 cup':
                if isinstance(grams, str):
                    grams = grams.split()
                    lowGrams = int(grams[0])
                    highGrams = int(grams[2])
                    lowTeaSpoons = lowGrams / 48
                    highTeaSpoons = highGrams / 48
                    teaSpoon = ((highTeaSpoons - lowTeaSpoons) / 2 ) + lowTeaSpoons
                else:
                    teaSpoon = grams / 48
            if volume == '1/2 cup':
                if isinstance(grams, str):
                    grams = grams.split()
                    lowGrams = int(grams[0])
                    highGrams = int(grams[2])
                    lowTeaSpoons = lowGrams / 24
                    highTeaSpoons = highGrams / 24
                    teaSpoon = ((highTeaSpoons - lowTeaSpoons) / 2 ) + lowTeaSpoons
                else:
                    teaSpoon = grams / 24
            if volume == '1/4 cup':
                if isinstance(grams, str):
                    grams = grams.split()
                    lowGrams = int(grams[0])
                    highGrams = int(grams[2])
                    lowTeaSpoons = lowGrams / 12
                    highTeaSpoons = highGrams / 12
                    #teaSpoon = "{} to {}".format(lowTeaSpoons,highTeaSpoons)
                    teaSpoon = ((highTeaSpoons - lowTeaSpoons) / 2 ) + lowTeaSpoons
                else:
                    teaSpoon = grams / 12
        if 'table' in volume:
            units = volume.split()
            units = int(units[0])
            teaSpoon = grams / (units * 3)
        if 'tea' in volume:
            volume = volume.split()
            teaSpoon = grams / float(volume[0]) 

        excel_temp = pd.DataFrame([[ingredient,teaSpoon]], columns = column_names)
        excel_df = excel_df.append(excel_temp, ignore_index=True)
    print(excel_df.head())

    return excel_df


excel_df = create_excel_df()

def convert_to_teaspoons(amount,ingredient):
    tsp_amount = 1.0
    measurements = ["tbsp","tsp","oz","ounce","fl","qt","pt","gal","lb","ml","kg","cup","gram","liter"]
    convert = [3.0,1.0,6.0,6.0,6.0,192.0,96.0,768.0,92.03,0.2,240.0,48.0,0.23,202.88]
    amount_list = amount.split()
    if amount != "":
        amount_num = amount_list[0]
        if(len(amount_list) > 1):
            amount_measurement = amount_list[1]
            for idx, measurement in enumerate(measurements):
                if amount_measurement == measurement:
                    tsp_amount = float(amount_num) * convert[idx]
        else:
            generated_tsp = 1
            generated_ingredient = ""
            for i, row in excel_df.iterrows():
                excel_ingredient = row["ingredient"]
                if ingredient in excel_ingredient.lower():
                    generated_ingredient = excel_ingredient
            generated_spoons = excel_df[excel_df["ingredient"]==generated_ingredient]["spoons"].values[0]
            if(generated_spoons != 0.0):
                generated_tsp = generated_spoons
                tsp_amount = float(float(amount_num) * generated_tsp)
    return tsp_amount

lastIngredientCol = final_df.columns.get_loc("zucchini")
print(final_df.iloc[:, 17:lastIngredientCol+1])

#Changes ingredients columns to float type to show the exact amount
final_df.iloc[:, 17:lastIngredientCol+1] =final_df.iloc[:, 17:lastIngredientCol+1].astype(float)

#Iterates over every row in the df, and for each row iterates all the ingredients in the names of the ingredients in that recipe
# it finds the matching amount of the ingredients using matching indexes in the normalized amounts column
# if it found an amount, it will get the numerical value of the amount, and multiply it by the value in the matching ingredient column
# if the ingredient doesn't exist, the value will stay 0. If it does exist, multiplying by 1 will return the amount found earlier
for i, row in final_df.iterrows():
    amount_num = 1
    for idx, ingredient in enumerate(row["normalized_ingredients"]):
        amount = row["normalized_amounts"][idx]
        if amount != '':
            amount_num = convert_to_teaspoons(amount,ingredient)
        else:
            amount_num = 0.0625
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