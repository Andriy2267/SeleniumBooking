from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def apply_star_rating(self, stars: int):
        wait = WebDriverWait(self.driver, 10)

        if stars not in [2, 3, 4, 5]:
            raise ValueError("Star rating must be between 2 and 5")

        checkbox_value = f'class={stars}'

        checkbox = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'input[name="{checkbox_value}"]'))
        )

        checkbox_id = checkbox.get_attribute("id")

        label = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'label[for="{checkbox_id}"]'))
        )

        label.click()
