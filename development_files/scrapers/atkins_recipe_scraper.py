from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException
#import time
import json
from selenium.common.exceptions import NoSuchElementException
#100 recipes per hour

def find_one(driver, wait, by, query, what):
    try:
        return wait.until(EC.presence_of_element_located((by, query)))
    except Exception as e:
        print("Unable to find " + what + ", due to:" + str(e))
        return None


def find_many(driver, wait, by, query, what):
    try:
        if wait == None:
            elements = driver.find_elements(by, query)
            return None if len(elements) == 0 else elements
        else:
            return wait.until(EC.presence_of_all_elements_located((by, query)))
    except Exception as e:
        print("Unable to find " + what + ", due to:" + str(e))
        # template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        # message = template.format(type(ex).__name__, ex.args)
        # print(message)
        return None

PATH = "C:\Program Files (x86)\chromedriver.exe"
# PATH = "C:\geckodriver.exe"
s = Service(PATH)

driver = webdriver.Chrome(service=s) #, options=options)
wait = WebDriverWait(driver, 5)
URL = "https://www.atkins.com/recipes"

try:
    RECIPES_TYPES_PATH = '//ul[@class="small-block-grid-2 medium-block-grid-3 large-block-grid-4 recipes-explore"]/li/a/img'
    categories = [
        # {
        #     "url": "https://www.atkins.com/recipes/breakfast", V
        #     "pages": 12
        # },
        # {
        #     "url": "https://www.atkins.com/recipes/entree", V
        #     "pages": 50
        # },
        # {
        #     "url": "https://www.atkins.com/recipes/snacks", V
        #     "pages": 10
        # },
        # {
        #     "url": "https://www.atkins.com/recipes/sides", V
        #     "pages": 13
        # },
        # {
        #     "url": "https://www.atkins.com/recipes/gluten-free", V
        #     "pages": 75,
        #     "diet": "gluten free"
        # },
        # {
        #     "url": "https://www.atkins.com/recipes/desserts", V
        #     "pages": 11
        # },
        # {
        #     "url": "https://www.atkins.com/recipes/beverages", V
        #     "pages": 6
        # }
    ]

    diet_keywords = ["keto","gluten free","vegan","vegetarian","mediterranean"]

    recipe_book_root = {"recipe-book":[]}
    recipe_book = recipe_book_root["recipe-book"]

    for i in range(len(categories)):
        category = categories[i]
        for page in range(1, category["pages"] + 1):
            page_url = category["url"] + "?page=" + str(page)
            driver.get(page_url)
            print("Working on url: " + page_url)
            r_listings = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//ul[@class="small-block-grid-2 medium-block-grid-4 recipes-explore category"]/li/a/div/img')))
            for j in range(len(r_listings)):
                try:
                    r_listing = r_listings[j]
                    driver.execute_script("arguments[0].scrollIntoView();", r_listing)
                    print("clicking on " + r_listing.get_attribute("src"))
                    driver.execute_script("arguments[0].click();", r_listing)
                    # driver.get("https://www.atkins.com/recipes/poached-eggs-over-tomato-avocado-and-muenster/1257")
                    recipe = {"recipe_source": "atkins.com"}
                    recipe_title_element = find_one(driver,wait, By.XPATH, '//div[@class="columns medium-9"]/h1',"Recipe Title")
                    if recipe_title_element:
                        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                        recipe["recipe_title"] = recipe_title_element.text
                        image_element = find_one(driver,wait, By.XPATH, '//img[@class="recipes-detail-photo-image"]',"Recipe Image")
                        recipe["image_url"] = image_element.get_attribute('src')
                        extra_details_element = find_one(driver,wait,By.XPATH,'//div[@class="recipes-detail-info"]/div',"Extra Details")
                        prep_time_element = extra_details_element.text.split("Prep Time: ")[1].split("\n")[0].split(" Minutes")[0]
                        recipe["prep_time"] = prep_time_element + " mins"
                        cook_time_element = extra_details_element.text.split("Cook Time: ")[1].split("\n")[0].split(" Minutes")[0]
                        recipe["cook_time"] = cook_time_element + " mins"
                        calories_element = find_one(driver,wait,By.XPATH,'//div[@class="large-5 columns recipes-detail-stats"]/div[4]/strong',"Calories").text.split("cal")[0]
                        recipe["calories"] = calories_element
                        serving_size_element = find_one(driver,wait,By.XPATH,'//select[@id="servingSize"]/option[@selected="selected"]',"Serving Size")
                        if serving_size_element:
                            recipe["serving_size"] = serving_size_element.get_attribute("value")
                        recipe["diets"] = ["low-carb"]
                        matched_diet_keywords = list(filter(lambda keyword : keyword in recipe["recipe_title"].lower(), diet_keywords))
                        recipe["diets"].extend(matched_diet_keywords)
                        if ("diet" in category) and (category["diet"] in recipe["recipe_title"]) and (category["diet"] not in recipe["diets"]):
                            recipe["diet"].append(category["diet"])
                        ingredients_list = find_many(driver,wait,By.XPATH, '//ul[@id="ingredientsList"]/li/div',"Ingredients List")
                        if ingredients_list:
                            recipe["ingredients"] = []
                            for i in ingredients_list:
                                recipe["ingredients"].append(i.text)
                            directions_list = find_many(driver,wait, By.XPATH, '//div[@class="large-7 columns recipes-detail-directions"]/ol/li/span',"Directions List")
                            if directions_list:
                                recipe["directions"] = []
                                for d in directions_list:
                                    recipe["directions"].append(d.text)
                            else:
                                directions_list = find_many(driver,wait, By.XPATH, '//div[@class="large-7 columns recipes-detail-directions"]/ol/li',"Directions List")
                                if directions_list:
                                    recipe["directions"] = []
                                    for d in directions_list:
                                        recipe["directions"].append(d.text)
                                else:
                                    directions_div = find_one(driver,wait, By.XPATH, '//div[@class="large-7 columns recipes-detail-directions"]',"Directions List")
                                    if directions_div:
                                        directions_parts = directions_div.text.split('\n')
                                        directions_parts.pop(0)
                                        direction_text = " ".join(directions_parts)
                                        recipe["directions"] = [direction_text]
                            #GET 2 things: 1. RATING, 2. COMMENTS
                            no_reviews_element = find_one(driver,wait, By.XPATH, '//div[@class="tt-c-reviews-summary__no-reivews-body tt-u-spacing--md"]',"No Reviews")
                            if no_reviews_element == None:
                                rating_element = find_one(driver,wait, By.XPATH, '//span[@class="tt-c-reviews-summary__rating-number"]',"Rating")
                                if rating_element:
                                    recipe["rating"] = float(rating_element.text)
                                    review_content_list = find_many(driver,wait, By.XPATH, '//span[@class="tt-c-review__text-content"]',"Review Content List")
                                    review_user_list = find_many(driver,wait, By.XPATH, '//span[@class="tt-o-byline__item tt-o-byline__author"]',"Review User List")
                                    if review_content_list and review_user_list:
                                        recipe["comments"] = []
                                        for review_index in range(len(review_content_list)):
                                            comment = {
                                                "user": review_user_list[review_index].text,
                                                "content": review_content_list[review_index].text
                                            }
                                            recipe["comments"].append(comment)
                            recipe_book.append(recipe)                   
                    driver.back()
                    r_listings = wait.until(EC.presence_of_all_elements_located((By.XPATH,'//ul[@class="small-block-grid-2 medium-block-grid-4 recipes-explore category"]/li/a/div/img')))
                except Exception as e:
                    print(e)
            print(recipe_book_root)
            with open("recipe_test.json","w", encoding='utf-8') as outfile:
                json.dump(recipe_book_root, outfile, ensure_ascii=False)
            print("saved json with page " + page_url)
except Exception as e:
    print(e)
finally:
    driver.quit()