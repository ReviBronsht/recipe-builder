#imports
from os import name
from unittest import result
import pymongo
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


## Get database for recommendation
#
#Using pymongo gets the db and the collection 
#before it's normalized from mongoDB
#Saves the collection as pandas dataframe
client = pymongo.MongoClient()
recipeDB = client["precent_recipeDB"]
recipesCol = recipeDB["recipes"]

#Getting the type of the recipe from the user 
recipeType = "cake"

recipeTitle = "xxx cake"

recipe = {
    "normalized_ingredients": ["flour","egg","milk"],
    "normalized_amounts" : ["25.0 tsp","2.0 tbsp","1.0 tsp"],
    "directions_keywords" : ["prepare","batter"]
}

size = 79

# normalizing user's recipe

last_ingredient = len(recipe["normalized_ingredients"]) - 1 + 3

df = pd.json_normalize(recipe)

print(df.head())


# ###### Normalizing the user's recipe to be the same format as the db recipes
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


for i, row in final_df.iterrows():
    ingredients = row["normalized_ingredients"]
    all_ingredients = list(final_df.iloc[:, 21:last_ingredient+1].columns.values)
    for ingredient in all_ingredients:
        if row[ingredient] == 1:
            if (ingredient not in ingredients):
                final_df.at[i,ingredient] = 0
        


#
## Amounts normalize
#This part will change the df created by dummies to show the amount of each ingredient
#instead of just if it exists or not

# using two excel tables for conversion rates in the convert_to_tablespoons function
weight_conv_df = pd.read_excel('C:\\Users\\revib\\Downloads\\Backend\\development_files\\algorithms\\VolumeToTbs_weight.xlsx')
unit_conv_df = pd.read_excel('C:\\Users\\revib\\Downloads\\Backend\\development_files\\algorithms\\VolumeToTbs_units.xlsx')

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
final_df.iloc[:, 21:last_ingredient+1] =final_df.iloc[:, 21:last_ingredient+1].astype(float)

#Iterates over every row in the df, and for each row iterates all the ingredients in the names of the ingredients in that recipe
# it converts the ingredient's amount to tablespoons using convert_to_tablespoons function 
for i, row in final_df.iterrows():
    amount_num = 1
    for idx, ingredient in enumerate(row["normalized_ingredients"]):
        amount = row["normalized_amounts"][idx]
        amount_num = convert_to_tablespoons(amount,ingredient)
        final_df.at[i,ingredient] = row[ingredient] * amount_num
#
## Precent
#
#Calculating the precentage of the ingredient from the recipe whole
# Finds whole for each recipe by calculating the sum of the teaspoons for every recipe
# this will normalize the data for clustering so its on the right distance from center of cluster

ingredients = final_df.iloc[:, 3:last_ingredient+1]
print("last ingredient:", last_ingredient)
print("ingredients: ",ingredients.head())
final_df["sum"] = ingredients.sum(axis=1)
print(final_df.head())

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
            print("precent:",precent)
            final_df.at[i,ingredient] = precent

#delete sum column
final_df = final_df.iloc[: , :-1]
print("final user's recipe normalized:")
print(final_df.head())
#

#Finds recipes similar to the user's recipe using a find query
# using regex with options: i to ignore case
df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": recipeType,"$options" :'i'}, "rating": { "$gte": 4.5 }})))
print(df.head())
print(len(df))
print(df["recipe_title"].head())
print(df["rating"].head())
print(df.shape)
##

#adding user's recipe to recipe df
# setting recipe df to the same size as database df

temp_recipe_df = df.iloc[:1].copy(deep=True)

for col in temp_recipe_df.iloc[:, :13].columns:
    temp_recipe_df[col].values[:] = np.NaN
for col in temp_recipe_df.iloc[:1, 14:15].columns:
    temp_recipe_df[col].values[:] = [""]
for col in temp_recipe_df.iloc[:1, 21:].columns:
    temp_recipe_df[col].values[:] = 0
     

temp_recipe_df["recipe_title"] = recipeTitle 
temp_recipe_df["normalized_ingredients"] = final_df["normalized_ingredients"]
temp_recipe_df["normalized_amounts"] = final_df["normalized_amounts"]
temp_recipe_df["directions_keywords"] = final_df["directions_keywords"]
#print(temp_recipe_df)

recipe_columns = final_df.iloc[:, 3:].columns
# print(recipe_columns)

for col in recipe_columns:
    print(final_df[col].values[:][0])
    temp_recipe_df[col] = final_df[col].values[:][0]

print(temp_recipe_df)
print("user's ingredients:")
print(temp_recipe_df["normalized_ingredients"])
frames = [temp_recipe_df, df]

print(len(temp_recipe_df.columns))
print(len(df.columns))

df.index = df.index + 1  # shifting index
df = pd.concat(frames)
df.sort_index(inplace=True) 
print(df)
####---- Recommendation


# Creates a list of important columns for the recommendation engine
columns = ['normalized_ingredients','directions_keywords']
print(df[columns].head(3))
#drops nulls if there are any
# temp_df = df[columns].dropna()
# print(temp_df.head())
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
print(df.head())

#converts text to a matrix of token counts
cm = CountVectorizer().fit_transform(df['important_features'])
#cosine similarity will get similarity matrix from token count matrix because it measures similarity between two non zero vectors
# each column and each row will be a recipe, and the value will be how similar it is one to the other
# so in the center diagonal line the values will be 1, because its the same recipe, and the similarity will be 100%
cs = cosine_similarity(cm)
print(cs)
print(cs.shape)


##Gets the user's recipe
recipe_id = 0

#creates a list of enums for the similarity score, to connect recipe id and its similarity score
#then sorts list to get highest similarity score, and removes the one with 1 value, since it'll be the 
# recipe itself
scores = list(enumerate(cs[recipe_id]))
sorted_scores = sorted(scores, key=lambda x:x[1], reverse=True)
sorted_scores = sorted_scores[1:]
print(sorted_scores)

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


    
print("----")
recipe_ingredients = df.loc[recipe_id]["normalized_ingredients"]
recipe_ingredients_amounts = []
recipe_ingredients_amounts = add_amounts(recipe_ingredients_amounts,recipe_ingredients,recipe_id,df)
recipe_directions = df.loc[recipe_id]["directions_keywords"]
print("user's ingredients: ",recipe_ingredients_amounts)
print(" user's directions: ",recipe_directions)

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

# convert to normal measurement
def convert_amounts(ingredient, tbspAmount, ingredientPercentage):
    ingredientTbsp = tbspAmount * (ingredientPercentage / 100.0)
    if (ingredientTbsp < 0.3333):
        return [ingredient, round(ingredientTbsp * 3,1), "tsp"]
    if (ingredientTbsp >= 4):
        return [ingredient, round(ingredientTbsp / 16,1), "cup"]
    return [ingredient, round(ingredientTbsp,1), "tbsp"]

for index, i in enumerate(new_ingredients):
    new_ingredients[index] = convert_amounts(i[0],size,i[1])
for index, i in enumerate(improved_ingredients):
    improved_ingredients[index] = convert_amounts(i[0],size,i[1])


print("Suggested ingredients to add to recipe: ",new_ingredients)
print("Suggested to change ingredients amount: ",improved_ingredients)
print("Suggested directions to improve recipe: ",improved_directions)
## 
results = {"new_ingredients":new_ingredients,"improved_ingredients":improved_ingredients,"improved_directions":improved_directions}
print(results)

# ## 


