#imports
import os
from unittest import result
import pymongo
import numpy as np
import pandas as pd
from pandas import DataFrame
import math
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import json
import sys

# Getting base of recipe from user
# a = sys.argv[1]
# b = sys.argv[2]
# c = sys.argv[3]
# recipe = json.loads(c)
# d = sys.argv[4]

a = "cake"
b= "xxx cake"
recipe = {
    "normalized_ingredients": ["chocolate"],
    "normalized_amounts" : ["1.0 tsp"],
    "directions_keywords" : ["bake"]
}
d = 10


recipeType = a
ingredientList = recipe["normalized_ingredients"] 
size = d

print(ingredientList)
## Get database for recommendation
#
#Using pymongo gets the db and the collection 
#before it's normalized from mongoDB
#Saves the collection as pandas dataframe
client = pymongo.MongoClient()
recipeDB = client["precent_recipeDB"]
recipesCol = recipeDB["recipes"]

#Finds recipes similar to the user's recipe using a find query
# using regex with options: i to ignore case
df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": recipeType,"$options" :'i'}, "rating": { "$gte": 4.5 }})))
print(df.head())
print(df.shape)
##


## ------
# Apriori
# the recommendation system uses apriori association-rule algorithm first to determine which ingredients and directions it should recommend
# it does so by finding which ingredients are likely to be in the same recipe as user's ingredients/directions


# Creates a new df all ingredients and directions and sets each col's type to bool to convert numbers to true/false
apriori_df = df.iloc[:, 21:]
print(apriori_df.head())
print(apriori_df.shape)

for col_name in apriori_df.columns: 
    apriori_df[col_name] = apriori_df[col_name].astype(bool)

print(apriori_df.head(10))
print(apriori_df["flour"].head(10))
print(apriori_df.shape)

##
# Runs appriori model
# with minimum support value set as 0.01, so the algorithm won't consider items purchased together in only 1% of recipes
# use_colnames to use the column names (directions and ingredients) rather than column indexes
ar_ap = apriori(apriori_df, min_support=0.01, max_len=2,
                use_colnames=True)

#Calculates association rules
# with min_threshold to limit results that are not likely to be highly relevant
ar = association_rules(ar_ap, 
                       metric="lift", 
                       min_threshold=0.5)
print(ar)

# Making recommendations
def predict(antecedent, rules, max_results= int(20/len(ingredientList))):
    
    # get the rules for this antecedent
    preds = rules[rules['antecedents'] == antecedent]
    
    # a way to convert a frozen set with one element to string
    preds = preds['consequents'].apply(iter).apply(next)
    
    return preds[:max_results]

#combines lists of recommendations for all ingredients
preds = []
for i in ingredientList:
    curr_preds = predict({i}, ar).values.tolist()
    preds = preds + curr_preds

#adds user's original ingredients to the generated recipe
preds = ingredientList + preds

#gets unique recommendations
unique_preds =  np.array(preds)
unique_preds = np.unique(unique_preds)

#divides recommendations into ingredients and directions
lastIngredientCol = apriori_df.columns.get_loc("zucchini")
ingredients_df = apriori_df.iloc[:, :lastIngredientCol+1]
ingredients_names = list(ingredients_df.columns.values)

ingredient_preds = []
directions_preds = []

for i in unique_preds:
    if i in ingredients_df:
        ingredient_preds.append(i)
    else:
        directions_preds.append(i)
        
print("ingredients", ingredient_preds)
print("directions", directions_preds)

#-----
# Cosine similarity
# to get the amounts of the ingredients for the generated recipe, the recommendation system runs a cosine similarity algorithm 
# it finds the recipes that are most similar to the generated recipe, and averages their amounts to get the amounts for the user's ingredients

#preparing the dataset for cosine similarity algorithm by getting only the list of ingredients,
#inserting the user's generated recipe at the top so its index is 0,
#and convering them to string for the cosine similarity
cs_df = df["normalized_ingredients"]

cs_df.loc[-1] = ingredient_preds
cs_df.index = cs_df.index + 1  # shifting index
cs_df.sort_index(inplace=True) 

cs_df = cs_df.apply(', '.join)
print(cs_df.head())

#converts text to a matrix of token counts
cm = CountVectorizer().fit_transform(cs_df)
#cosine similarity will get similarity matrix from token count matrix because it measures similarity between two non zero vectors
# each column and each row will be a recipe, and the value will be how similar it is one to the other
# so in the center diagonal line the values will be 1, because its the same recipe, and the similarity will be 100%
cs = cosine_similarity(cm)
print(cs)
print(cs.shape)

#creates a list of enums for the similarity score, to connect recipe index (which is 0) and its similarity score
#then sorts list to get highest similarity score, and removes the one with 1 value, since it'll be the 
# recipe itself
scores = list(enumerate(cs[0]))
sorted_scores = sorted(scores, key=lambda x:x[1], reverse=True)
sorted_scores = sorted_scores[1:]

#gets the seven most similar recipes to the user's recipe and puts them into new df
firstTen_sorted_scores = sorted_scores[0:10]
print(firstTen_sorted_scores) 
similar_amounts_df = pd.DataFrame()

for i in firstTen_sorted_scores:
    recipe = cs_df.iloc[[i[0]]]
    print(recipe)
    similar_amounts_df = similar_amounts_df.append(df.iloc[[i[0]-1]])

#removes unnecessary columns from new df and means the amounts to get the final amounts for the user's ingredients
similar_amounts_df = similar_amounts_df.iloc[:, 21:]
similar_amounts_df = similar_amounts_df.iloc[:, :lastIngredientCol+1]
similar_amounts_df = similar_amounts_df.replace(0, np.NaN)
similar_amounts_df = similar_amounts_df.mean(axis = 0)

# if didn't find amount for one or more of the ingredients, finds it in the entire db
all_amounts_df = df.iloc[:, 21:]
all_amounts_df = all_amounts_df.iloc[:, :lastIngredientCol+1]
all_amounts_df = all_amounts_df.replace(0, np.NaN)
all_amounts_df = all_amounts_df.mean(axis = 0)
print(similar_amounts_df)
print(all_amounts_df.head())

#gets the ingredient amounts from the new df
amount_preds = []
for i in ingredient_preds:
    amount = similar_amounts_df[i]
    if math.isnan(amount):
        amount = all_amounts_df[i]
    amount_preds.append(amount)
print(ingredient_preds)
print(amount_preds)


# convert amount recommendations from % to normal measurement
# using array of volume categories, it will decide if ingredient belongs to weight or volume
# if weight, will use convert rate from weight table to convert to grams
# if volume, will convert to tbs, tsp or cup appropriately
# converts according to user's chosen serving size
weight_conv_df = pd.read_excel(os.path.dirname(os.path.realpath(__file__)) + '\ingredients_weights.xlsx')
volume_categories_array = ["Sugar & Sweeteners", "Dairy-Free & Meat Substitutes", "Baking", "Dairy & Eggs", "Beverages","Condiments & Relishes","Dressings & Vinegars","Herbs & Spices","Oils","Sauces, Spreads & Dips","Seasonings & Spice Blends","Soups, Stews & Stocks","Wine, Beer & Spirits"]

def convert_amounts(ingredient, tbspAmount, ingredientPercentage):
    # find the type of ingredient by its name
    ingredientsCol = recipeDB["ingredients"]
    cursor = ingredientsCol.find({"ingredient_name": ingredient})
    ingredientDBObj = cursor.next()
    category = ingredientDBObj["category"]
    loc_result = weight_conv_df.loc[weight_conv_df['ingredient']
                                   == ingredient]
    isVolume = category in volume_categories_array
    ingredientTbsp = float(tbspAmount) * (ingredientPercentage / 100.0)
    
    # if isVolume is false, then it's weight
    if not isVolume:
        conv_rate = loc_result['tbs_in_1_gram'].values[0]
        return [ingredient, round(ingredientTbsp / conv_rate, 1), "gram"]
    
    
    if (ingredientTbsp < 0.3333):
        return [ingredient, round(ingredientTbsp * 3,1), "tsp"]
    if (ingredientTbsp >= 4):
        return [ingredient, round(ingredientTbsp / 16,1), "cup"]
    return [ingredient, round(ingredientTbsp,1), "tbsp"]

final_ingredients_recs = []
for index, i in enumerate(amount_preds):
    final_ingredients_recs.append(convert_amounts(ingredient_preds[index],size,i))
    
print(final_ingredients_recs)
print(directions_preds)

#-----
# Ordering directions
# to make directions appear more user friendly, puts the directions in order from db
# directions that are categorized 'prepare' will be first, 'cook' will be second, and 'finish' will be last

# getting the keywords collection and putting it into a df
directionsCol = recipeDB["directions_keywords"]
directions_df = DataFrame(list(directionsCol.find({})))
print(directions_df.head())
print(directions_df.shape)

prepare_directions = []
cook_directions = []
finish_directions = []

for i in directions_preds:
    if directions_df[directions_df.keyword == i]['type'].values[0] == "prepare":
       prepare_directions.append(i)
    elif directions_df[directions_df.keyword == i]['type'].values[0] == "cook":
        cook_directions.append(i)
    else:
        finish_directions.append(i)

print(prepare_directions)
print(cook_directions)
print(finish_directions)

final_directions_recs = prepare_directions + cook_directions + finish_directions

print("-------")
print(final_ingredients_recs)
print(final_directions_recs)

#converting results into a json format fitting for react

new_ingredients = []
improved_ingredients = []

for i in final_ingredients_recs:
    if i[0] in ingredientList:
        improved_ingredients.append(i)
    else:
        new_ingredients.append(i)

results = {"new_ingredients":new_ingredients,"improved_ingredients":improved_ingredients,"improved_directions":final_directions_recs}
print(results)