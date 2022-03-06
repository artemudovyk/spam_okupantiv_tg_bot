from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [  
    # TODO: make webhook more secure
    path('', views.index, name="index"),
    path('super_secter_webhook/', csrf_exempt(views.TelegramBotWebhookView.as_view())),
    path('post_contact/', views.post_contact, name='post_contact'),
    path('get_phone_numbers/', views.get_all_phone_numbers, name='get_all_phone_numbers'),
]