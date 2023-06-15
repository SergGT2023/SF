# from django.core.mail import send_mail
# from .models import *
# import os
# from dotenv import load_dotenv
# from pathlib import Path
#
#
# load_dotenv()
# env_path = Path('.')/'.env'
# load_dotenv(dotenv_path=env_path)
#
#
# def send_new():
#     user = User.objects.all().values_list("username")
#     title_ = Post.objects.all().values('pk')
#     text = Post.text
#     cat = Category.objects.all().values_list('name', "subscribers")
#     sub = Category.objects.all().values_list('name', flat=True)
#
#     for n, m in cat:
#         if m is not None:
#             print('n:', n)
#             print('m:', m)
#
#             for c in sub:
#                 print('c:', c)
#                 if n == c:
#                     send_mail(subject=f"{title_}",
#                               message= f" Здравствуй,{user}. Новая статья в твоём любимом разделе! {c} \n Заголовок статьи: {title} \n Текст статьи: {text[:50]} \n Перейти на новость: http://127.0.0.1:8000/news/%7Btitle",
#                               from_email=os.getenv('DEFF_EMAIL'),
#                               recipient_list="user_email"
#                               )