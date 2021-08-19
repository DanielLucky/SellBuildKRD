from django.contrib.auth.models import User
from django.test import TestCase, Client
import datetime as dt

from Sell.models import Sell


class Test_createProfile(TestCase):
    def setUp(self):
        self.client = Client()
        # self.user = User.objects.create(username='tester', email='test@test.test', password='test')
        self.user = User.objects.create_user('tester', 'test@test.tt', 'test')
        self.sell = Sell.objects.create(
            nameSell='testname',
            author=self.user
        )
        self.user = User.objects.create_user('tester2', 'test@test.tt2', 'test2')


    def test_addTarget(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200) # Проверка на доступность главной страницы
        self.assertContains(response, 'testname') # Проверка названия таргета

    def test_login(self):
        self.client.login(username='tester', password='test')  # Авторизация пользователя
        response = self.client.get('/')
        self.assertEqual(len(response.context['sells']), 1)  # Проверка на добавление записи

    def test_template_index(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response=response, template_name='listing.html', msg_prefix='', count=None) # шаблон главной страницы

    def test_submitTarget(self):
        self.client.login(username='tester', password='test')
        response = self.client.get('/account/submit/') # Доступ на добавление объявления для зарегестрированных пользователей
        self.assertEqual(response.status_code, 200)

        self.client.logout() # logout 'test' юзера
        response = self.client.get('/account/submit/') # Проверка недоступности добавления объявления для AnonymousUser
        self.assertEqual(response.status_code, 302)

    def test_yearFormat(self):
        response = self.client.get('/')
        self.assertEqual(response.context['year'], dt.datetime.now().year)

    def test_deleteSubmit(self):
        self.client.login(username='tester', password='test')
        response = self.client.get('/account/detail/tester')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/account/detail/tester', data={'delete': '1'})
        response = self.client.get('/account/detail/tester')
        self.assertEqual(len(response.context['targets']), 0)


