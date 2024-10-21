import time

from django.test import TestCase
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


def test_home_page_firefox():
    selenium_webdriver = webdriver.Firefox()
    selenium_webdriver.get('http://127.0.0.1:8000/')
    time.sleep(2)
    assert 'Vítejte v eShop EVAKoberce' in selenium_webdriver.page_source


class GuiTestWithSelenium(TestCase):


    def test_home_page_chrome(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/')
        assert 'Vítejte v eShop EVAKoberce.' in selenium_webdriver.page_source

    def test_signup(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/accounts/signup/')
        time.sleep(2)
        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('TestUser1')
        time.sleep(2)
        first_name_field = selenium_webdriver.find_element(By.ID, 'id_first_name')
        first_name_field.send_keys('Name')
        time.sleep(2)
        last_name_field = selenium_webdriver.find_element(By.ID, 'id_last_name')
        last_name_field.send_keys('Surname')
        time.sleep(2)
        password1_field = selenium_webdriver.find_element(By.ID, 'id_password1')
        password1_field.send_keys('EVAdskj45!dfa@')
        time.sleep(2)
        date_of_birth_field = selenium_webdriver.find_element(By.ID, 'id_date_of_birth')
        date_of_birth_field.send_keys('06-05-2010')
        time.sleep(2)
        submit_button = selenium_webdriver.find_element(By.ID, 'id_submit')
        submit_button.send_keys(Keys.RETURN)

        assert 'Username:' in selenium_webdriver.page_source

    def test_signup_user_already_exists(self):
        selenium_webdriver = webdriver.Chrome()
        selenium_webdriver.get('http://127.0.0.1:8000/accounts/signup/')
        time.sleep(2)
        username_field = selenium_webdriver.find_element(By.ID, 'id_username')
        username_field.send_keys('TestUser1')
        time.sleep(2)
        first_name_field = selenium_webdriver.find_element(By.ID, 'id_first_name')
        first_name_field.send_keys('Name')
        time.sleep(2)
        last_name_field = selenium_webdriver.find_element(By.ID, 'id_last_name')
        last_name_field.send_keys('Surname')
        time.sleep(2)
        password1_field = selenium_webdriver.find_element(By.ID, 'id_password1')
        password1_field.send_keys('Surname')
        time.sleep(2)
        date_of_birth_field = selenium_webdriver.find_element(By.ID, 'id_date_of_birth')
        date_of_birth_field.send_keys('06-05-2010')
        time.sleep(2)
        submit_button = selenium_webdriver.find_element(By.ID, 'id_submit')
        submit_button.send_keys(Keys.RETURN)

        assert 'A user with that username already exists.'