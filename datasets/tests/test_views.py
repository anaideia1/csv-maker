import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

from datasets.models import SchemaColumn


class TestLogin(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_login(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.ID, 'id_username').send_keys("admin")
        self.driver.find_element(By.ID, 'id_password').send_keys("admin")
        self.driver.find_element(By.ID, 'submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def test_logout(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.ID, 'id_username').send_keys("admin")
        self.driver.find_element(By.ID, 'id_password').send_keys("admin")
        self.driver.find_element(By.ID, 'submit').click()
        self.driver.find_element(By.ID, 'id_logout').click()
        self.assertIn(
            "http://localhost:8000/accounts/login/",
            self.driver.current_url
        )

    def tearDown(self):
        self.driver.quit()


class TestSchemaAdd(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:8000/accounts/login/")
        self.driver.find_element(By.ID, 'id_username').send_keys("admin")
        self.driver.find_element(By.ID, 'id_password').send_keys("admin")
        self.driver.find_element(By.ID, 'submit').click()

    def test_schema_add_link(self):
        self.driver.get("http://localhost:8000/")
        self.driver.find_element(By.ID, 'id_schema_add').click()
        self.assertIn("http://localhost:8000/create/", self.driver.current_url)

    def test_schema_add_form_with_one_column(self):
        self.driver.get("http://localhost:8000/create/")
        self.driver.find_element(By.ID, 'id_name').send_keys("first_schema")
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-0-order'
        ).send_keys(1)
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-0-name'
        ).send_keys("admin")
        self.driver.find_element(By.ID, 'submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def test_schema_add_form_with_two_column(self):
        self.driver.get("http://localhost:8000/create/")
        self.driver.find_element(By.ID, 'id_name').send_keys("second_schema")
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-0-order'
        ).send_keys(1)
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-0-name'
        ).send_keys("first")
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-0-field_type'
        ).send_keys(SchemaColumn.PHONE)
        self.driver.find_element(By.ID, 'add-column').click()
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-1-order'
        ).send_keys(2)
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-1-name'
        ).send_keys("second")
        self.driver.find_element(
            By.ID, 'id_schemacolumn_set-1-field_type'
        ).send_keys(SchemaColumn.JOB)
        self.driver.find_element(By.ID, 'submit').click()
        self.assertIn("http://localhost:8000/", self.driver.current_url)

    def tearDown(self):
        self.driver.quit()

