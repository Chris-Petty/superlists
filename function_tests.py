from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get('http://localhost:8000')

        # Chris notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # He is invited to enter a to-do item straight away

        # He types "go to dentist" into a text box

        # When he hits enter, the page updates, and now the page lists
        # "1: go to dentist" as a item in a to-do list

        # There is still a text box inviting him to add another item.
        # He enters, "finish TDD tutorial and Praise our goat overlord"

        # The page updates again and now shows both items on his list

        # Chris wonders whether the site will remember his list. He then
        # that the site has generated a unique URL for him -- there is
        # some explainatory text to that effect.

        # He visits that URL - his to-do list is still there.

        # Satisfied, he goes back to sleep

if __name__ == '__main__':
    unittest.main()
