from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.services.utils import unique_slugify

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True, unique=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d/', 
        default='images/avatars/default.png',
        blank=True,  
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    class Meta:
        db_table = 'app_profiles'
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

