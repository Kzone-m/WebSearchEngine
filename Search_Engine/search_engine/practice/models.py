from django.db import models
'''
POSITION = (
    ('Pitcher', 'pitcher'),
    ('Catcher', 'catcher'),
    ('Infielder', 'infielder'),
    ('Outfielder', 'outfielder')
)

TEAM = (
    ('A', 'a'),
    ('B', 'b'),
    ('C', 'c'),
)


class Team(models.Model):
    name = models.CharField('球団名', max_length=32, choices=TEAM)

    def __str__(self):
        return self.name + str(self.pk)

    class Meta:
        verbose_name = verbose_name_plural = '球団'
'''


class BaseballPlayer(models.Model):
    name = models.CharField('選手名', max_length=32)
    yearly_pay = models.IntegerField('年棒')
    position = models.CharField('守備位置', max_length=32)
    team = models.CharField('球団名', max_length=32)
    # team = models.ForeignKey(Team)

    def __str__(self):
        return self.name + '@' + self.team

    class Meta:
        verbose_name = verbose_name_plural = '選手'

