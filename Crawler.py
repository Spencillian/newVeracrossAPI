from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


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

        try:
            for i, val in enumerate(self.number_grades):
                self.number_grades[i] = float(val.text[:-1])
        except TypeError:
            print(f"FormError: {val.text} is not the correct form to be processed into a float type")

    # TODO: Get rid the num_classes thing and just deliver all of them
    def get_grades(self):
        grades = []

        try:
            for i in range(len(self.number_grades) - 1):
                grades.append({"id": str(i), "name": self.class_names[i].text, "number": self.number_grades[i], "letter": self.letter_grades[i].text})

        except IndexError:
            print(f"No classes found. Most likely user and pass are wrong. Small chance that Veracross is down")
            return False

        self.driver.close()
        return grades
