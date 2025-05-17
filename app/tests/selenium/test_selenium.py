from app import create_app, db
from app.config import TestConfig
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest

localHost = "http://127.0.0.1:5000/"

class SeleniumTests(unittest.TestCase):
    def add_test_data_to_db(self):
        from werkzeug.security import generate_password_hash
        from app.models import User

        existing_user = User.query.filter_by(username="seleniumuser").first()
        if not existing_user:
            test_user = User(username="seleniumuser")
            test_user.password_hash = generate_password_hash("testpass")
            db.session.add(test_user)
            db.session.commit()

    def setUp(self):
        self.testApp = create_app(TestConfig)
        self.app_context = self.testApp.app_context()
        self.app_context.push()
        db.create_all()
        self.add_test_data_to_db()

        self.server_thread = threading.Thread(target=self.testApp.run, kwargs={"use_reloader": False})
        self.server_thread.daemon = True
        self.server_thread.start()

        options = webdriver.ChromeOptions()
        #options.add_argument("--headless=new")
        options.add_argument("window-size=1200x800")
        self.driver = webdriver.Chrome(options=options)
    
    def tearDown(self):
        self.server_thread.join(timeout=1)
        self.driver.close()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_login(self):
        self.driver.get(localHost + "login")
        print(self.driver.page_source)

        wait = WebDriverWait(self.driver, 5)
        username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = self.driver.find_element(By.NAME, "password")
        submit_button = self.driver.find_element(By.XPATH, '//button[text()="Login"]')

        username_field.send_keys("seleniumuser")
        password_field.send_keys("testpass")
        submit_button.click()

        wait.until(EC.url_changes(localHost + "login"))
        self.assertIn("Logged in successfully.", self.driver.page_source)
