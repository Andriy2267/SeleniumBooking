from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def close_genius_popup(self):
        try:
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss sign in information.']"))
            )
            close_button.click()
            print("Genius pop-up закрито.")
        except (TimeoutException, NoSuchElementException):
            print("Genius pop-up не з’явився.")

    def apply_star_rating(self, star_value: int):
        if star_value not in [2, 3, 4, 5]:
            raise ValueError("Допустимі значення зірок: 2, 3, 4, 5")

        try:
            xpath = f"//div[@data-filters-group='class']//label[contains(., '{star_value} stars')]"
            star_checkbox_label = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", star_checkbox_label)

            WebDriverWait(self.driver, 1).until(lambda d: star_checkbox_label.is_displayed())

            self.driver.execute_script("arguments[0].click();", star_checkbox_label)

            print(f"Застосовано фільтр на {star_value} зірок.")
        except Exception as e:
            print(f"Не вдалося застосувати фільтр для {star_value} зірок: {e}")
