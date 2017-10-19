from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from chronicle.views import home_page

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'sess_text': 'A new sess chronicle'})
        self.assertIn('A new sess chronicle', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
                        

