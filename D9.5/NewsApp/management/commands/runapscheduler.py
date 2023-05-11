import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime
from NewsApp.models import *
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

logger = logging.getLogger(__name__)



def news_week():

    for category in Category.objects.all():
        news_week_category = []
        week_number_last = datetime.now().isocalendar()[1] - 1
        for newsApp in Post.objects.filter(postCategory=category.id,
                                            dateCreation__week=week_number_last).values('pk',
                                                                                    'title',
                                                                                    'dateCreation',
                                                                                    'postCategory__name'):
            date_format = newsApp.get("dateCreation").strftime("%m/%d/%Y")
            new = (f' http://127.0.0.1:8000/news/{newsApp.get("pk")}, {newsApp.get("title")}, '
                   f'Категория: {newsApp.get("postCategory__name")}, Дата создания: {date_format}')
            news_week_category.append(new)

        subscribers = category.subscribers.all()
        for subscriber in subscribers:

            html_content = render_to_string(
                'week.html', {'user': subscriber,
                                     'text': news_week_category,
                                     'category_name': category.name,
                                     'week_number_last': week_number_last})

            msg = EmailMultiAlternatives(

                subject=f'Привет, {subscriber.username}, новые статьи в любимом разделе!',
                from_email=os.getenv('DEFF_EMAIL'),
                to=[subscriber.email]
            )

            msg.attach_alternative(html_content, 'text/html')
            #print(html_content)
            msg.send()


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            news_week,

            trigger=CronTrigger(week="*/1"),
            id="news_week",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Добавлена работа 'news_week'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Задачник запущен")
            print('Задачник запущен')
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Задачник остановлен")
            scheduler.shutdown()
            print('Задачник остановлен')
            logger.info("Задачник остановлен успешно!")
