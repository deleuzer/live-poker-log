from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    def tearDown(self):
        self.browser.quit()
    def test_can_store_a_sesslog_and_get_it_later(self):
        # Brett hears about a poker session tracking website. He goes
        # to checkout the homepage.
        self.browser.get('http://localhost:8000')
        # He notices the page title and header mention poker sessions
        self.assertIn('Poker Chronicle', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Poker Chronicle', header_text)
        # He is invited to start detailing his play immediately
        textbox = self.browser.find_element_by_id('id_new_sess')
        self.assertEqual(
            textbox.get_attribute('placeholder'),
            'Describe session'
            )
        # He types "I got crushed" into a text area (Brett is running bad)
        textbox.send_keys('I got crushed')
        # When he submits the form, the page updates, and now the page lists
        # "Sess 1: I got crushed" as the first session
        textbox.submit()
        time.sleep(1)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == 'Sess 1: I got crushed' for row in rows),
            "New poker sess did not appear in table"
            )
        # There is still a text area inviting him to enter another session.
        # He enters "Bad beats everywhere" (Brett continues his run bad)
        self.fail('Finish the test!')

        # The page updates again and now shows both sessions
        # Brett wonders if the site will remember his session. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect.
        # He visits the URL - his sessions are still there
        # Satisfied, he starts watching poker videos.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
    
