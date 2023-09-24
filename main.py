import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

from parametrs import *


class HousesForRent:
    def __init__(self):
        self.response = requests.get(url=SEARCH_URL)
        self.search_page = BeautifulSoup(self.response.text, "html.parser")
        self.house_links = []
        self.house_prices = []
        self.house_addresses = []

    def get_house_links(self):
        links_list = self.search_page.select("h2 > a")
        links = [f"{URL_PREFIX}{link['href']}" for link in links_list]
        self.house_links = links

    def get_house_prices(self):
        prices_list = self.search_page.select("#minimumRent")
        prices = [price.text.replace('â\x82¹ ', u"\u20B9") for price in prices_list]
        self.house_prices = prices

    def get_house_addresses(self):
        address_list = self.search_page.select(
            'div[itemtype="http://schema.org/Apartment"] > section > div > div > div')
        addresses = [address.text for address in address_list]
        self.house_addresses = addresses


class FillGoogleForm:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)

        self.house_details = HousesForRent()
        self.house_details.get_house_links()
        self.house_details.get_house_prices()
        self.house_details.get_house_addresses()

    def fill_the_form(self):
        for address, price, link in zip(self.house_details.house_addresses, self.house_details.house_prices,
                                        self.house_details.house_links):
            self.driver.get(url=FORM_URL)
            time.sleep(1)
            text_boxes = self.driver.find_elements(by=By.CSS_SELECTOR, value='input[data-initial-dir="auto"]')
            text_boxes[0].send_keys(address)
            text_boxes[1].send_keys(price)
            text_boxes[2].send_keys(link)

            submit = self.driver.find_element(by=By.CSS_SELECTOR, value='div[role="button"]')
            submit.click()
        self.driver.quit()


f = FillGoogleForm()
f.fill_the_form()
