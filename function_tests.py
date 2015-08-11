from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
#import time


class NewVisitorTest(unittest.TestCase):

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
        self.browser.get('http://localhost:8000')

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

        # When he hits enter, the page updates, and now the page lists
        # "1: go to dentist" as a item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.check_for_row_in_list_table('1: go to dentist')

        # There is still a text box inviting him to add another item.
        # He enters, "finish TDD tutorial and praise our goat overlord"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('finish TDD tutorial and praise our goat overlord')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and now shows both items on his list
        self.check_for_row_in_list_table('1: go to dentist')
        self.check_for_row_in_list_table('2: finish TDD tutorial and praise our goat overlord')


        # Chris wonders whether the site will remember his list. He then
        # that the site has generated a unique URL for him -- there is
        # some explainatory text to that effect.
        self.fail('Finish the test!')
        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()
