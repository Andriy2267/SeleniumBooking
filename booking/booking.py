from selenium import webdriver
import booking.constrants as const
import os
from selenium.webdriver.common.by import By
from booking.bookingfiltration import BookingFiltration
import time
from booking.bookingReport import BookingReport

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
        currency_button = self.find_element(By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]')
        currency_button.click()
        time.sleep(2)

        currency_options = self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
        for option in currency_options:
            if currency_code in option.text:
                option.click()
                break
        time.sleep(2)

    def change_language(self, language="English (UK)"):
        select_language_element = self.find_element(By.CSS_SELECTOR,
                                                    'button[data-testid="header-language-picker-trigger"]')
        select_language_element.click()
        time.sleep(2)

        language_options = self.find_elements(By.CSS_SELECTOR, 'button[data-testid="selection-item"]')
        for language_option in language_options:
            if language in language_option.text:
                language_option.click()
                break

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

        while True:
            try:
                value_element = self.find_element(By.XPATH, '//label[contains(text(),"Adults")]/following::input[1]')
                value = int(value_element.get_attribute("value"))

                if value <= 1:
                    break

                minus_button = self.find_element(By.XPATH, '//label[contains(text(),"Adults")]/following::button[1]')
                minus_button.click()
                time.sleep(0.2)
            except Exception as e:
                print("Помилка зменшення:", e)
                break

        for _ in range(adult_count - 1):
            plus_button = self.find_element(By.XPATH, '//label[contains(text(),"Adults")]/following::button[2]')
            plus_button.click()
            time.sleep(0.2)

    def click_search(self):
        search_element = self.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        search_element.click()

    def apply_filtration(self):
        filtration = BookingFiltration(driver=self)
        filtration.close_genius_popup()
        filtration.apply_star_rating(4)

    def report_results(self):
        hotel_boxes = self.find_element(By.CSS_SELECTOR, 'div[data-results-container="1"]')
        report = BookingReport(hotel_boxes)
        print(report.pull_deal_box_attributes())
