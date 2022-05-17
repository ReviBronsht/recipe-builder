#imports
from os import name
import pymongo
import pandas as pd
from pandas import DataFrame
import unicodedata
from word2number import w2n

## Get database for normalization
#
#Using pymongo gets the db and the collection 
#before it's normalized from mongoDB
#Saves the collection as pandas dataframe
client = pymongo.MongoClient()
recipeDB = client["recipeDB"]
recipesCol = recipeDB["recipes"]

df = DataFrame(list(recipesCol.find({})))
print(df.head())
print(len(df))
##

## Setting normalization functions
#

# setting lcs function to find the longest common subsequence to match amounts that are written differently
def lcs(X, Y):
    n = len(Y)
    m = len(X)
    L = [[None]*(n + 1) for i in range(m + 1)]
    for i in range(m + 1): 
        for j in range(n + 1): 
            if i == 0 or j == 0 : 
                L[i][j] = 0
            elif X[i-1] == Y[j-1]: 
                L[i][j] = L[i-1][j-1]+1
            else: 
                L[i][j] = max(L[i-1][j], L[i][j-1])            
    return L[m][n]

# get amount gets an ingredient sentence and uses a measurement keywords array to find the measurement (with lcs and helping function get_normal_num)
# it converts amounts that are written like words with w2n and normalizes fractions with unicodedata.numberic
def get_normal_num(num, total_sum):
    fraq = 0.0
    if num.isnumeric():
        try:
                     total_sum = total_sum +  unicodedata.numeric(num) 
        except:
                     total_sum = total_sum + float(num)
        return total_sum
    elif "/" in num :
        fraq = num.split("/")
        if fraq[0].isnumeric() and fraq[1].isnumeric():
            fraq = float(float(fraq[0])/float(fraq[1]))
            total_sum = total_sum + fraq
        return total_sum
    else:
        return 0
    
def get_amount(sentence):
    measurements = ["tbsp","tsp","oz","ounce","fl","qt","pt","gal","lb","pound","ml","kg","cup","gram","liter"]
    amount = ""
    sentence = sentence.lower().replace(',','').replace('.','')
    sentence_list = sentence.split()
    total_sum = 0.0
    measurement = ""
    measure = ""
    for word in enumerate(sentence_list):
         try:
             word = w2n.word_to_num(word)
         except:
             pass
    amount1 = sentence_list[0]
    temp = get_normal_num(amount1,total_sum)
    if temp != 0:
        total_sum = temp
    if len(sentence_list) > 1:
        measure = sentence_list[1]
        amount2 = sentence_list[1]
        temp = get_normal_num(amount2,total_sum)
        if temp != 0:
             total_sum = temp
             if len(sentence_list) > 2:
                measure = sentence_list[2]
    for i in measurements:
                  if lcs(measure,i) == len(i):
                      measurement = i
                      break
    if total_sum == 0.0:
        return ""
    else:
        if measurement == "":
                amount = str(total_sum)
        else:
                amount = str(total_sum) + " " + measurement
        return amount

# ingredient normalize finds all the keywords present in the ingredient sentence using in
# then gets the longest one to avoid situations where one ingredient contains another
# (like 'banana peel' would return 'eel')
# it activates the get_amount function to return the amount of the ingredient
def ingredient_normalize(old_list, keywords):
    new_list = []
    amount_list = []
    for sentence in old_list:
        temp_list = [""]
        sentence = sentence.lower()
        for keyword in keywords:
            if keyword in sentence:
                temp_list.append(keyword)
        ingredient = max(temp_list, key=len)
        new_list.append(ingredient)
        while '' in new_list:
            new_list.remove('')
        if ingredient != "":
                amount = get_amount(sentence)
                amount_list.append(amount)
    return pd.Series([new_list, amount_list])

# directions normalize finds all the directions keywords in the direction sentence and returns them
#since there are no directions keywords that have spaces in them (unlike ingredients) its ok to use split.
def direction_normalize(old_list, keywords):
    new_list = []
    for sentence in old_list:
        sentence = sentence.lower().replace(',','').replace('.','')
        sentence_list = sentence.split()
        for keyword in keywords:
            if keyword in sentence_list:
                new_list.append(keyword)
    return new_list

#finds classes relvant to ingredient names and adds them in a new column
def add_class(old_list,dataF):
    new_list = []
    for word in old_list:
        word_cat = dataF[dataF['ingredient_name'] == word]
        for cat in word_cat["category"]:
            new_list.append(cat)
    return new_list

#unique values will return distinct values of a list where more than one value shouldn't appear twice
def unique_values(old_list):
    new_list = []
    for word in old_list:
        if word not in new_list:
            new_list.append(word)
    return new_list
##

###~ Normalization ~~##

## Creating a temp_df to normalize and deleting invalid recipes
#
temp_df = df

#deletes duplicate recipes
temp_df = temp_df.drop_duplicates(subset=['recipe_title'])

#deletes recipes with essential missing values
temp_df = temp_df.drop(temp_df.index[temp_df['ingredients'].isnull()])
temp_df = temp_df.drop(temp_df.index[temp_df['directions'].isnull()])
temp_df = temp_df.drop(temp_df.index[temp_df['rating'].isnull()])
temp_df = temp_df.drop(temp_df.index[temp_df['serving_size'].isnull()])
temp_df = temp_df.drop(temp_df.index[temp_df['calories'].isnull()])

print(len(temp_df))
##

#fixing field types 
temp_df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
temp_df['serving_size'] = pd.to_numeric(df['serving_size'], errors='coerce')
temp_df['calories'] = pd.to_numeric(df['calories'], errors='coerce')
temp_df = temp_df.dropna(subset=['rating', 'serving_size','calories'])



## Normalizing Ingredient names
#
# gets the ingredient_names keywords and uses the keyword normalize function to create a new column with the ingredients as names
print(temp_df['ingredients'].head())

ingredientsCol = recipeDB["ingredients"]
ingredientsDF = DataFrame(list(ingredientsCol.find({})))
ingredient_names = ingredientsDF['ingredient_name']

temp_df[['normalized_ingredients','normalized_amounts']] = temp_df['ingredients'].apply(ingredient_normalize,args=[ingredient_names])
temp_df['normalized_categories'] = temp_df['normalized_ingredients'].apply(add_class,args=[ingredientsDF])
print(temp_df['ingredients'].head(),temp_df['normalized_ingredients'].head(),temp_df['normalized_categories'].head())
##

## Normalizing Directions names
#
# gets the directions_names keywords from the collection in the db 
# and uses the keyword normalize function to create a new column with the ingredients as names
# gets only the unique cooking directions keywords so they don't repeat themselves
print(temp_df['directions'].head())

directionsCol = recipeDB["directions_keywords"]
directionsDF = DataFrame(list(directionsCol.find({})))
directions_names = directionsDF['keyword']

temp_df['directions_keywords'] = temp_df['directions'].apply(direction_normalize,args=[directions_names])
temp_df['directions_keywords'] = temp_df['directions_keywords'].apply(unique_values)
print(temp_df['directions'].head(),temp_df['directions_keywords'].head())
##



######

## Saving the dataframe to new db in MongoDB
#
#Creates a new db with a new collection, saves the df as dictionary in records format
#and inserts into the collection
new_recipeDB = client["new_recipeDB"]
new_recipesCol = new_recipeDB["recipes"]
data = temp_df.to_dict("records")
for recipe in data:
    new_recipesCol.insert_one(recipe)
#