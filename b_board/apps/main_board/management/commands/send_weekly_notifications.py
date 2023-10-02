from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
import logging
from datetime import datetime, timedelta
# ====================================
from django.conf import settings
from apps.main_board.models import Ad, Subscription
from django.contrib.auth.models import User 
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
 
 
logger = logging.getLogger(__name__)
 
def send_weekly_news():
    last_week = datetime.now() - timedelta(weeks=1)
    subscriptions = Subscription.objects.all()
    for subscription in subscriptions:
        if subscription.subscribe_all:
            new_ads = Ad.objects.filter(time_create__gte=last_week)
        elif subscription.categories:
            new_ads = Ad.objects.filter(time_create__gte=last_week, category_ad__in=subscription.categories.all())
        if new_ads.exists():
            user = subscription.user
            subject = f'Новости за последнюю неделю'

            html = render_to_string('mail/week_post_subscribers.html',
                                    context={'new_ads': new_ads, 'user': user})

            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html, "text/html")
            msg.send()

 
# функция которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age) # type: ignore
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        scheduler.add_job(
            send_weekly_news,
            # trigger=CronTrigger(second="*/10"),
            trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),  
            id="send_weekly_news",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_news'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="02", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Старт планировщика ...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Остановка планировщика ...")
            scheduler.shutdown()
            logger.info("Планировщик успешно закрыт!")
            
# ============================================
