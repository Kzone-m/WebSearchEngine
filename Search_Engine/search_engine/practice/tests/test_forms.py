from django.test import TestCase
from practice.models import BaseballPlayer
from practice.forms import BaseballPlayerSearchForm


class TestBaseballPlayerSearchForm(TestCase):
    def test_filter_players_name(self):
        BaseballPlayer.objects.create(name='TEST1', yearly_pay=1000, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST2', yearly_pay=1000, position='Center', team='A')

        form = BaseballPlayerSearchForm({'name': 'TEST'})
        actual = form.filter_players(BaseballPlayer.objects.all())
        self.assertEqual(len(actual), 2)
        self.assertEqual(actual[0].name, 'TEST1')
        self.assertEqual(actual[1].name, 'TEST2')

    def test_filter_players_yearly_pay_min(self):
        BaseballPlayer.objects.create(name='TEST1', yearly_pay=999, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST2', yearly_pay=1000, position='Center', team='A')

        form = BaseballPlayerSearchForm({'yearly_pay_min': 1000})
        actual = form.filter_players(BaseballPlayer.objects.all())
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, 'TEST2')

    def test_filter_players_yearly_pay_max(self):
        BaseballPlayer.objects.create(name='TEST1', yearly_pay=999, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST2', yearly_pay=1000, position='Center', team='A')

        form = BaseballPlayerSearchForm({'yearly_pay_max': 999})
        actual = form.filter_players(BaseballPlayer.objects.all())
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, 'TEST1')

    def test_filter_players_position(self):
        BaseballPlayer.objects.create(name='TEST1', yearly_pay=999, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST2', yearly_pay=1000, position='Pitcher', team='A')

        form = BaseballPlayerSearchForm({'position': 'Center'})
        actual = form.filter_players(BaseballPlayer.objects.all())
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, 'TEST1')

    def test_filter_players_team(self):
        BaseballPlayer.objects.create(name='TEST1', yearly_pay=999, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST2', yearly_pay=1000, position='Pitcher', team='B')

        form = BaseballPlayerSearchForm({'team': 'A'})
        actual = form.filter_players(BaseballPlayer.objects.all())
        self.assertEqual(len(actual), 1)
        self.assertEqual(actual[0].name, 'TEST1')

    def test_filter_players_invalid(self):
        BaseballPlayer.objects.create(name='TEST1', yearly_pay=999, position='Center', team='A')
        BaseballPlayer.objects.create(name='TEST2', yearly_pay=1000, position='Pitcher', team='B')

        form = BaseballPlayerSearchForm({'yearly_pay_max': 'Not Integer'})
        actual = form.filter_players(BaseballPlayer.objects.all())
        self.assertEqual(actual[0].name, 'TEST1')
        self.assertEqual(actual[1].name, 'TEST2')


