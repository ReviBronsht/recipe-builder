from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import json


def find_one(wait, by, query, what):
    try:
        return wait.until(EC.presence_of_element_located((by, query)))
    except Exception as e:
        print("Unable to find " + what + ", due to:" + str(e))
        return None


def find_many(wait, by, query, what):
    try:
        return wait.until(EC.presence_of_all_elements_located((by, query)))
    except Exception as e:
        print("Unable to find " + what + ", due to:" + str(e))
        return None


PATH = "C:\Program Files (x86)\chromedriver.exe"
s = Service(PATH)
driver = webdriver.Chrome(service=s)
wait = WebDriverWait(driver, 15)
URL = "https://www.enchantedlearning.com/wordlist/cooking.shtml"

output_root = {"cooking_terms_root": []}

try:
    driver.get(URL)
    words_list = find_many(
        wait, By.XPATH, '//div[@class="wordlist-item"]', "Words")
    for word in words_list:
        word_obj = {"keyword": word.text}
        output_root["cooking_terms_root"].append(word_obj)
    print(output_root)
    with open("cooking_terms_ouput.json", "w", encoding='utf-8') as outfile:
        json.dump(output_root, outfile, ensure_ascii=False)
    print("saved json cooking_terms_ouput")

except NoSuchElementException as e:
    print(e)
except Exception as e:
    print(e)
finally:
    driver.quit()