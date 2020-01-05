from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import shelve


class Crawler:
    def __init__(self):
        self.class_names = None
        self.number_grades = None
        self.letter_grades = None

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def navigate(self, user, pasw):
        self.driver.get("https://accounts.veracross.com/aof/portals/login")
        username = self.driver.find_element_by_name("username")
        username.send_keys(user, Keys.TAB)

        password = self.driver.find_element_by_name("password")
        password.send_keys(pasw, Keys.ENTER)

        self.driver.implicitly_wait(10)

        self.class_names = self.driver.find_elements_by_xpath("//a[@class='course-name']")
        self.number_grades = self.driver.find_elements_by_xpath("//span[@class='numeric-grade']")
        self.letter_grades = self.driver.find_elements_by_xpath("//span[@class='letter-grade']")

    def get_grades(self, num_classes):
        grades = []

        for i in range(num_classes):
            grades.append({self.class_names[i].text: self.number_grades[i].text})

        for i in range(num_classes):
            grades.append({self.class_names[i].text: self.letter_grades[i].text})

        self.driver.close()
        return grades
