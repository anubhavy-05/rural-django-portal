from django.contrib import admin
from django.urls import path
# Hamare naye view ko import kar rahe hain
from dashboard.views import dashboard_home 

urlpatterns = [
    path('admin/', admin.site.urls),
    # Jab URL khali ho (yani seedha 127.0.0.1:8001), toh dashboard_home chalao
    path('', dashboard_home, name='home'), 
]