from django.urls import path
from . import views

app_name = 'practice'

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_song, name='upload_song'),
    path('upload_sheet/<int:song_id>/', views.upload_sheet, name='upload_sheet'),
    path('song/<int:song_id>/', views.song_detail, name='song_detail'),
    path('song/<int:song_id>/timing/', views.set_page_timing, name='set_page_timing'),
    path('api/song/<int:song_id>/timings/', views.get_page_timings, name='get_page_timings'),
]