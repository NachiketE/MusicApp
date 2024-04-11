from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Song
from pymongo import MongoClient
from django import forms
from .forms import MusicForm
from datetime import datetime

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DATABASE_NAME = 'MusicPlaylistManagementSystem'
NUM_PARTITIONS = 5

def consistent_hash_alphabetical(name, num_partitions):
    # Convert the first letter of the name to lowercase
    first_letter = name[0].lower()
    
    
    # Convert the lowercase letter to an ASCII value
    ascii_value = ord(first_letter)
    
    # Calculate partition number based on ASCII value
    partition_number = ascii_value % num_partitions
    return partition_number

def add_music(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            music_data = form.cleaned_data
            # Convert release_date to string format
            music_data['release_date'] = music_data['release_date'].strftime('%Y-%m-%d')
            partition_number = consistent_hash_alphabetical(music_data['title'], NUM_PARTITIONS)
            collection_name = f"Music_{partition_number + 1}"
            client = MongoClient(MONGO_HOST, MONGO_PORT)
            db = client[DATABASE_NAME]
            collection = db[collection_name]
            collection.insert_one(music_data)
            client.close()
            return render(request, 'success.html')
    else:
        form = MusicForm()
    return render(request, 'add_music.html', {'form': form})

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
    
    collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']
    
    songs = []
    for collection_name in collections:
        collection = db[collection_name]
        songs.extend(collection.find())  # Retrieve all documents in the collection
    
    return render(request, 'all_songs.html', {'songs': songs})


def search_results_view(request):
    query = request.GET.get('q')
    if query:
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['music']
        
        # List of collection names
        collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']
        
        # Search each collection for the query
        search_results = []
        for collection_name in collections:
            collection = db[collection_name]
            results = collection.find({'$or': [{'title': {'$regex': query, '$options': 'i'}}, {'artist': {'$regex': query, '$options': 'i'}}]})
            search_results.extend(results)
    else:
        search_results = []
    
    return render(request, 'search_results.html', {'query': query, 'search_results': search_results})