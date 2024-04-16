from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Song
from pymongo import MongoClient
from django import forms
from .forms import MusicForm
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from pymongo import MongoClient
from bson import ObjectId
import random
from .models import PlaylistMusicMapping

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DATABASE_NAME = 'music'
NUM_PARTITIONS = 2

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def home_view(request):
    username = request.user.username if request.user.is_authenticated else None

    songs = Song.objects.all()
    return render(request, 'home.html', {'username': username,'songs': songs})

def all_songs_view(request):
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['music']
    user = request.user

    collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']
    
    songs = []
    for collection_name in collections:
        collection = db[collection_name]
        songs.extend(collection.find())  # Retrieve all documents in the collection
    
    user_playlists = get_user_playlists(user)

    return render(request, 'all_songs.html', {'songs': songs, 'user_playlists': user_playlists})


def search_results_view(request):
    query = request.GET.get('q')
    if query:
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['music']
        
        # List of collection names
        collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']
        user = request.user

        user_playlists = get_user_playlists(user)

        # Search each collection for the query
        search_results = []
        for collection_name in collections:
            collection = db[collection_name]
            results = collection.find({'$or': [{'title': {'$regex': query, '$options': 'i'}}, {'artist': {'$regex': query, '$options': 'i'}}]})
            search_results.extend(results)
    else:
        search_results = []
    
    return render(request, 'search_results.html', {'query': query, 'search_results': search_results,  'user_playlists': user_playlists})

@login_required
def playlist_view(request):
    # Retrieve playlists from MongoDB for the current user
    user_playlists = get_user_playlists(request.user)
    
    if user_playlists is None:
        user_playlists = []

    return render(request, 'playlist.html', {'user_playlists': user_playlists})



@login_required
def create_playlist_view(request):
    if request.method == 'POST':
        playlist_name = request.POST.get('playlist_name')
        user = request.user

        # Check if a valid playlist name is provided
        if playlist_name:
            # Save playlist to MongoDB for the current user
            save_playlist(user, playlist_name)

        # Redirect to the playlist page
        return HttpResponseRedirect(reverse('playlist'))

    return render(request, 'create_playlist.html')



def get_user_playlists(user):
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['music']
    
    # Calculate partition number using the hash function
    partition_number = hash_user_id(user.id, NUM_PARTITIONS) + 1
    
    # Get the collection for the user's playlists
    collection_name = f'Playlist_{partition_number}'
    collection = db[collection_name]
    
    # Retrieve the playlists for the user
    user_playlists = list(collection.find({'user_id': str(user.id)}))
    
    # Check if any playlists exist for the user
    if user_playlists:
        return user_playlists
    else:
        return None



def save_playlist(user, playlist_name):
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['music']
    
    # Calculate partition number using the hash function
    partition_number = hash_user_id(user.id, NUM_PARTITIONS) + 1
    
    # Get the collection for the user's playlists
    collection_name = f'Playlist_{partition_number}'
    collection = db[collection_name]
    
    # Generate a unique playlist_id
    playlist_id = generate_unique_playlist_id(collection)
    
    # Insert the new playlist document
    playlist_data = {
        'playlist_id': playlist_id,
        'user_id': str(user.id),
        'playlist_name': playlist_name
    }
    collection.insert_one(playlist_data)

def generate_unique_playlist_id(collection):
    playlist_id = random.randint(1, 100000)
    # Check if the playlist_id already exists in the collection
    while collection.find_one({'playlist_id': playlist_id}):
        playlist_id = random.randint(1, 100000)
    return playlist_id



def hash_user_id(user_id, num_partitions):
    user_id_int = int(user_id)
    
    hash_value = user_id_int % num_partitions
    
    return hash_value


@login_required
def delete_playlist_view(request):
    if request.method == 'POST':
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['music']

        # Get playlist name from form data
        playlist_name = request.POST.get('playlist_name')

        # Delete the playlist from the MongoDB collection
        collections = ['Playlist_1', 'Playlist_2']
        for collection_name in collections:
            collection = db[collection_name]
            collection.delete_one({'playlist_name': playlist_name})

        # Redirect back to the playlist page
        return HttpResponseRedirect(reverse('playlist'))
    
@login_required
def add_to_playlist_view(request):
    if request.method == 'POST':
        client = MongoClient('localhost', 27017)
        db = client['music']
        music_id = request.POST.get('music_id')
        playlist_id = request.POST.get('playlist_id')
        print(music_id)
        print(playlist_id)
        # Create an entry in PlaylistMusicMapping collection
        mapping_entry = {
        'music_id': music_id,
        'playlist_id': playlist_id
        }
        print(mapping_entry)
        

        
        collection_name = 'PlaylistMusicMapping'
        collection = db[collection_name]

        collection.insert_one(mapping_entry)

        
        # Redirect to a new page with a success message
        return render(request, 'song_added.html', {'music_id': music_id, 'playlist_id': playlist_id})
    else:
        # Handle GET requests if needed
        pass


@login_required
def view_playlist_songs(request, playlist_id):
    # Connect to MongoDB
    client = MongoClient('localhost', 27017)
    db = client['music']  # Replace 'your_database_name' with your actual MongoDB database name

    # Retrieve the songs associated with the playlist from the PlaylistMusicMapping collection
    playlist_mapping_collection = db['PlaylistMusicMapping']
    playlist_mapping_data = list(playlist_mapping_collection.find({'playlist_id': str(playlist_id)}))

    # Retrieve song details from all the Music collections based on song_id
    songs = []
    for mapping_data in playlist_mapping_data:
        song_id = mapping_data['music_id']
        for collection_name in db.list_collection_names():
            if collection_name.startswith("Music_"):
                music_collection = db[collection_name]
                song_data = music_collection.find_one({'music_id': str(song_id)})
                if song_data:
                    song = Song(
                        music_id=song_data['music_id'],
                        title=song_data['title'],
                        artist=song_data['artist'],
                        genre=song_data['genre'],
                        duration=song_data['duration'],
                        release_date=song_data['release_date']
                    )
                    songs.append(song)

    # Render the single_playlist.html template with the playlist and songs data
    return render(request, 'single_playlist.html', {'songs': songs, 'playlist_id': playlist_id})


@login_required
def delete_song_from_playlist(request, playlist_id):
    if request.method == 'POST':
        song_id = request.POST.get('song_id')
        # Connect to MongoDB and remove the song from the PlaylistMusicMapping collection
        client = MongoClient('localhost', 27017)
        db = client['music']  # Replace 'your_database_name' with your actual MongoDB database name
        playlist_mapping_collection = db['PlaylistMusicMapping']
        playlist_mapping_collection.delete_one({'playlist_id': str(playlist_id), 'music_id': str(song_id)})
        
    return HttpResponseRedirect(reverse('view_playlist_songs', args=[playlist_id]))