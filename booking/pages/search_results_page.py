from selenium.webdriver.common.by import By
from booking.pages.base_page import BasePage
from booking.components.booking_report import BookingReport

class SearchResultsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_results(self):
        hotel_box = self.get_element((By.CSS_SELECTOR, 'div[data-results-container="1"]'))
        return BookingReport(hotel_box).pull_deal_box_attributes()
