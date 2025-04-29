from selenium import webdriver
import booking.constrants as const
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:\Users\ASUS\Desktop\ChromeDriver\chrome-win64", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] = self.driver_path

        # Add Chrome Options
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)

        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    def __enter__(self):
        return self

    def land_first_page(self):
        self.get(const.BASE_URL)

    def change_currency(self, currency_code="USD"):
        # Клік на кнопку вибору валюти
        currency_button = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_button.click()
        time.sleep(2)  # Зачекай, поки відкриється меню

        # Знайти всі елементи валют
        currency_options = self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
        print(currency_options)
        for option in currency_options:
            if currency_code in option.text:
                option.click()
                break
        time.sleep(2)  # Зачекай, поки зміна валюти набуде чинності


    def select_place_to_go(self, place_to_go):
        search_field = self.find_element(By.ID, ':rh:')
        search_field.clear()
        search_field.send_keys(place_to_go)

        select_first = self.find_element(By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]')
        select_first.click()

    def select_dates(self, checkin, checkout):
        checkin_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{checkin}"]')
        checkin_element.click()

        checkout_element = self.find_element(By.CSS_SELECTOR, f'span[data-date="{checkout}"]')
        checkout_element.click()

    def select_adults(self, adult_count=1):
        self.find_element(By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]').click()
        time.sleep(1)

        # Зменшити до мінімуму (1 дорослий)
        while True:
            try:
                value_element = self.find_element(By.XPATH, '//label[contains(text(),"Дорослі")]/following::input[1]')
                value = int(value_element.get_attribute("value"))

                if value <= 1:
                    break

                minus_button = self.find_element(By.XPATH, '//label[contains(text(),"Дорослі")]/following::button[1]')
                minus_button.click()
                time.sleep(0.2)
            except Exception as e:
                print("Помилка зменшення:", e)
                break

        # Збільшити до бажаної кількості
        for _ in range(adult_count - 1):
            plus_button = self.find_element(By.XPATH, '//label[contains(text(),"Дорослі")]/following::button[2]')
            plus_button.click()
            time.sleep(0.2)

    def click_search(self):
        search_element = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_element.click()