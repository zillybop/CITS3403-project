import os
import sys
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Add project root to path for Flask imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestSelenium(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Flask test database
        from app import app as flask_app, db
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL', 'sqlite:///test.db')
        with flask_app.app_context():
            db.create_all()

        # Setup WebDriver
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        cls.driver = webdriver.Chrome(options=options)
        cls.base_url = os.getenv('APP_URL', 'http://localhost:5000')
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.test_user = os.getenv('TEST_USER')
        cls.test_pass = os.getenv('TEST_PASSWORD')

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def _click_submit(self):
        btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        btn.click()

    def _login(self, username=None, password=None):
        if not (self.test_user and self.test_pass):
            self.skipTest('TEST_USER and TEST_PASSWORD not set')
        user = username or self.test_user
        pwd = password or self.test_pass
        self.driver.get(f"{self.base_url}/login")
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username'))).clear()
        self.driver.find_element(By.NAME, 'username').send_keys(user)
        self.driver.find_element(By.NAME, 'password').send_keys(pwd)
        self._click_submit()
        self.wait.until(EC.url_contains('/introductory'))

    def test_register_login_logout(self):
        # End-to-end registration, logout, login
        unique = str(int(time.time()))
        username = f"testuser_{unique}"
        password = "TestPass123!"
        # Register
        self.driver.get(f"{self.base_url}/register")
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username'))).send_keys(username)
        pw_field = self.wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
        pw2_field = self.wait.until(EC.visibility_of_element_located((By.NAME, 'password2')))
        pw_field.send_keys(password)
        pw2_field.send_keys(password)
        self._click_submit()
        self.wait.until(EC.url_contains('/introductory'))
        # Logout
        self.driver.get(f"{self.base_url}/logout")
        # Back on intro page with login link
        login_link = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'Log in')))
        login_link.click()
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username')))
        # Login
        self._login(username, password)

    def test_invalid_login(self):
        # Invalid credentials shows login page again
        self.driver.get(f"{self.base_url}/login")
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username'))).send_keys('wrong')
        self.driver.find_element(By.NAME, 'password').send_keys('wrong')
        self._click_submit()
        # Should remain on /login and show flash
        self.wait.until(EC.url_contains('/login'))
        flash = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'alert-danger')))
        self.assertIn('invalid username or password', flash.text.lower())

    def test_duplicate_registration(self):
        # Attempt to register existing user -> inline error
        if not (self.test_user and self.test_pass):
            self.skipTest('TEST_USER and TEST_PASSWORD not set')
        self.driver.get(f"{self.base_url}/register")
        self.wait.until(EC.visibility_of_element_located((By.NAME, 'username'))).send_keys(self.test_user)
        pw_field = self.wait.until(EC.visibility_of_element_located((By.NAME, 'password')))
        pw2_field = self.wait.until(EC.visibility_of_element_located((By.NAME, 'password2')))
        pw_field.send_keys(self.test_pass)
        pw2_field.send_keys(self.test_pass)
        self._click_submit()
        # Inline validation error under username
        err = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.text-danger')))
        self.assertIn('already exists', err.text.lower())

    

if __name__ == '__main__':
    unittest.main()
