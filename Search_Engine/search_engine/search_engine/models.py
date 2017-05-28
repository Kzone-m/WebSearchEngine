from django.db import models


class Index(models.Model):
    index = models.CharField('索引', max_length=100)

    def __str__(self):
        return self.index

    class Meta:
        verbose_name = verbose_name_plural = '索引'


class Url(models.Model):
    url = models.CharField('URL', max_length=100)
    index = models.ForeignKey(Index)

    def __str__(self):
        return self.url + ' for ' + self.index.index

    class Meta:
        verbose_name = verbose_name_plural = 'URL'