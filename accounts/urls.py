from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('all-songs/', views.all_songs_view, name='all_songs'),
    path('add-music/', views.add_music, name='add_music'),
    path('search/', views.search_results_view, name='search_results'),

]
