from pymongo import MongoClient

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database
NUM_PARTITIONS = 2  # Number of partitions

# Sample data for Playlist collection


# Sample data for PlaylistMusicMapping collection
playlist_music_mapping_data = [
   {"playlist_id": "1", "music_id": "55"},
    {"playlist_id": "1", "music_id": "56"},
    {"playlist_id": "5", "music_id": "70"},
    {"playlist_id": "5", "music_id": "55"},
    {"playlist_id": "18", "music_id": "61"},
    {"playlist_id": "18", "music_id": "66"},
    {"playlist_id": "18", "music_id": "48"},
    {"playlist_id": "1", "music_id": "72"},
    {"playlist_id": "5", "music_id": "57"},
    {"playlist_id": "5", "music_id": "58"},
    {"playlist_id": "5", "music_id": "40"},
    {"playlist_id": "18", "music_id": "41"},
    {"playlist_id": "1", "music_id": "42"},
    {"playlist_id": "5", "music_id": "55"},
    {"playlist_id": "18", "music_id": "62"},
    {"playlist_id": "18", "music_id": "66"},
    {"playlist_id": "5", "music_id": "57"},
    {"playlist_id": "5", "music_id": "79"},
    {"playlist_id": "1", "music_id": "69"},
    {"playlist_id": "18", "music_id": "43"}
]

# Connect to MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]

# # Clear all previous tables (collections) for Playlist and PlaylistMusicMapping
# for i in range(NUM_PARTITIONS):
#     playlist_collection_name = f"Playlist_{i + 1}"
#     mapping_collection_name = f"PlaylistMusicMapping_{i + 1}"
#     db[playlist_collection_name].drop()
#     db[mapping_collection_name].drop()


# Insert data into the appropriate collection for each partition for PlaylistMusicMapping collection
for mapping in playlist_music_mapping_data:
    playlist_partition_number = int(mapping['playlist_id']) % NUM_PARTITIONS
    mapping_collection_name = f"PlaylistMusicMapping"
    mapping_collection = db[mapping_collection_name]
    mapping_collection.insert_one(mapping)

# Close the MongoDB connection
client.close()
