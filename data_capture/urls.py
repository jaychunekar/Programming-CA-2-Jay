from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('upload/', views.upload_file, name='upload_file'),
    path('scrape/', views.scrape_url, name='scrape_url'),
    path('api/upload/', views.api_upload_file, name='api_upload_file'),
    path('api/scrape/', views.api_scrape_url, name='api_scrape_url'),
]


