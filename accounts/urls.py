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
    path('delete-song/<int:playlist_id>/', views.delete_song_from_playlist, name='delete_song_from_playlist'),

    path('admin-control/', admin_views.admin_control, name='admin_control'),
    path('admin-music/', admin_views.music_page, name='admin_music_page'),
    path('admin-users/', admin_views.users_page, name='admin_users_page'),
    path('admin-playlists/', admin_views.playlists_page, name='admin_playlists_page'),
    path('admin-view-music/', admin_views.view_all_music, name='admin_view_music'),
    path('admin-search-music/', admin_views.search_music, name='admin_search_music'),
    path('admin-delete-song/', admin_views.delete_music, name='admin_delete_song'),
    path('admin-edit-song/', admin_views.edit_music, name='admin_edit_song'),
    path('admin-delete-user/', admin_views.delete_user, name='admin_delete_user'),
    path('admin-view-playlist-songs/<int:playlist_id>/', admin_views.view_playlist_songs, name='admin_view_playlist_songs')
]
