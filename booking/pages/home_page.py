from selenium.webdriver.common.by import By
from booking.pages.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def open(self, url):
        self.driver.get(url)

    def change_currency(self, currency_code):
        self.click((By.CSS_SELECTOR, 'button[data-testid="header-currency-picker-trigger"]'))
        for option in self.get_elements((By.CSS_SELECTOR, 'button[data-testid="selection-item"]')):
            if currency_code in option.text:
                option.click()
                break

    def change_language(self, language_text):
        self.click((By.CSS_SELECTOR, 'button[data-testid="header-language-picker-trigger"]'))
        for option in self.get_elements((By.CSS_SELECTOR, 'button[data-testid="selection-item"]')):
            if language_text in option.text:
                option.click()
                break

    def select_place_to_go(self, destination):
        self.send_keys((By.ID, ':rh:'), destination)
        self.click((By.CSS_SELECTOR, 'li[id="autocomplete-result-0"]'))

    def select_dates(self, checkin, checkout):
        self.click((By.CSS_SELECTOR, f'span[data-date="{checkin}"]'))
        self.click((By.CSS_SELECTOR, f'span[data-date="{checkout}"]'))

    def set_adults(self, adult_count=2):
        self.click((By.CSS_SELECTOR, 'button[data-testid="occupancy-config"]'))

        input_locator = (By.XPATH, '//label[contains(text(),"Adults")]/following::input[1]')
        value = int(self.get_element(input_locator).get_attribute("value"))

        while value > 1:
            self.click((By.XPATH, '//label[contains(text(),"Adults")]/following::button[1]'))
            value = int(self.get_element(input_locator).get_attribute("value"))

        for _ in range(adult_count - 1):
            self.click((By.XPATH, '//label[contains(text(),"Adults")]/following::button[2]'))

    def click_search(self):
        self.click((By.CSS_SELECTOR, 'button[type="submit"]'))
