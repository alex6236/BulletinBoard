from django import template
from django.utils import timezone
from datetime import timedelta
from apps.main_board.models import Ad

register = template.Library()

@register.inclusion_tag('includes/popular_ads.html')
def get_popular_ads():
    start_date = timezone.now() - timedelta(weeks=1)
    popular_ads = Ad.objects.filter(time_create__gte=start_date, status='published').order_by('-likes')[:5]
    return {'popular_ads': popular_ads}



