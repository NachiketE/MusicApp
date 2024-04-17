from pymongo import MongoClient

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database
NUM_PARTITIONS = 2  # Number of partitions

# Sample data for Playlist collection
playlist_data = [
    {"playlist_id": "1", "user_id": "1", "playlist_name": "Favorites"},
    {"playlist_id": "2", "user_id": "1", "playlist_name": "Workout Mix"},
    {"playlist_id": "3", "user_id": "1", "playlist_name": "Chill Vibes"},
    {"playlist_id": "4", "user_id": "4", "playlist_name": "Road Trip"},
    {"playlist_id": "5", "user_id": "4", "playlist_name": "Study Jams"},
    {"playlist_id": "6", "user_id": "6", "playlist_name": "Party Hits"},
    {"playlist_id": "7", "user_id": "8", "playlist_name": "Relaxing Piano"},
    {"playlist_id": "8", "user_id": "8", "playlist_name": "90s Classics"},
    {"playlist_id": "9", "user_id": "9", "playlist_name": "Indie Vibes"},
    {"playlist_id": "10", "user_id": "10", "playlist_name": "Feel Good"},\
]

# Sample data for PlaylistMusicMapping collection
playlist_music_mapping_data = [
    {"playlist_id": "1", "music_id": "1"},
    {"playlist_id": "1", "music_id": "2"},
    {"playlist_id": "2", "music_id": "3"},
    {"playlist_id": "2", "music_id": "4"},
    {"playlist_id": "3", "music_id": "5"},
    {"playlist_id": "3", "music_id": "6"},
    {"playlist_id": "4", "music_id": "7"},
    {"playlist_id": "4", "music_id": "8"},
    {"playlist_id": "5", "music_id": "9"},
    {"playlist_id": "5", "music_id": "10"},
    {"playlist_id": "6", "music_id": "11"},
    {"playlist_id": "6", "music_id": "2"},
    {"playlist_id": "7", "music_id": "3"},
    {"playlist_id": "7", "music_id": "5"},
    {"playlist_id": "8", "music_id": "5"},
    {"playlist_id": "8", "music_id": "6"},
    {"playlist_id": "9", "music_id": "5"},
    {"playlist_id": "9", "music_id": "8"},
    {"playlist_id": "10", "music_id": "9"},
    {"playlist_id": "10", "music_id": "1"}
]

# Connect to MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]

# Clear all previous tables (collections) for Playlist and PlaylistMusicMapping
for i in range(NUM_PARTITIONS):
    playlist_collection_name = f"Playlist_{i + 1}"
    mapping_collection_name = f"PlaylistMusicMapping_{i + 1}"
    db[playlist_collection_name].drop()
    db[mapping_collection_name].drop()

# Insert data into the appropriate collection for each partition for Playlist collection
for playlist in playlist_data:
    partition_number = int(playlist['user_id']) % NUM_PARTITIONS
    collection_name = f"Playlist_{partition_number + 1}"
    collection = db[collection_name]
    collection.insert_one(playlist)

# Insert data into the appropriate collection for each partition for PlaylistMusicMapping collection
for mapping in playlist_music_mapping_data:
    playlist_partition_number = int(mapping['playlist_id']) % NUM_PARTITIONS
    mapping_collection_name = f"PlaylistMusicMapping_{playlist_partition_number + 1}"
    mapping_collection = db[mapping_collection_name]
    mapping_collection.insert_one(mapping)

# Close the MongoDB connection
client.close()
