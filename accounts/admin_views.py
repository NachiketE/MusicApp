from django.shortcuts import render
from pymongo import MongoClient
from .forms import MusicForm
from pymongo import MongoClient
from .models import Song
from bson import ObjectId
import random

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DATABASE_NAME = 'music'
NUM_PARTITIONS = 5

def edit_music(request):
    if request.method == 'POST':
        original_title = request.POST.get('original_title')
        title = request.POST.get('title')
        artist = request.POST.get('artist')

        print(original_title)
        print(title)
        print(artist)

        client = MongoClient('localhost', 27017)
        db = client['music']
        collections = ['Music_1', 'Music_2', 'Music_3', 'Music_4', 'Music_5']

        for collection_name in collections:
                collection = db[collection_name]
                result = collection.update_one({'title': original_title}, {'$set': {'title': title, 'artist': artist}})

        client.close()

        return render(request, 'admin-templates/edit_music_success.html')

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

def delete_user(request):
    client = MongoClient('localhost', 27017)
    db = client['music']
    collections = ['auth_user']

    if request.method == 'POST':
        username = request.POST.get('username')
        print(username)
        try:
            for collection_name in collections:
                collection = db[collection_name]
                collection.delete_one({'username': username})
            return render(request, 'admin-templates/delete_user_success.html')
        except Song.DoesNotExist:
            pass
    return render(request, 'admin-templates/delete_user_success.html')  

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
    client = MongoClient('localhost', 27017)
    db = client['music']
    collections = ['auth_user']
    
    users = []
    for collection_name in collections:
        collection = db[collection_name]
        users.extend(collection.find())  

    return render(request, 'admin-templates/admin_users_page.html', {'users': users})

def playlists_page(request):
    client = MongoClient('localhost', 27017)
    db = client['music']

    collections = ['Playlist_1', 'Playlist_2']
    
    playlists = []
    for collection_name in collections:
        collection = db[collection_name]
        playlists.extend(collection.find())  

    return render(request, 'admin-templates/admin_playlists_page.html', {'playlists': playlists})

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
            music_id = str(generate_unique_music_id(collection))
            music_data['music_id'] = music_id
            collection.insert_one(music_data)
            client.close()
            return render(request, 'admin-templates/add_music_success.html')
    else:
        form = MusicForm()
    return render(request, 'admin-templates/add_music.html', {'form': form})

def view_playlist_songs(request, playlist_id):
    client = MongoClient('localhost', 27017)
    db = client['music']

    playlist_mapping_collection = db['PlaylistMusicMapping']
    playlist_mapping_data = list(playlist_mapping_collection.find({'playlist_id': str(playlist_id)}))

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

    return render(request, 'admin-templates/admin_single_playlist.html', {'songs': songs})
