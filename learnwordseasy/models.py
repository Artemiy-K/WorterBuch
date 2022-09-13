from django.db import models


class Words(models.Model):
    title1 = models.CharField(max_length=150, verbose_name='Слово')
    title2 = models.CharField(max_length=150, verbose_name='Перевод', null=True)
    example1 = models.TextField(blank=True, verbose_name='Предлложение 1')
    example2 = models.TextField(blank=True, verbose_name='Предлложение 2')
    example3 = models.TextField(blank=True, verbose_name='Предлложение 3')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    for_test = models.IntegerField(default=0)

    def __str__(self):
        return self.title1

    class Meta:
        verbose_name = 'Слово'
        verbose_name_plural = 'Слова'
        ordering = ['-created_at']


class Category(models.Model):
    title1 = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.title1

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title1']



