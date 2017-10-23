from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import os
import time

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
    def tearDown(self):
        self.browser.quit()
    def check_for_row_in_chronicle_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
    def wait_for_row_in_chronicle_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)
    def test_can_start_a_list_for_one_user(self):
        # Brett hears about a poker session tracking website. He goes
        # to checkout the homepage.
        self.browser.get(self.live_server_url)
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
        self.wait_for_row_in_chronicle_table('Sess 1: I got crushed')
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_chronicle_table('Sess 1: I got crushed')
        # There is still a text area inviting him to enter another session.
        # He enters "Bad beats everywhere" (Brett continues his run bad)
        textbox = self.browser.find_element_by_id('id_new_sess')
        textbox.send_keys('Bad beats everywhere')
        textbox.submit()
        self.wait_for_row_in_chronicle_table('Sess 2: Bad beats everywhere')
        self.wait_for_row_in_chronicle_table('Sess 1: I got crushed')
        # The page updates again and now shows both sessions
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.check_for_row_in_chronicle_table('Sess 1: I got crushed')
        self.check_for_row_in_chronicle_table('Sess 2: Bad beats everywhere')
        # Satisfied, he starts watching poker videos.
    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Brett starts a new group of chronicles
        self.browser.get(self.live_server_url)
        textbox = self.browser.find_element_by_id('id_new_sess')
        textbox.send_keys('Crushed this session')
        textbox.submit()
        self.wait_for_row_in_chronicle_table('Sess 1: Crushed this session')
        # He notices that the chronicles have a unique URL
        brett_chronicles_url = self.browser.current_url
        self.assertRegex(brett_chronicles_url, '/chronicles/.+')

        # Now a new user, Bo comes to the site.
        ## We use a new browser session to make sure no information
        ## of Brett's is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()
        # Bo visits the home page. There is no sign of Brett's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Crushed this session', page_text)
        self.assertNotIn('I got crushed', page_text)
        # Bo starts a new list by entering a new chronicle.
        # He is better than Brett.
        textbox = self.browser.find_element_by_id('id_new_sess')
        textbox.send_keys('Destroyed the morons')
        textbox.submit()
        self.wait_for_row_in_chronicle_table('Sess 1: Destroyed the morons')
        # Bo gets his own unique URL
        bo_chronicles_url = self.browser.current_url
        self.assertRegex(bo_chronicles_url, '/chronicles/.+')
        self.assertNotEqual(bo_chronicles_url, brett_chronicles_url)
        # Again, there is no trace of Brett's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Crushed this session', page_text)
        self.assertIn('Destroyed the morons', page_text)
        # Satisfied, they both go back to sleep.

    def test_layout_and_styling(self):
        # Brett goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        # He notices the text box is nicely centered
        textbox = self.browser.find_element_by_id('id_new_sess')
        self.assertAlmostEqual(
            textbox.location['x'] + textbox.size['width'] / 2,
            512,
            delta=10
        )
        # He starts a new list and sees the input is nicely
        # centered there too
        textbox.send_keys('testing')
        textbox.submit()
        self.wait_for_row_in_chronicle_table('Sess 1: testing')
        textbox = self.browser.find_element_by_id('id_new_sess')
        self.assertAlmostEqual(
            textbox.location['x'] + textbox.size['width'] / 2,
            512,
            delta=10,
        )
