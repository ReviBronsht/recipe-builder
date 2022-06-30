#imports
import json
#imports
import pymongo
import os
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
import sys


a = sys.argv[1]
b = sys.argv[2]
recipe = json.loads(b)

# recipe = b.to_dict()

last_ingredient = len(recipe["normalized_ingredients"]) - 1 + 3

df = pd.json_normalize(recipe)


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
#print(final_df.head())

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
weight_conv_df = pd.read_excel(os.path.dirname(os.path.realpath(__file__)) + '\VolumeTotbs_weight.xlsx')
unit_conv_df = pd.read_excel(os.path.dirname(os.path.realpath(__file__)) + '\VolumeTotbs_units.xlsx')

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
#print(final_df.head())
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
recipeType = "cake"

#Finds recipes similar to the user's recipe using a find query
# using regex with options: i to ignore case
df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": recipeType,"$options" :'i'}})))
#print(df.head())
#print(len(df))
#print(df["recipe_title"].head())
#print(df["rating"].head())
##

#reg function will perform regression on a target, once to predict recipe rating and once to predict recipe calories
def reg (target_col):
    # seperating features from target
    features = df.iloc[:, 21:]
    target = df[target_col]
    # splitting features to train and test
    X_train, X_test, y_train, y_test = train_test_split(features,target, train_size=0.8,random_state=0)
    #print("Training size: ", len(X_train), " Test size: ", len(X_test))

    # setting recipe df to the same size as database df
    columns = features.columns
    #print(columns)

    temp_recipe_df = df.iloc[:1, 21:]
    for col in columns:
        temp_recipe_df[col].values[:] = 0
        
    #print(temp_recipe_df)

    recipe_columns = final_df.iloc[:, 3:].columns
    # print(recipe_columns)

    for col in recipe_columns:
        #print(final_df[col].values[:][0])
        temp_recipe_df[col] = final_df[col].values[:][0]

    # 
    #
    # fits the linear regression model on the training dataset
    # usess a pipeline from PCA to linear regression, because 
    # our data has a lot of variables (900+), and many of them are 0
    # So to optimize the regression we'll preform PCA, to reduce the amount of variables to the meaningful ones

    from sklearn.ensemble import ExtraTreesRegressor as regressor
    pcr = make_pipeline(PCA(n_components=100), regressor( random_state=0))
    pcr.fit(X_train, y_train)
    # predicts the model on the test dataset
    predictions = pcr.predict(X_test)
    #print(len(predictions))


    #tests quality of regression model using mean_squared_error
    from sklearn.metrics import mean_squared_error
    # real value
    y_true = y_test
    # predicted value
    y_pred = predictions
    # calculate errors
    errors = mean_squared_error(y_true, y_pred)

    #print("mean squared error =",errors)

    #prints results
    results_df = X_test
    results_df[target_col] = y_true
    results_df["pred_rating"] = predictions
    #print(results_df)

    # predicting the recipe's rating
    #print(temp_recipe_df)
    recipe_predictions = pcr.predict(temp_recipe_df)
    return round(recipe_predictions[0],2)

print("rating: ", reg("rating"),"calories: ", reg("calories"))