from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    #def close_genius_popup(self):
     #   try:
      #      close_button = WebDriverWait(self.driver, 5).until(
       #         EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Dismiss sign in information.']"))
         #   )
          #  close_button.click()
           # print("Genius pop-up закрито.")
        #except (TimeoutException, NoSuchElementException):
         #   print("Genius pop-up не з’явився.")

    def apply_star_rating(self, stars: int):
        wait = WebDriverWait(self.driver, 10)

        # Перевірка, чи передане значення коректне
        if stars not in [2, 3, 4, 5]:
            raise ValueError("Star rating must be between 2 and 5")

        # Формуємо значення атрибуту name
        checkbox_value = f'class={stars}'

        # Чекаємо, поки елемент з потрібним значенням name з'явиться
        checkbox = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'input[name="{checkbox_value}"]'))
        )

        # Клік по <label> по for=ID input'а
        checkbox_id = checkbox.get_attribute("id")

        label = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, f'label[for="{checkbox_id}"]'))
        )

        label.click()
