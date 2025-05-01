from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

class BookingReport:
    def __init__(self, boxes_section_element:WebElement):
        self.boxes_section_element = boxes_section_element
        self.deal_boxes = self.pull_deal_boxes()

    def pull_deal_boxes(self):
        return self.boxes_section_element.find_elements(By.CSS_SELECTOR, 'div[data-testid="property-card"]')

    def pull_deal_box_attributes(self):
        collection = []
        for deal_box in self.deal_boxes:
            hotel_name = deal_box.find_element(By.CSS_SELECTOR, 'div[data-testid="title"]').get_attribute('innerHTML').strip()
            hotel_price = deal_box.find_element(By.CSS_SELECTOR, 'span[data-testid="price-and-discounted-price"]').get_attribute('innerHTML').strip()
            hotel_score = deal_box.find_element(By.CSS_SELECTOR, 'div[class="f63b14ab7a dff2e52086"]').get_attribute('innerHTML').strip()

            collection.append(
                [hotel_name, hotel_price, hotel_score]
            )

        return collection