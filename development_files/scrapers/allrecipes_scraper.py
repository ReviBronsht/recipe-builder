#imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

#setting variables
#diet_keywords for saving diets by correct names in db
#diet_filters for checking for additional diets from title
#main_diet for the diet of the category it was in
#site url for recipe source
diet_keywords = ["keto","gluten free","vegan","vegetarian","mediterranean","low-calorie","low-cholesterol","low-sodium","whole30","diabetic","low-carb","low-fat"]
diet_filter = ["keto","gluten","vegan","vegetarian","mediterranean","calorie","cholesterol","sodium","whole30","diabetic","carb","fat"]
site_url = "https://www.allrecipes.com/"

#setting up selenium
PATH = r"C:\Users\revib\Desktop\Python_test\chromedriver2\chromedriver.exe"
s = Service(PATH)
driver =  webdriver.Chrome(service=s)
wait = WebDriverWait(driver, 15)

#setting functions to find one element and many elements with try, except and wait
def find_one(driver, wait, by, query, what):
    try:
        return wait.until(EC.presence_of_element_located((by, query)))
    except Exception as e:
        print("Unable to find " + what)
        return None
def find_many(driver, wait, by, query, what):
    try:
        return wait.until(EC.presence_of_all_elements_located((by, query)))
    except Exception as e:
        print("Unable to find " + what)
        return None

##~
##Category
# Setting up the base category link and the limit of pages
#Scraping each category seperately instead of iterating over all of them allows to save 
#several files seperately to avoid crashing all of them at once if a crash does happen
##Gluten Free
#main_diet = "gluten free"
#age_limit = 50
#cat_link = "https://www.allrecipes.com/recipes/741/healthy-recipes/gluten-free/?page="
##Low Calorie
#main_diet = "low-calorie"
#page_limit = 40
#cat_link = "https://www.allrecipes.com/recipes/741/healthy-recipes/low-calorie/?page="
##Low Cholesterol
#main_diet = "low-cholesterol"
#page_limit = 50
#cat_link = "https://www.allrecipes.com/recipes/737/healthy-recipes/low-cholesterol/?page="
##Low Sodium
#main_diet = "low-sodium"
#page_limit = 50
#cat_link = "https://www.allrecipes.com/recipes/1788/healthy-recipes/low-sodium/?page="
##Whole30
#main_diet = "whole30"
#page_limit = 50
#cat_link = "https://www.allrecipes.com/recipes/22590/healthy-recipes/whole30/?page="
##Diabetic
#main_diet = "diabetic"
#page_limit = 17
#cat_link = "https://www.allrecipes.com/recipes/739/healthy-recipes/diabetic/?page="
##Keto
#main_diet = "keto"
#page_limit = 22
#cat_link = "https://www.allrecipes.com/recipes/22959/healthy-recipes/keto-diet/?page="
##Low carb
#main_diet = "low-carb"
#page_limit = 50
#cat_link = "https://www.allrecipes.com/recipes/742/healthy-recipes/low-carb/?page="
##Low fat
main_diet = "low-fat"
page_limit = 50
cat_link = "https://www.allrecipes.com/recipes/1231/healthy-recipes/low-fat/?page="
##Mediterranean
#main_diet = "mediterranean"
#page_limit = 10
#cat_link = "https://www.allrecipes.com/recipes/16704/healthy-recipes/mediterranean-diet/?page="
##
# Loop will iterate over every page of the category until the limit 
# and save all the recipe links for the category.
recipe_links = []
for x in range(2,page_limit):
    try:
        link = cat_link + str(x)
        driver.get(link)
        print("Entered page: " + str(x))
        for recipe in find_many(driver, wait, By.XPATH,"//*/a[@class='tout__titleLink elementFont__toutLink']","Link"):
            r_link = recipe.get_attribute("href")
            recipe_links.append(r_link)
    except:
        print("page not found")
        break
##~

##~
##Recipe

#
#getting data from current recipe
#
#saving recipes in recipe book root
recipe_book_root = {"recipe-book":[]}
recipe_book = recipe_book_root["recipe-book"]

# Second loop will iterate over all the recipes from the recipe link array and get their details
woo = 0
for r in recipe_links:
    try:
        driver.get(r)
        #getting recipe_source from set site_url
        recipe = {"recipe_source": site_url}
        # getting recipe_title by XPath
        title = find_one(driver, wait, By.XPATH, "//*/h1", "Recipe Title")
        if title:
                recipe["recipe_title"] = title.text
            # getting description by XPath
        description = find_one(
                driver, wait, By.XPATH, "//*/div[@class='recipe-summary elementFont__dek--within']/p", "Recipe Description")
        if description:
                recipe["description"] = description.text
            # getting image by Xpath
        image = find_one(driver, wait, By.XPATH,
                            "//*/div[@class='image-container']/div", "Recipe Image")
        if image:
                recipe["image"] = image.get_attribute("data-src")
            # getting cook time, serving size and prep time by Xpath
        #//*/div[@class='recipe-meta-item-header elementFont__subtitle--bold elementFont__transformCapitalize']
        #//*/div[@class='recipe-meta-item-body elementFont__subtitle']
        times_titles = find_many(driver, wait, By.XPATH,
                            "//*/div[@class='recipe-meta-item-header elementFont__subtitle--bold elementFont__transformCapitalize']", "Recipe Times")
        cook_index = -1
        prep_index = -1
        serving_index = -1

        if times_titles:
                indecies = []
                for i in times_titles:
                    indecies.append(i.text)
                if "Servings:" in indecies:
                    serving_index = indecies.index("Servings:")
                if "Prep:" in indecies:
                    prep_index = indecies.index("Prep:")
                if "Cook:" in indecies:
                    cook_index = indecies.index("Cook:")
                    

        times = find_many(driver, wait, By.XPATH,
                            "//*/div[@class='recipe-meta-item-body elementFont__subtitle']", "Recipe Times")
        if times:
                if cook_index != -1:
                    recipe["cook_time"] = times[cook_index].text
                else:
                    recipe["cook_time"] = "-"
                if prep_index != -1:
                    recipe["prep_time"] = times[prep_index].text
                else:
                    recipe["prep_time"] = "-"
                if serving_index != -1:
                    recipe["serving_size"] = times[serving_index].text
            # getting calories by Xpath
        cals = find_one(driver, wait, By.XPATH,
                            "//*/div[@class='section-body']", "Calories")
        if cals:
                recipe["calories"] = cals.text.split()[0]
            # getting diets
            # main_diet comes from category as set earlier
            # other diets come by checking the recipe title to see if there are any other diets mentioned there
        recipe["diets"] = [main_diet]
        for idx, val in enumerate(diet_filter):
                if diet_keywords[idx] != main_diet:
                    if val in title.text.lower():
                        recipe["diet"].append(diet_keywords[idx])
            # getting ingredients by iterating over relevant elements by XPATH
        ingredients_list = find_many(
                driver, wait, By.XPATH, "//*/span[@class='ingredients-item-name elementFont__body']", "Ingredients")
        if ingredients_list:
                recipe["ingredients"] = []
                for i in ingredients_list:
                    recipe["ingredients"].append(i.text)
            # getting directions ingredients by iterating over relevant elements by XPATH
        directions_list = find_many(
                driver, wait, By.XPATH, "//*/div[@class='section-body elementFont__body--paragraphWithin elementFont__body--linkWithin']//p", "Directions")
        if directions_list:
                recipe["directions"] = []
                for i in directions_list:
                    recipe["directions"].append(i.text)
            # getting rating by XPATH and using round to set it to the correct format
        rating = find_one(driver, wait, By.XPATH,
                            "//*/span[@class='review-star-text visually-hidden']", "Recipe Rating")
        if rating:
                rating = rating.text.split(" ")[1]
                rating = round(float(rating), 1)
                recipe["rating"] = str(rating)
        #getting comments by iterating over relevant elements by XPATH, once for users and once for content
        #then iterating over users (for matching index, could've also iterated over contents) and adding the user
        # and their matching content to recipe
        users = []
        contents = []
        reviewer_names_list = find_many(driver, wait, By.XPATH,"//*/div[@class='feedback__wrapper karma-main-column']//span[@class='reviewer__name']/a","Reviewer Name")
        if reviewer_names_list:
            for i in reviewer_names_list:
                users.append(i.text)
        reviews_list = find_many(driver, wait, By.XPATH,"//*/div[@class='feedback__wrapper karma-main-column']//div[@class='feedback__reviewBody elementFont__subtitle--within feedback__reviewBody--truncated']/p","Review")
        if reviews_list:
            for i in reviews_list:
                contents.append(i.text)
        if len(users) != 0:
            recipe["comments"] = []
            for idx, val in enumerate(users):
                comment = {
                            "user": val,
                            "content": contents[idx].replace('"', '')
                            }
                recipe["comments"].append(comment)
        #Saving current recipe
        print(recipe)
        recipe_book.append(recipe)
        print(woo, "/", len(recipe_links))
        woo += 1
    except:
        print(recipe)
        recipe_book.append(recipe)
        print("recipe not found")
        print(woo, "/", len(recipe_links))
        woo += 1
###~
#
#finalizing results
#
print(recipe_book_root)
#converting recipe to json and saving it as a json file
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(recipe_book_root, f, ensure_ascii=False)

#closing the tab
driver.quit()

