#imports
import json
from calendar import c
import pymongo
from os import name
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn import linear_model
# import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import sys


a = sys.argv[1]
b = sys.argv[2]
recipe = json.loads(b)

# recipe = b.to_dict()

last_ingredient = len(recipe["normalized_ingredients"]) - 1 + 3

df = pd.json_normalize(recipe)

# print(df.head())

# #df = DataFrame(list(recipesCol.find({})))
# # print(df.head())
# # print(len(df))
# ##

# ######

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
# print(final_df.head())

# the get dummies above also marks containing values
# like for bread crumbs, it will mark that the recipe has both bread and breadcrumbs because bread is in bread crumbs
# this function finds which ingredients are falsly marked like that in the db and turns them back to 0


for i, row in final_df.iterrows():
    ingredients = row["normalized_ingredients"]
    all_ingredients = list(final_df.iloc[:, 3:last_ingredient+1].columns.values)
    for ingredient in all_ingredients:
        if row[ingredient] == 1:
            if (ingredient not in ingredients):
                final_df.at[i,ingredient] = 0
        


# #
# ## Amounts normalize
# #This part will change the df created by dummies to show the amount of each ingredient
# #instead of just if it exists or not

# #convert to teaspoons function used to unify ingredients based on their measurements
# # it will convert all other measurements to teaspoons, and if there is no measurement will
# # just return a float value of the amount
# # this will mostly work because items measured without a measurement will be compared to the same item without a measurement
# # (like eggs, most recipes will say 1 or 2 eggs, not 0.23 gram of egg), and the opposite is also true.


df = pd.read_excel('C:\\Users\\revib\\Downloads\\Backend\\Backend\\routes\\measurements.xlsx')
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
    # print(excel_df.head())

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



#Changes ingredients columns to float type to show the exact amount
final_df.iloc[:, 3:last_ingredient+1] =final_df.iloc[:, 3:last_ingredient+1].astype(float)

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
# print(final_df.head())

## Precent
#
#Calculating the precentage of the ingredient from the recipe whole
# Finds whole for each recipe by calculating the sum of the teaspoons for every recipe
# this will normalize the data for clustering so its on the right distance from center of cluster

ingredients = final_df.iloc[:, 3:last_ingredient+1]
# print("last ingredient:", last_ingredient)
# print("ingredients: ",ingredients.head())
final_df["sum"] = ingredients.sum(axis=1)
# print(final_df.head())

# function to find the precent of something out of the recipe whole
def find_precent(value,whole):
    return round((value/whole) * 100, 3)

#getting names of the ingredient columns for the iteration
ingredients_names = []
for col in ingredients.columns:
    ingredients_names.append(col)

#iterates over every row and ingredient and calculates its precentage from the whole
for i, row in final_df.iterrows():
    whole = row["sum"]
    for ingredient in ingredients_names:
        value = row[ingredient]
        if(value != 0.0):
            precent = find_precent(value,whole)
            # print("precent:",precent)
            final_df.at[i,ingredient] = precent

#delete sum column
final_df = final_df.iloc[: , :-1]
# print(final_df.head())
#

#
# ## Get database for regression

#Using pymongo gets the db and the collection 
#before it's normalized from mongoDB
#Saves the collection as pandas dataframe
client = pymongo.MongoClient()
recipeDB = client["precent_recipeDB"]
recipesCol = recipeDB["recipes"]

#Getting the type of the recipe from the user 
recipeType = a

#Finds recipes similar to the user's recipe using a find query
# using regex with options: i to ignore case
df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": recipeType,"$options" :'i'}})))
# print(df.head())
# print(len(df))
# print(df["recipe_title"].head())
# print(df["rating"].head())
##

# seperating features from target
df = df.dropna()
features = df.iloc[:, 17:]
target = df["rating"]
# splitting features to train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(features,target, train_size=0.8,random_state=0)
# print("Training size: ", len(X_train), " Test size: ", len(X_test))

# setting recipe df to the same size as database df
columns = features.columns
# print(columns)

temp_recipe_df = df.iloc[:1, 17:]
for col in columns:
     temp_recipe_df[col].values[:] = 0
     
# print(temp_recipe_df)

recipe_columns = final_df.iloc[:, 3:].columns
# print(recipe_columns)

for col in recipe_columns:
    # print(final_df[col].values[:][0])
    temp_recipe_df[col] = final_df[col].values[:][0]

# 
#
# fits the linear regression model on the training dataset
# usess a pipeline from PCA to linear regression, because 
# our data has a lot of variables (900+), and many of them are 0
# So to optimize the regression we'll preform PCA, to reduce the amount of variables to the meaningful ones
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA

pcr = make_pipeline(PCA(n_components=2), LinearRegression())
pcr.fit(X_train, y_train)

#print(X_train.size)
# predicts the model on the test dataset
predictions = pcr.predict(X_test)
# print(len(predictions))


#tests quality of regression model using mean_squared_error
from sklearn.metrics import mean_squared_error
# real value
y_true = y_test
# predicted value
y_pred = predictions
# calculate errors
errors = mean_squared_error(y_true, y_pred)

# print("mean squared error =",errors)

#prints results
results_df = X_test
results_df["rating"] = y_true
results_df["pred_rating"] = predictions
# print(results_df)

# predicting the recipe's rating
# print(temp_recipe_df)
recipe_predictions = pcr.predict(temp_recipe_df)
print(recipe_predictions[0])