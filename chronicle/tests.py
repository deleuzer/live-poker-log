from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from chronicle.views import home_page
from chronicle.models import PokerSession, Chronicles

class HomePageTest(TestCase):
    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
class ChroniclesAndPokerSessionModelTest(TestCase):
    def test_saving_and_retrieving_pokersessions(self):
        chronicles = Chronicles()
        chronicles.save()
        first_pokersession = PokerSession()
        first_pokersession.text = 'The first (ever) poker session'
        first_pokersession.chronicles = chronicles
        first_pokersession.save()
        second_pokersession = PokerSession()
        second_pokersession.text = 'Session the second'
        second_pokersession.chronicles = chronicles
        second_pokersession.save()
        saved_chronicles = Chronicles.objects.first()
        self.assertEqual(saved_chronicles, chronicles)
        saved_pokersessions = PokerSession.objects.all()
        self.assertEqual(saved_pokersessions.count(), 2)
        first_saved_pokersession = saved_pokersessions[0]
        second_saved_pokersession = saved_pokersessions[1]
        self.assertEqual(first_saved_pokersession.text,
                         'The first (ever) poker session'
        )
        self.assertEqual(first_saved_pokersession.chronicles, chronicles)
        self.assertEqual(second_saved_pokersession.text,
                         'Session the second'
        )
        self.assertEqual(second_saved_pokersession.chronicles, chronicles)
class ChroniclesViewTest(TestCase):
    def test_uses_chronicle_template(self):
        chronicles = Chronicles.objects.create()
        response = self.client.get(f'/chronicles/{chronicles.id}/')
        self.assertTemplateUsed(response, 'chronicles.html')
    def test_displays_only_sessions_for_that_chronicle(self):
        correct_chronicles = Chronicles.objects.create()
        PokerSession.objects.create(text='session 1', chronicles=correct_chronicles)
        PokerSession.objects.create(text='session 2', chronicles=correct_chronicles)
        other_chronicles = Chronicles.objects.create()
        PokerSession.objects.create(text='other session 1',
                                    chronicles=other_chronicles)
        PokerSession.objects.create(text='other session 2',
                                    chronicles=other_chronicles)
        
        response = self.client.get(f'/chronicles/{correct_chronicles.id}/')
        self.assertContains(response, 'session 1')
        self.assertContains(response, 'session 2')
        self.assertNotContains(response, 'other session 1')
        self.assertNotContains(response, 'other session 2')

class NewChronicleTest(TestCase):
    def test_can_save_a_POST_request(self):
        response = self.client.post('/chronicles/new',
                                    data={'sess_text': 'A new sess chronicle'})
        self.assertEqual(PokerSession.objects.count(), 1)
        new_sess = PokerSession.objects.first()
        self.assertEqual(new_sess.text, 'A new sess chronicle')
    def test_redirects_after_POST(self):
        response = self.client.post('/chronicles/new',
                                    data={'sess_text': 'A new sess chronicle'})
        new_chronicle = Chronicles.objects.first()
        self.assertRedirects(response,
                             f'/chronicles/{new_chronicle.id}/')
    def test_can_save_a_POST_request_to_an_existing_chronicle(self):
        other_chronicles = Chronicles.objects.create()
        correct_chronicles = Chronicles.objects.create()
        self.client.post(
            f'/chronicles/{correct_chronicles.id}/add_sess',
            data={'sess_text': 'A new sess for testing'}
        )
        self.assertEqual(PokerSession.objects.count(), 1)
        new_sess = PokerSession.objects.first()
        self.assertEqual(new_sess.text, 'A new sess for testing')
        self.assertEqual(new_sess.chronicles, correct_chronicles)
    def test_redirects_to_chronicle_view(self):
        other_chronicles = Chronicles.objects.create()
        correct_chronicles = Chronicles.objects.create()
        response = self.client.post(
            f'/chronicles/{correct_chronicles.id}/add_sess',
            data={'sess_text': 'A new sess for testing'}
        )
        self.assertRedirects(response,
                             f'/chronicles/{correct_chronicles.id}/')
    def test_passes_correct_chronicles_to_template(self):
        other_chronicles = Chronicles.objects.create()
        correct_chronicles = Chronicles.objects.create()
        response = self.client.get(f'/chronicles/{correct_chronicles.id}/')
        self.assertEqual(response.context['chronicles'], correct_chronicles)
