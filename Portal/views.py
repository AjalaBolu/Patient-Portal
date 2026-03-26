from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@email.com',
        password='admin123'
    )