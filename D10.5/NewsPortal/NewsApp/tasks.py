from celery import shared_task
from django.core.mail import send_mail
from .models import *
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

@shared_task
def send_new_news():
    print('hello')
    user = User.objects.all().values_list("username")
    title_ = Post.objects.all().values('pk')
    text = Post.text
    cat = Category.objects.all().values_list('name', "subscribers")
    sub = Category.objects.all().values_list('name', flat=True)

    for n, m in cat:
        if m is not None:
            print('n:', n)
            print('m:', m)

            for c in sub:
                print('c:', c)
                if n == c:
                    send_mail(subject=f"{title_}",
                        message=f"Здравствуй,{user}.",
                        from_email=os.getenv('DEFF_EMAIL'),
                        recipient_list=["simanin69@gmail.com"],
                        )