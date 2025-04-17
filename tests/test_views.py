from django.test import TestCase
from django.urls import reverse
from users.models import User
from ads.models import Ad, ExchangeProposal


class AdCreateViewTest(TestCase):
    """ Тест создания объявления. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.form_data = {
            'title': 'Тест',
            'description': 'Описание',
            'image_url': '',
            'category': 'одежда',
            'condition': 'новый',
        }

    def test_ad_create_view_creates_ad(self):
        """ Тест создания объявления и привязки к текущему пользователю. """

        response = self.client.post(reverse('ads:ad-create'), data=self.form_data)

        self.assertEqual(response.status_code, 302)

        new_ad = Ad.objects.latest('id')

        self.assertEqual(new_ad.title, self.form_data['title'])
        self.assertEqual(new_ad.user, self.user)

    def test_ad_create_view_redirects_on_success(self):
        """ Тест проверяет, что после создания объявления, происходит перенаправление на страницу с информацией. """

        response = self.client.post(reverse('ads:ad-create'), data=self.form_data)

        self.assertEqual(response.status_code, 302)

        new_ad = Ad.objects.latest('id')

        self.assertRedirects(response, reverse('ads:ad-detail', kwargs={'pk': new_ad.pk}))


class AdUpdateViewTest(TestCase):
    """ Тест редактирования объявления. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.ad = Ad.objects.create(title='Тест', user=self.user)

        self.updated_data = {
            'title': 'Тест обновлен',
            'description': 'Описание обновлено',
            'category': 'одежда',
            'condition': 'новый',
        }

    def test_ad_update_view_updates_ad(self):
        """ Тест редактирования объявления. """

        response = self.client.post(reverse('ads:ad-update', kwargs={'pk': self.ad.pk}), data=self.updated_data)
        updated_ad = Ad.objects.get(pk=self.ad.pk)

        self.assertEqual(updated_ad.title, self.updated_data['title'])
        self.assertEqual(updated_ad.description, self.updated_data['description'])

    def test_ad_update_view_redirects_on_success(self):
        """ Тест проверяет, что после редактирования объявления, происходит перенаправление на страницу с моими объявлениями. """

        response = self.client.post(reverse('ads:ad-update', kwargs={'pk': self.ad.pk}), data=self.updated_data)

        self.assertRedirects(response, reverse('ads:ads-mylist'))


class AdDeleteViewTest(TestCase):
    """ Тест удаления объявления. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.ad = Ad.objects.create(title='Тест', user=self.user)

    def test_ad_delete_view_deletes_ad(self):
        """ Тест удаления объявления. """

        response = self.client.post(reverse('ads:ad-delete', kwargs={'pk': self.ad.pk}))

        self.assertFalse(Ad.objects.filter(pk=self.ad.pk).exists())

    def test_ad_delete_view_redirects_on_success(self):
        """ Тест проверяет, что после удаления объявления, происходит перенаправление на страницу с моими объявлениями. """

        response = self.client.post(reverse('ads:ad-delete', kwargs={'pk': self.ad.pk}))

        self.assertRedirects(response, reverse('ads:ads-mylist'))


class ExchangeProposalCreateTest(TestCase):
    """ Тест создания обмена. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.ad = Ad.objects.create(title='Тест', user=self.user)

        self.form_data = {
            'ad_receiver': self.ad.pk,
            'comment': 'Поменяемся?',
        }

    def test_exchange_proposal_create_submits_and_saves(self):
        """ Тест создания обмена. """

        response = self.client.post(reverse('ads:exchange-create', kwargs={'pk': self.ad.pk}), data=self.form_data)
        new_proposal = ExchangeProposal.objects.latest('id')

        self.assertEqual(new_proposal.ad_sender, self.ad)
        self.assertEqual(new_proposal.owner, self.user)
        self.assertEqual(new_proposal.comment, self.form_data['comment'])

    def test_exchange_proposal_create_redirects_on_success(self):
        """ Тест проверяет, что после создания обмена происходит перенаправление на страницу с объявлениями. """

        response = self.client.post(reverse('ads:exchange-create', kwargs={'pk': self.ad.pk}), data=self.form_data)

        self.assertRedirects(response, reverse('ads:ads-list'))


class MyExchangeProposalListViewTest(TestCase):
    """ Тест списка моих предложений обмена. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.ad1 = Ad.objects.create(title='Тест 1', user=self.user)
        self.ad2 = Ad.objects.create(title='Тест 2', user=self.user)

        self.exchange_proposed = ExchangeProposal.objects.create(owner=self.user, ad_sender=self.ad1, ad_receiver=self.ad2, status='Ожидает')
        self.other_exchange = ExchangeProposal.objects.create(owner=self.user, ad_sender=self.ad2, ad_receiver=self.ad1, status='Подтвержден')

    def test_my_exchange_proposal_list_view_lists_correct_exchanges(self):
        """ Тест списка моих предложений обмена. """

        response = self.client.get(reverse('ads:my-exchanges-list'))
        exchanges = list(response.context['exchanges'])

        self.assertIn(self.exchange_proposed, exchanges)
        self.assertNotIn(self.other_exchange, exchanges)

    def test_my_exchange_proposal_list_view_requires_authentication(self):
        """ Тест проверяет, что только авторизованные пользователи могут посмотреть предложения обмена. """

        self.client.logout()

        response = self.client.get(reverse('ads:my-exchanges-list'))

        self.assertEqual(response.status_code, 302)


class OffersExchangeProposalListViewTest(TestCase):
    """ Тест предложений пользователю об обмене. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.ad1 = Ad.objects.create(title='Тест 1', user=self.user)
        self.ad2 = Ad.objects.create(title='Тест 2', user=self.user)

        other_user = User.objects.create_user(email='other@test.ru', password='otherpass')
        another_ad = Ad.objects.create(title='Тест 3', user=other_user)

        self.exchange_proposed = ExchangeProposal.objects.create(owner=self.user, ad_sender=self.ad1, ad_receiver=another_ad, status='Ожидает')

        self.exchange_from_other = ExchangeProposal.objects.create(owner=other_user, ad_sender=another_ad, ad_receiver=self.ad1, status='Ожидает')

    def test_offers_exchange_proposal_list_view_lists_correct_exchanges(self):
        """ Тест проверяет, что показываются только предложения обмена от других пользователей. """

        response = self.client.get(reverse('ads:offers-exchanges'))
        exchanges = list(response.context['exchanges'])

        self.assertIn(self.exchange_from_other, exchanges)
        self.assertNotIn(self.exchange_proposed, exchanges)

    def test_offers_exchange_proposal_list_view_requires_authentication(self):
        """ Тест проверяет, что только авторизованные пользователи могут посмотреть предложения обмена. """

        self.client.logout()

        response = self.client.get(reverse('ads:offers-exchanges'))

        self.assertEqual(response.status_code, 302)


class ExchangeProposalDeleteViewTest(TestCase):
    """ Тест удаления предложения об обмене. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.ad1 = Ad.objects.create(title='Тест 1', user=self.user)
        self.ad2 = Ad.objects.create(title='Тест 2', user=self.user)

        self.proposal = ExchangeProposal.objects.create(owner=self.user, ad_sender=self.ad1, ad_receiver=self.ad2, status='Ожидает')

    def test_exchange_proposal_delete_view_deletes_proposal(self):
        """ Тест удаления предложения об обмене. """

        response = self.client.post(reverse('ads:delete-exchange-proposal', kwargs={'pk': self.proposal.pk}))

        self.assertFalse(ExchangeProposal.objects.filter(pk=self.proposal.pk).exists())

    def test_exchange_proposal_delete_view_redirects_on_success(self):
        """ Тест проверяет, что после удаления предложения происходит перенаправляется на страницу с моими предложениями обмена. """

        response = self.client.post(reverse('ads:delete-exchange-proposal', kwargs={'pk': self.proposal.pk}))

        self.assertRedirects(response, reverse('ads:my-exchanges-list'))

    def test_exchange_proposal_delete_view_requires_authentication(self):
        """ Тест проверяет, что только авторизованные пользователи могут удалить предложения обмена. """

        self.client.logout()

        response = self.client.post(reverse('ads:delete-exchange-proposal', kwargs={'pk': self.proposal.pk}))

        self.assertEqual(response.status_code, 302)


class AdSearchListViewTest(TestCase):
    """ Тест поиска по объявлениям. """

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@mail.ru', password='testpass')
        self.client.login(email='testuser@mail.ru', password='testpass')

        self.ad1 = Ad.objects.create(title='Тест 1', description='Описание 1', category='одежда', condition='новый', user=self.user)
        self.ad2 = Ad.objects.create(title='Тест 2', description='Описание 2', category='обувь', condition='б/у', user=self.user)
        self.another_user = User.objects.create_user(email='another@user.mail.ru', password='another_pass')
        self.another_ad = Ad.objects.create(title='Тест 3', description='Описание 3', category='одежда', condition='новый', user=self.another_user)

    def test_ad_search_list_view_performs_full_text_search(self):
        """ Тест полнотекстового поиска. """

        response = self.client.get(reverse('ads:search-ads') + '?query=Тест 3')
        ads = list(response.context['ads'])

        self.assertIn(self.another_ad, ads)
        self.assertNotIn(self.ad1, ads)
        self.assertNotIn(self.ad2, ads)

    def test_ad_search_list_view_filters_by_category(self):
        """ Тест фильтрации объявления по категории. """

        response = self.client.get(reverse('ads:search-ads') + '?category=одежда')
        ads = list(response.context['ads'])

        self.assertIn(self.another_ad, ads)
        self.assertNotIn(self.ad2, ads)

    def test_ad_search_list_view_filters_by_condition(self):
        """ Тест фильтрации объявления по состоянию товара. """

        response = self.client.get(reverse('ads:search-ads') + '?condition=новый')
        ads = list(response.context['ads'])

        self.assertIn(self.another_ad, ads)
        self.assertNotIn(self.ad2, ads)

    def test_ad_search_list_view_pagination_works(self):
        """ Тест пагинации(20 объявлений на странице). """

        for i in range(30):
            Ad.objects.create(title=f'Тест {i}', description=f'Описание {i}', user=self.user)

        response = self.client.get(reverse('ads:search-ads'))

        self.assertLessEqual(len(response.context['ads']), 20)
