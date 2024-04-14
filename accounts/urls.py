from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('home/', views.home_view, name='home'),
    path('all-songs/', views.all_songs_view, name='all_songs'),
    path('add-music/', admin_views.add_music, name='add_music'),
    path('search/', views.search_results_view, name='search_results'),
    path('playlist/', views.playlist_view, name='playlist'),
    path('create-playlist/', views.create_playlist_view, name='create_playlist'),
    path('delete-playlist/', views.delete_playlist_view, name='delete_playlist'),
    path('add-to-playlist/', views.add_to_playlist_view, name='add_song_to_playlist'),
    path('view-playlist-songs/<int:playlist_id>/', views.view_playlist_songs, name='view_playlist_songs'),

]
