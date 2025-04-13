from django.db import models

from users.models import User


class Ad(models.Model):
    """ Модель объявления. """

    # выбор состояния товара
    CONDITION_CHOICES = (
        ('новый', 'Новый'),
        ('б/у', 'Б/у'),
    )
    # выбор категории
    CATEGORY_CHOICES = (
        ('одежда', 'Одежда'),
        ('обувь', 'Обувь'),
        ('аксессуары', 'Аксессуары'),
        ('хобби', 'Хобби'),
        ('электроника', 'Электроника'),
        ('для дома и дачи', 'Для дома и дачи'),
        ('запчасти', 'Запчасти'),
        ('товары для детей', 'Товары для детей'),
        ('красота и здоровье', 'Красота и здоровье'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Создатель объявления')
    title = models.CharField(max_length=250, verbose_name='Заголовок объявления')
    description = models.TextField(verbose_name='Описание товара')
    image_url = models.ImageField(upload_to='ad_images', verbose_name='Изображение', blank=True, null=True)
    category = models.CharField(max_length=30, verbose_name='Категория товара', choices=CATEGORY_CHOICES)
    condition = models.CharField(max_length=10, verbose_name='Состояние товара', choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания объявления")

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

    def __str__(self):
        return self.title


class ExchangeProposal(models.Model):
    """ Модель для предложений обмена. """

    ad_sender = models.ForeignKey(Ad, on_delete=models.DO_NOTHING, verbose_name='Что менять', related_name='sender_exchange_proposals')
    ad_receiver = models.ForeignKey(Ad, on_delete=models.DO_NOTHING, verbose_name='На что менять', related_name='receiver_exchange_proposals')
    comment = models.TextField(verbose_name='Комментарий')
    status = models.CharField(max_length=15, verbose_name='Статус', default='Ожидает')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания объявления")

    class Meta:
        verbose_name = 'Предложение обмена'
        verbose_name_plural = 'Предложения обмена'
