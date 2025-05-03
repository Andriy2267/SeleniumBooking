from selenium import webdriver
from selenium.webdriver.chrome.service import Service

import booking.constrants as const
import os
from selenium.webdriver.common.by import By
from booking.bookingfiltration import BookingFiltration
from booking.bookingReport import BookingReport
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

class Booking(webdriver.Chrome):
    def __init__(self, teardown: bool = False, detach: bool = True):
        self.teardown = teardown

        options = webdriver.ChromeOptions()
        if detach:
            options.add_experimental_option("detach", True)

        service = Service(ChromeDriverManager().install())
        super().__init__(service=service, options=options)

        self.implicitly_wait(15)
        self.maximize_window()

    def __del__(self):
        if self.teardown:
            self.quit()

    def __enter__(self):
        return self

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency_code="USD"):
        wait = WebDriverWait(self, 10)

        currency_button = wait.until(ES.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')))
        currency_button.click()
        wait.until(ES.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[data-testid="selection-item"]')))
        currency_options = self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
        for option in currency_options:
            if currency_code in option.text:
                option.click()
                break

    def change_language(self, language="English (UK)"):
        wait = WebDriverWait(self, 10)

        select_language_element = wait.until(ES.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="header-language-picker-trigger"]')))
        select_language_element.click()
        wait.until(ES.presence_of_all_elements_located((By.CSS_SELECTOR, 'button[data-testid="header-language-picker-trigger"]')))
        language_options = self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
        for language_option in language_options:
            if language in language_option.text:
                language_option.click()
                break

    def select_place_to_go(self, place_to_go="Kyiv"):
        wait = WebDriverWait(self, 10)
        search_field = wait.until(ES.element_to_be_clickable((By.ID, ':rh:')))
        search_field.clear()
        search_field.send_keys(place_to_go)
        select_first_element = wait.until(ES.element_to_be_clickable((By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')))
        select_first_element.click()

    def select_dates(self, checkin, checkout):
        wait = WebDriverWait(self, 10)
        select_checkin_element = wait.until(ES.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{checkin}"]')))
        select_checkin_element.click()

        select_checkout_element = wait.until(ES.element_to_be_clickable((By.CSS_SELECTOR, f'span[data-date="{checkout}"]')))
        select_checkout_element.click()

    def select_adults(self, adult_count=2):
        wait = WebDriverWait(self, 10)

        occupancy_button = wait.until(
            ES.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]')))
        occupancy_button.click()

        input_xpath = '//label[contains(text(),"Adults")]/following::input[1]'
        wait.until(ES.presence_of_element_located((By.XPATH, input_xpath)))

        while True:
            try:
                value_element = wait.until(ES.presence_of_element_located((By.XPATH, input_xpath)))
                value = int(value_element.get_attribute("value"))

                if value <= 1:
                    break

                minus_button = wait.until(
                    ES.element_to_be_clickable((By.XPATH, '//label[contains(text(),"Adults")]/following::button[1]')))
                minus_button.click()
            except Exception as e:
                print("Error:", e)
                break

        for _ in range(adult_count - 1):
            try:
                plus_button = wait.until(
                    ES.element_to_be_clickable((By.XPATH, '//label[contains(text(),"Adults")]/following::button[2]')))
                plus_button.click()
            except Exception as e:
                print("Error:", e)
                break

    def click_search(self):
        wait = WebDriverWait(self, 10)
        search_element = wait.until(ES.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]')))
        search_element.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.apply_star_rating(4)

    def report_results(self):
        wait = WebDriverWait(self, 10)
        hotel_boxes = wait.until(ES.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-results-container="1"]')))
        report = BookingReport(hotel_boxes)
        print(report.pull_deal_box_attributes())
