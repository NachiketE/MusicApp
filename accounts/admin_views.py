from django.shortcuts import render
from pymongo import MongoClient
from .forms import MusicForm
from pymongo import MongoClient
import random


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DATABASE_NAME = 'music'
NUM_PARTITIONS = 5

def admin_control(request):
    return render(request, 'admin-templates/admin_control.html')

def music_page(request):
    client = MongoClient('localhost', 27017)
    db = client['music']

    collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']
    
    songs = []
    for collection_name in collections:
        collection = db[collection_name]
        songs.extend(collection.find())  

    return render(request, 'admin-templates/admin_music_page.html', {'songs': songs})

def users_page(request):
    return render(request, 'admin-templates/admin_users_page.html')

def playlists_page(request):
    return render(request, 'admin-templates/admin_playlists_page.html')

def consistent_hash_alphabetical(name, num_partitions):
    first_letter = name[0].lower()
    ascii_value = ord(first_letter)
    partition_number = ascii_value % num_partitions
    return partition_number

def generate_unique_music_id(collection):
    music_id = random.randint(1, 100000)
    while collection.find_one({'music_id': music_id}):
        music_id = random.randint(1, 100000)
    return music_id

def add_music(request):
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            music_data = form.cleaned_data
            music_data['release_date'] = music_data['release_date'].strftime('%Y-%m-%d')
            partition_number = consistent_hash_alphabetical(music_data['title'], NUM_PARTITIONS)
            collection_name = f"Music_{partition_number + 1}"
            client = MongoClient(MONGO_HOST, MONGO_PORT)
            db = client[DATABASE_NAME]
            collection = db[collection_name]
            music_id = generate_unique_music_id(collection)
            music_data['music_id'] = music_id
            collection.insert_one(music_data)
            client.close()
            return render(request, 'admin-templates/add_music_success.html')
    else:
        form = MusicForm()
    return render(request, 'admin-templates/add_music.html', {'form': form})