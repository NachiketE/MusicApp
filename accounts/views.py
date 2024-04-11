from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login
from .models import Song
from pymongo import MongoClient


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
    songs = Song.objects.all()
    return render(request, 'home.html', {'songs': songs})

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

