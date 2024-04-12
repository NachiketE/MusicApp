from django.shortcuts import render
from pymongo import MongoClient
from .forms import MusicForm
from pymongo import MongoClient


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