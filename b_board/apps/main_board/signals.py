
from .models import Ad, Reply

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
# =====================================================

@receiver(post_save, sender=Reply)
def send_notification_to_ad_author(sender, instance, created, **kwargs):
    if created:
        ad_author = instance.reply.author
        reply_text = instance.text
        # category_ad = instance.reply.category
        ad_url = instance.reply.get_absolute_url()
        html = render_to_string('mail/new_reply_to_ad_author.html',
                                context={'ad_author': ad_author, 
                                         'reply_text': reply_text, 
                                         'ad_url': ad_url, 
                                        #  'category_ad': category_ad, 
                                         })
        subject = f"Новый отклик на ваше объявление."
        recipient_list = [ad_author.email]
        send_email_notification(subject, html, recipient_list)
        
@receiver(post_save, sender=Reply)
def send_notification_to_reply_author(sender, instance, created, **kwargs):
    if not created and instance.is_published:
        reply_author = instance.author
        ad_title = instance.reply.title
        ad_url = instance.reply.get_absolute_url()
        
        html = render_to_string('mail/new_reply_to_reply_author.html',
                                context={'reply_author': reply_author, 
                                         'ad_title': ad_title, 
                                         'ad_url': ad_url, 
                                        #  'category_ad': category_ad, 
                                         })
        subject = f"Новый отклик на ваше объявление."
        recipient_list = [reply_author.email]
        send_email_notification(subject, html, recipient_list)
        
def send_email_notification(subject, html, recipient):
 
    msg = EmailMultiAlternatives(
        subject=subject,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[recipient],
    )
    msg.attach_alternative(html, "text/html")
    msg.send() 
