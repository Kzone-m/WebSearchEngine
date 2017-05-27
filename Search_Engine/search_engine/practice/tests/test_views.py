from django.test import TestCase
from django.core.urlresolvers import reverse
from practice.models import BaseballPlayer
from practice.forms import BaseballPlayerAddForm


class TestPracticeList(TestCase):
    def test_get(self):
        BaseballPlayer.objects.create(name='TEST', yearly_pay=1000, position='Center', team='A')
        res = self.client.get(reverse('practice_list'))
        self.assertTemplateUsed(res, 'practice/practice_list.html')
        self.assertContains(res, 'TEST')
        self.assertContains(res, 1000)
        self.assertContains(res, 'Center')
        self.assertContains(res, 'A')

    def test_get_paginate(self):
        BaseballPlayer.objects.create(name='TEST1', yearly_pay=1000, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST2', yearly_pay=1000, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST3', yearly_pay=1000, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST4', yearly_pay=1000, position='Center', team='A')

        res = self.client.get(reverse('practice_list'), data={'page': 1})
        self.assertContains(res, 'TEST1')
        self.assertContains(res, 'TEST2')

        res = self.client.get(reverse('practice_list'), data={'page': 2})
        self.assertContains(res, 'TEST3')
        self.assertContains(res, 'TEST4')

    def test_get_invalid_page(self):
        BaseballPlayer.objects.create(name='TEST', yearly_pay=1000, position='Center', team='A')
        res = self.client.get(reverse('practice_list'), data={'page': 'not integer'})
        self.assertTemplateUsed(res, 'practice/practice_list.html')
        self.assertContains(res, 'TEST')
        self.assertContains(res, 1000)
        self.assertContains(res, 'Center')
        self.assertContains(res, 'A')

    def test_get_too_big_page(self):
        BaseballPlayer.objects.create(name='TEST', yearly_pay=1000, position='Center', team='A')
        res = self.client.get(reverse('practice_list'), data={'page': 99999999})
        self.assertTemplateUsed(res, 'practice/practice_list.html')
        self.assertContains(res, 'TEST')
        self.assertContains(res, 1000)
        self.assertContains(res, 'Center')
        self.assertContains(res, 'A')


class TestPracticeAdd(TestCase):
    def test_get(self):
        res = self.client.get(reverse('practice_add'))
        self.assertTemplateUsed(res, 'practice/practice_add.html')

    def test_post(self):
        # player = BaseballPlayer.objects.create(id=1, name='HIGE', yearly_pay=1000, position='Center', team='A')
        res = self.client.post(reverse('practice_add'), data={'name': 'SODA', 'yearly_pay': 100, 'position': 'Pitcher', 'team': 'B'})
        self.assertRedirects(res, reverse('practice_list'))

    def test_invalid_post(self):
        res = self.client.post(reverse('practice_add'), data={'name': 'SODA', 'yearly_pay': 100, 'position': 'Pitcher', 'team': ''})
        self.assertTemplateUsed(res, 'practice/practice_add.html')


class TestPracticeEdit(TestCase):
    def test_get(self):
        BaseballPlayer.objects.create(id=1, name='HIGE', yearly_pay=1000, position='Center', team='A')
        res = self.client.get(reverse('practice_edit', args=(1, )))
        self.assertTemplateUsed(res, 'practice/practice_edit.html')
        self.assertContains(res, 'HIGE')
        self.assertContains(res, 1000)
        self.assertContains(res, 'Center')
        self.assertContains(res, 'A')

    def test_post(self):
        player = BaseballPlayer.objects.create(id=1, name='HIGE', yearly_pay=1000, position='Center', team='A')
        res = self.client.post(reverse('practice_edit', args=(1, )), data={'name': 'SODA', 'yearly_pay': 100, 'position': 'Pitcher', 'team': 'B'})
        self.assertRedirects(res, reverse('practice_list'))
        player.refresh_from_db()
        self.assertEqual(player.name, 'SODA')
        self.assertEqual(player.yearly_pay, 100)
        self.assertEqual(player.position, 'Pitcher')

    def test_invalid_post(self):
        player = BaseballPlayer.objects.create(id=1, name='HIGE', yearly_pay=1000, position='Center', team='A')
        res = self.client.post(reverse('practice_edit', args=(1, )), data={'name': 'SODA', 'yearly_pay': 100, 'position': 'Pitcher', 'team': ''})
        self.assertTemplateUsed(res, 'practice/practice_edit.html')

    def test_404(self):
        res = self.client.get(reverse('practice_edit', args=(1, )))
        self.assertEqual(res.status_code, 404)


class TestPracticeDelete(TestCase):
    def test_get(self):
        BaseballPlayer.objects.create(id=1, name='HIGE', yearly_pay=1000, position='Outfielder', team='B')
        res = self.client.get(reverse('practice_delete', args=(1,)))
        self.assertRedirects(res, reverse('practice_list'))
        self.assertFalse(BaseballPlayer.objects.exists())

    def test_404(self):
        res = self.client.get(reverse('practice_delete', args=(1,)))
        self.assertEqual(res.status_code, 404)