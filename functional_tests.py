from selenium import webdriver
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
        self.fail('Finish the test!')
        # He is invited to start detailing his play immediately
        # He types "I got crushed" into a text area (Brett is running bad)
        # When he hits enter, the page updates, and now the page lists
        # "Sess 1: I got crushed" as the first session
        # There is still a text area inviting him to enter another session.
        # He enters "Bad beats everywhere" (Brett continues his run bad)
        # The page updates again and now shows both sessions
        # Brett wonders if the site will remember his session. Then he sees
        # that the site has generated a unique URL for him -- there is some
        # explanatory text to that effect.
        # He visits the URL - his sessions are still there
        # Satisfied, he starts watching poker videos.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
    
