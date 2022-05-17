#imports
import imp
from os import name
from unittest import result
import pymongo
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import json
import sys

a = sys.argv[1]
b = sys.argv[2]
c = sys.argv[3]
recipe = json.loads(c)

## Get database for recommendation
#
#Using pymongo gets the db and the collection 
#before it's normalized from mongoDB
#Saves the collection as pandas dataframe
client = pymongo.MongoClient()
recipeDB = client["precent_recipeDB"]
recipesCol = recipeDB["recipes"]

#Getting the type of the recipe from the user 
recipeType = a

recipeTitle = b

# normalizing user's recipe

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
    #print(excel_df.head())

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
#print(final_df.head())

## Precent
#
#Calculating the precentage of the ingredient from the recipe whole
# Finds whole for each recipe by calculating the sum of the teaspoons for every recipe
# this will normalize the data for clustering so its on the right distance from center of cluster

ingredients = final_df.iloc[:, 3:last_ingredient+1]
#print("last ingredient:", last_ingredient)
#print("ingredients: ",ingredients.head())
final_df["sum"] = ingredients.sum(axis=1)
#print(final_df.head())

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
            #print("precent:",precent)
            final_df.at[i,ingredient] = precent

#delete sum column
final_df = final_df.iloc[: , :-1]
#print("final user's recipe normalized:")
#print(final_df.head())
#

#Finds recipes similar to the user's recipe using a find query
# using regex with options: i to ignore case
df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": recipeType,"$options" :'i'}, "rating": { "$gte": 4.5 }})))
#print(df.head())
#print(len(df))
#print(df["recipe_title"].head())
#print(df["rating"].head())
#print(df.shape)
##

#adding user's recipe to recipe df
# setting recipe df to the same size as database df

temp_recipe_df = df.iloc[:1].copy(deep=True)

for col in temp_recipe_df.iloc[:, :10].columns:
    temp_recipe_df[col].values[:] = ""
for col in temp_recipe_df.iloc[:1, 11:12].columns:
    temp_recipe_df[col].values[:] = [""]
for col in temp_recipe_df.iloc[:1, 17:].columns:
    temp_recipe_df[col].values[:] = 0
     

temp_recipe_df["recipe_title"] = recipeTitle 
temp_recipe_df["normalized_ingredients"] = final_df["normalized_ingredients"]
temp_recipe_df["normalized_amounts"] = final_df["normalized_amounts"]
temp_recipe_df["directions_keywords"] = final_df["directions_keywords"]
##print(temp_recipe_df)

recipe_columns = final_df.iloc[:, 3:].columns
# #print(recipe_columns)

for col in recipe_columns:
    #print(final_df[col].values[:][0])
    temp_recipe_df[col] = final_df[col].values[:][0]

#print(temp_recipe_df)
#print("user's ingredients:")
#print(temp_recipe_df["normalized_ingredients"])
frames = [temp_recipe_df, df]

#print(len(temp_recipe_df.columns))
#print(len(df.columns))

df.index = df.index + 1  # shifting index
df = pd.concat(frames)
df.sort_index(inplace=True) 
#print(df)
####----


# Creates a list of important columns for the recommendation engine
columns = ['normalized_ingredients','directions_keywords']
#print(df[columns].head(3))
#drops nulls if there are any
# temp_df = df[columns].dropna()
# #print(temp_df.head())
#

# Creates function that combines the values of important columns into a string
def get_important_features(df):
    important_features = []
    for i in range(0, df.shape[0]):
        ingredients_list = []
        for ingredient in df['normalized_ingredients'][i]:
            n_ingredient = ingredient.replace(' ', '-')
            ingredients_list.append(n_ingredient)
        str_I = " ".join(str(x) for x in ingredients_list)
        str_D = " ".join(str(x) for x in df['directions_keywords'][i])
        important_features.append(str_I + ' ' + str_D)
    return important_features

#creates column for the important features
df['important_features'] = get_important_features(df)
#print(df.head())

#converts text to a matrix of token counts
cm = CountVectorizer().fit_transform(df['important_features'])
#cosine similarity will get similarity matrix from token count matrix because it measures similarity between two non zero vectors
# each column and each row will be a recipe, and the value will be how similar it is one to the other
# so in the center diagonal line the values will be 1, because its the same recipe, and the similarity will be 100%
cs = cosine_similarity(cm)
#print(cs)
#print(cs.shape)


##Gets the user's recipe
recipe_id = 0

#creates a list of enums for the similarity score, to connect recipe id and its similarity score
#then sorts list to get highest similarity score, and removes the one with 1 value, since it'll be the 
# recipe itself
scores = list(enumerate(cs[recipe_id]))
sorted_scores = sorted(scores, key=lambda x:x[1], reverse=True)
sorted_scores = sorted_scores[1:]
#print(sorted_scores)

# Uses the first best 3 recipes to find the ingredients the user might be missing, the ingredients the user might
# want to change their amount, and the directions he might be missing
def add_items(new_list,old_list):
    for i in old_list:
        new_list.append(i)
    return new_list

def add_amounts(new_list,old_list,recipe,df):
    for i in old_list:
        amount = df.loc[recipe][i]
        new_list.append([i, amount])
    return new_list

#print("----")
recipe_ingredients = df.loc[recipe_id]["normalized_ingredients"]
recipe_ingredients_amounts = []
recipe_ingredients_amounts = add_amounts(recipe_ingredients_amounts,recipe_ingredients,recipe_id,df)
recipe_directions = df.loc[recipe_id]["directions_keywords"]
#print("user's ingredients: ",recipe_ingredients_amounts)
#print(" user's directions: ",recipe_directions)

improved_ingredients_temp = []
improved_directions_temp = []
j = 0


for item in sorted_scores:
    similar_ingredients = df.loc[item[0]]["normalized_ingredients"]
    similar_ingredients_amounts = []
    similar_ingredients_amounts = add_amounts(similar_ingredients_amounts,similar_ingredients,item[0],df)
    similar_directions = df.loc[item[0]]["directions_keywords"]
    improved_ingredients_temp = add_items(improved_ingredients_temp,similar_ingredients_amounts)
    improved_directions_temp = add_items(improved_directions_temp,similar_directions)
    j = j+1
    if j>2:
        break

new_ingredients = []
improved_ingredients = []
improved_directions = []

def improve_directions(improved,current,all):
    for i in all:
        if(i not in current):
            improved.append(i)
    return improved
    
def improve_ingredients(improved,current,all):
    temp = []
    for i in all:
        if(i[0] not in current):
            temp.append(i)
    df2 = pd.DataFrame(np.array(temp),columns=["ingredient","amount"])
    df2["amount"] = pd.to_numeric(df2["amount"])
    df2 = df2.groupby("ingredient").mean()
    for i, row in df2.iterrows():
        improved.append([i,row["amount"]])
    return improved

def change_amount(improved,current,all):
    temp = []
    for i in all:
        if(i[0] in current):
            temp.append(i)
    df2 = pd.DataFrame(np.array(temp),columns=["ingredient","amount"])
    df2["amount"] = pd.to_numeric(df2["amount"])
    df2 = df2.groupby("ingredient").mean()
    for i, row in df2.iterrows():
        improved.append([i,row["amount"]])
    return improved

new_ingredients = improve_ingredients(new_ingredients,recipe_ingredients,improved_ingredients_temp)
improved_ingredients = change_amount(improved_ingredients,recipe_ingredients,improved_ingredients_temp)
improved_directions = improve_directions(improved_directions,recipe_directions,improved_directions_temp)

#print("Suggested ingredients to add to recipe: ",new_ingredients)
#print("Suggested to change ingredients amount: ",improved_ingredients)
#print("Suggested directions to improve recipe: ",improved_directions)
## 
results = {"new_ingredients":new_ingredients,"improved_ingredients":improved_ingredients,"improved_directions":improved_directions}
print(results)
# ## 


