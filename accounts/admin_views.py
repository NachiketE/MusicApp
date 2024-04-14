from django.shortcuts import render
from pymongo import MongoClient
from .forms import MusicForm
from pymongo import MongoClient
from .models import Song
import random


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DATABASE_NAME = 'music'
NUM_PARTITIONS = 5

def delete_music(request):
    client = MongoClient('localhost', 27017)
    db = client['music']
    collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']

    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        try:
            for collection_name in collections:
                collection = db[collection_name]
                collection.delete_one({'title': title})
            return render(request, 'admin-templates/delete_music_success.html')
        except Song.DoesNotExist:
            pass
    return render(request, 'admin-templates/delete_music_success.html')  

def search_music(request):
    query = request.GET.get('q')
    if query:
        client = MongoClient('localhost', 27017)
        db = client['music']

        collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']

        search_results = []
        for collection_name in collections:
            collection = db[collection_name]
            results = collection.find({'$or': [{'title': {'$regex': query, '$options': 'i'}}, {'artist': {'$regex': query, '$options': 'i'}}]})
            search_results.extend(results)
    else:
        search_results = []
    
    return render(request, 'admin-templates/search_music.html', {'query': query, 'search_results': search_results})

def admin_control(request):
    return render(request, 'admin-templates/admin_control.html')

def view_all_music(request):
    client = MongoClient('localhost', 27017)
    db = client['music']

    collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']
    
    songs = []
    for collection_name in collections:
        collection = db[collection_name]
        songs.extend(collection.find())  

    return render(request, 'admin-templates/view_all_music.html', {'songs': songs})

def music_page(request):
    return render(request, 'admin-templates/admin_music_page.html')

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