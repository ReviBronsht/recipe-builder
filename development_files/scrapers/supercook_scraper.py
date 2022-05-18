from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
#from selenium.common.exceptions import TimeoutException
#import time
import json


def find_one(driver, wait, by, query, what):
    try:
        return wait.until(EC.presence_of_element_located((by, query)))
    except Exception as e:
        print("Unable to find " + what + ", due to:" + str(e))
        return None


def find_many(driver, wait, by, query, what):
    try:
        return wait.until(EC.presence_of_all_elements_located((by, query)))
    except Exception as e:
        print("Unable to find " + what + ", due to:" + str(e))
        return None


PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service=s)  # , options=options)
wait = WebDriverWait(driver, 15)
URL = "https://www.supercook.com/#/desktop"

#ingredient_category_list = ["Vegetables & Greens","Dairy & Eggs","Herbs & Spices","Baking","Sugar & Sweeteners","Fruits & Berries","Oils","Cheeses","Condiments & Relishes","Meats","Nuts & Seeds","Desserts & Sweet Snacks","Dressings & Vinegars","Sauces, Spreads & Dips","Bread & Salty Snacks","Wine, Beer & Spirits","Soups, Stews & Stocks","Poultry","Grains & Cereals","Beans, Peas & Lentils","Seasonings & Spice Blends","Beverages","Pasta","Dairy-Free & Meat Substitutes","Fish","Seafood & Seaweed","Pre-Made Doughs & Wrappers","Supplements"]
output_root = {"ingredients_root": []}

try:
    driver.get(URL)
    more_buttons = find_many(
        driver, wait, By.XPATH, '//a[@class="tags-mini-item more-tag tags-mini-item-desktop"]', "The 'More' button")
    if more_buttons:
        for button in more_buttons:
            button.click()
    ingredients_category_items_list = find_many(driver, wait, By.XPATH,
        '//div[@class="ingredients-category-item"]', "Ingredients Category Items List")
    # ingredients_type_listings = find_many(
    #     driver, wait, By.XPATH, '//h4[@class="ingredients-name ingredients-name-desktop"]', "Ingredient Categories")
    for ingredients_category_item in ingredients_category_items_list:
        ingredients_type = ingredients_category_item.find_element(By.CLASS_NAME,'ingredients-name')
        ingredient_category = ingredients_type.text
        print("Working on: " + ingredient_category)
        ingredients_list = ingredients_category_item.find_elements(By.CLASS_NAME,'tags-mini-item')
        for ingredient in ingredients_list:
            ingrdedient_obj = {
                "category": ingredient_category,
                "ingredient_name": ingredient.text
            }
            output_root["ingredients_root"].append(ingrdedient_obj)
    print(output_root)
    with open("supercook_ouput.json","w", encoding='utf-8') as outfile:
        json.dump(output_root, outfile, ensure_ascii=False)
    print("saved json supercook_ouput")

except NoSuchElementException as e:
    print(e)
except Exception as e:
    print(e)
finally:
    driver.quit()