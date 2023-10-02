from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.services.utils import unique_slugify


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        return self.name
    
    # def get_absolute_url(self):
    #     return reverse('category', kwargs={'category_id': self.pk})
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})
    
    
class Ad(models.Model):
    
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'), 
        ('draft', 'Черновик')
    )
    
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.CASCADE, default=1)
    title = models.CharField(verbose_name='Заголовок', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    category_ad = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE, null=True)
    text_ad = models.TextField(verbose_name='Текст объявления')
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус объявления', max_length=20)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания объявления')
    pictures = models.ImageField(
        verbose_name='Картинка', 
        blank=True, 
        upload_to='images/pictures/', 
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))])
    video = models.FileField(
        verbose_name='Видео',
        blank=True,
        upload_to='videos/',
        validators=[FileExtensionValidator(allowed_extensions=('mp4', 'avi', 'mkv', 'mov'))])
    likes = models.ManyToManyField(User, related_name='ad_like')

    def rating(self):
        return self.likes.count()
    
    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        
    
    def get_absolute_url(self):
        if self.status == 'published':
            return reverse('ad_detail', kwargs={'slug': self.slug})
        else:
            return reverse('draft_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        """
        slug из заголовка
        """
        if not self.slug:
            self.slug = unique_slugify(self, self.title)
        super().save(*args, **kwargs)
    
       
    
class Reply(models.Model):
    reply = models.ForeignKey(Ad, on_delete=models.CASCADE)
    text = models.TextField(verbose_name = 'Отклик')
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор отклика')
    created_reply = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False, verbose_name='Опубликовано')
    
    class Meta:
        verbose_name = 'Отклик пользователя'
        verbose_name_plural = 'Отклики пользователей'

    def __str__(self):
        return self.text
    
class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    categories = models.ManyToManyField(Category, blank=True, verbose_name='Категории')
    subscribe_all = models.BooleanField(default=False, verbose_name='Подписаться на все объявления')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'Подписки пользователя {self.user.username}'
