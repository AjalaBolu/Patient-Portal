from django.urls import path
from . import views

app_name = 'communications'

urlpatterns = [
    path('', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
]
