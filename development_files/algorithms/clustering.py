#imports
from os import name
import pymongo
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn.cluster import KMeans as clustering
from sklearn.metrics import silhouette_score
import sys
#a = sys.argv[1]
a = "avocado"

# print(a)

# from amounts import amounts_normalize

## Get database for regression
#
#Using pymongo gets the db and the collection 
#before it's normalized from mongoDB
#Saves the collection as pandas dataframe
client = pymongo.MongoClient()
recipeDB = client["precent_recipeDB"]
recipesCol = recipeDB["recipes"]

# #Getting the type of the recipe from the user 
recipeType = a

#Finds recipes similar to the user's recipe using a find query
# using regex with options: i to ignore case
#finds recipes with rating greater than 4.5 to make sure the algorithm will only work on good recipes
df = DataFrame(list(recipesCol.find({"recipe_title": {"$regex": recipeType,"$options" :'i'}, "rating": { "$gte": 4.5 }})))
print(df.head())
print(len(df))
print(df["recipe_title"].head())
print(df["rating"].head())
##


#
## Clusering

#First runs Kmeans clustering to find the best amount of clusters using silhouette_score
#It runs over all relevant columns and tests amounts of clusters from 2 to 8, runs clustering using fit_predict and 
#calculates silhouette_score to measure how accurate the clusters are.
#finds out the amount of clusters for which the silhouette score is the biggest, and returns it.
x = df.iloc[:, 21:]
x["serving_size"] = df["serving_size"]
x["total_tbs"] = df["total_tbs"]
# Saves all ingredient + direction names for later
cols = []
for col in x.columns:
    cols.append(col)


# Saves ingredient names and direction names to seperate them for later
ingredients = []
lastIngredientCol = x.columns.get_loc("zucchini")
print("ingredients index: ", x.iloc[:, :lastIngredientCol+1])
print("directions index: ",x.iloc[:, lastIngredientCol+1:])
for col in x.iloc[:, :lastIngredientCol+1]:
    ingredients.append(col)
directions = []
for col in x.iloc[:, lastIngredientCol+1:-2]:
    directions.append(col)

print("ingredients:", ingredients)
print("directions", directions)

#
# Our data has a lot of variables (900+), and many of them are 0
# Because of the many dimensions the model might not be able to predict properly
# So to optimize the clustering we'll preform PCA, to reduce the amount of variables to the meaningful ones


# # PCA will reduce the 900+ dimensions into 100 dimensions
from sklearn.decomposition import PCA

pca = PCA(n_components = 3)
pca.fit(x)
x_pca=pca.transform(x)
print(x_pca)
x = x_pca

#

sil = {}
for k in range(2,8):
    kmeans = clustering(n_clusters=k,random_state=0)
    cluster = kmeans.fit_predict(x)
    sil[k] = silhouette_score(x, cluster)
    print("K=",k, ' : ', sil[k])
max_sil = -1
max_k = 2
for k in range(2,8):
    if (sil[k] > max_sil):
        max_sil = sil[k]
        max_k = k
    
print("best k is: ", max_k, "and its silhouette score is: ", max_sil)

# using the best silhouette score found earlier, runs clustering and adds cluster number to the df
kmeans = clustering(n_clusters=max_k,random_state=0)  
f_cluster = kmeans.fit(x)

#Gets average recipe for every cluster using cluster_centers_
centers = f_cluster.cluster_centers_
X_projected = pca.inverse_transform(centers)
centers = X_projected

print(len(centers[0]))
print(centers)

# Builds df from cluster centers

df2 = pd.DataFrame(np.array(centers),columns=cols)
print("df2: ", df2)


results = []
# Prints recipes from new df
for i, row in df2.iterrows():
    ingredients_array = []
    directions_array = []
    print(recipeType," recipe #", i + 1, "has these ingredients: ")
    for col in ingredients:
        if row[col] > 1:
            ingredient = {col:round(row[col],2)}
            ingredients_array.append(ingredient)
    ingredients_array = sorted(ingredients_array, key=lambda x: list(x.values())[0], reverse=True)[:4]
    print(ingredients_array)
    for col in directions:
        if row[col] > 0.5:
            directions_array.append(col)
    directions_array = directions_array[:-2]
    directions_array = directions_array[:3]
    print("and is prepared in these ways:")
    print(directions_array)
    print("in the serving size:")
    serving_size = round(row["serving_size"])
    print(serving_size)
    print("with the tbs total:")
    total_tbs = round(row["total_tbs"])
    print(total_tbs)

    results.append({str(i): [{"ingredients": ingredients_array},{"directions":directions_array},{"serving_size": str(serving_size)},{"total_tbs": str(total_tbs)}]}) 

print(results)




#
