from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import json

base_url = "https://www.mcdonalds.com"

def init_driver(driver_path, headless=True):
    """Initializes the browser driver."""
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    service = Service(driver_path)
    return webdriver.Chrome(service=service, options=chrome_options)

def clean_value(value):
    """Cleans the value from unnecessary symbols and formats."""
    if 'N/A' in value:
        return '0'
    match = re.match(r"(.*?)(?=\s[A-ZА-Я])", value)
    return match.group(1).strip() if match else value.strip()

def parse_nutrition(soup: BeautifulSoup):
    """Parses nutrition information of a product."""
    nutrition_info = {}
    name_tag = soup.find("span", class_="cmp-product-details-main__heading-title")
    description_tag = soup.find("span", class_="body") or soup.find("div", class_="cmp-text")

    if name_tag:
        nutrition_info['name'] = name_tag.get_text(strip=True)

    description_text = description_tag.get_text(strip=True)
    nutrition_info['description'] = description_text.replace('\xa0', ' ').replace('\n', ' ')

    nutrition_items_primary = soup.find_all("li", class_="cmp-nutrition-summary__heading-primary-item")
    nutrition_items_secondary = soup.find_all("li", class_="label-item")

    for item in nutrition_items_primary:
        value_span = item.find("span", class_="value")
        metric_span = item.find("span", class_="metric")

        if value_span and metric_span:
            value = clean_value(value_span.get_text(strip=True).split('\n')[0])
            metric = metric_span.get_text(strip=True)

            if "Калорійність" in metric:
                nutrition_info['calories'] = value
            elif "Жири" in metric:
                nutrition_info['fats'] = value
            elif "Вуглеводи" in metric:
                nutrition_info['carbs'] = value
            elif "Білки" in metric:
                nutrition_info['proteins'] = value

    for item in nutrition_items_secondary:
        value_span = item.find("span", class_="value").find_all("span", recursive=False)[0]
        metric_span = item.find("span", class_="metric")

        if value_span and metric_span:
            value = clean_value(value_span.get_text(strip=True).split('\n')[0].split(' ')[0])
            metric = metric_span.get_text(strip=True)

            if "НЖК" in metric:
                nutrition_info['unsaturated_fats'] = value
            elif "Цукор" in metric:
                nutrition_info['sugar'] = value
            elif "Сіль" in metric:
                nutrition_info['salt'] = value
            elif "Порція" in metric:
                nutrition_info['portion'] = value

    return nutrition_info

def parse_product_page(driver, url):
    """Parses a product page by the given URL."""
    driver.get(url)
    time.sleep(1)
    product_html = driver.page_source
    soup = BeautifulSoup(product_html, "lxml")
    return parse_nutrition(soup)

def parse_menu(driver, url):
    """Parses the full menu from the main page."""
    all_products = []
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")

    products = soup.find_all("li", class_="cmp-category__item")
    for product in products:
        a_tag = product.find("a", href=True)
        if a_tag:
            product_url = base_url + a_tag['href'] + "#accordion-29309a7a60-item-9ea8a10642"
            nutrition_info = parse_product_page(driver, product_url)
            all_products.append(nutrition_info)

    return all_products

def save_to_json(data, file_name):
    """Saves data to a JSON file."""
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_all_products():
    driver_path = 'chromedriver.exe'  #for Chrome version 128
    driver = init_driver(driver_path)

    try:
        return parse_menu(driver, "https://www.mcdonalds.com/ua/uk-ua/eat/fullmenu.html")
    finally:
        driver.quit()


all_products = get_all_products()
save_to_json(all_products, 'products.json')