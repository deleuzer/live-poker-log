from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from chronicle.views import home_page
from chronicle.models import PokerSession

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={'sess_text': 'A new sess chronicle'})
        self.assertIn('A new sess chronicle', response.content.decode())
        self.assertTemplateUsed(response, 'home.html')
                        
class PokerSessionModelTest(TestCase):
    def test_saving_and_retrieving_pokersessions(self):
        first_pokersession = PokerSession()
        first_pokersession.text = 'The first (ever) poker session'
        first_pokersession.save()
        second_pokersession = PokerSession()
        second_pokersession.text = 'Session the second'
        second_pokersession.save()
        saved_pokersessions = PokerSession.objects.all()
        self.assertEqual(saved_pokersessions.count(), 2)
        first_saved_pokersession = saved_pokersessions[0]
        second_saved_pokersession = saved_pokersessions[1]
        self.assertEqual(first_saved_pokersession.text,
                         'The first (ever) poker session'
        )
        self.assertEqual(second_saved_pokersession.text,
                         'Session the second'
        )
        
