from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
#import time


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Chris hears about a cool new online to-do app. He goes
        # to check out its homepage
        self.browser.get(self.live_server_url)

        # Chris notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # He types "go to dentist" into a text box
        inputbox.send_keys('go to dentist')

        # When he hits enter, he is taken to a new URL,
        # and now the page lists "1: go to dentist"
        # as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        chris_list_url = self.browser.current_url
        self.assertRegex(chris_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: go to dentist')

        # There is still a text box inviting him to add another item.
        # He enters, "finish TDD tutorial and praise our goat overlord"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('finish TDD tutorial and praise our goat overlord')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items on his list
        self.check_for_row_in_list_table('1: go to dentist')
        self.check_for_row_in_list_table('2: finish TDD tutorial and praise our goat overlord')

        # Now a new user, Francis, comes along to the second_item

        ## We use a new browser session to make sure that no information of
        ## Chris's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis visits the home page. There is no sign of Chris's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('go to dentist', page_text)
        self.assertNotIn('finish TDD tutorial and praise our goat overlord', page_text)

        # Francis starts a new list by entering a new item. he is
        # less interesting than Chris
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # Francis gets his own unique URL
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, chris_list_url)

        # Again, there is no trace of Chris's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('go to dentist', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep
