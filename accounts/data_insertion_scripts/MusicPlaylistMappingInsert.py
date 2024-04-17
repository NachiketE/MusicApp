from pymongo import MongoClient

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database
NUM_PARTITIONS = 2  # Number of partitions

# Sample data to insert
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

# Hashing function for playlist ID
def simple_hash_playlist_id(playlist_id, num_partitions):
    playlist_id_int = int(playlist_id)
    hash_value = playlist_id_int % num_partitions
    return hash_value

# Connect to MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]

# Check if referenced records exist in Music and Playlist collections
def check_foreign_key_constraints(playlist_id, music_id):
    for i in range(NUM_PARTITIONS):
        playlist_exists = db[f"Playlist_{i + 1}"].find_one({"playlist_id": playlist_id})
        music_exists = db[f"Music_{i + 1}"].find_one({"music_id": music_id})
        if playlist_exists is not None and music_exists is not None:
            return True
    return False


# Clear all previous tables (collections)
for i in range(NUM_PARTITIONS):
    collection_name = f"PlaylistMusicMapping_{i + 1}"
    db[collection_name].drop()

# Insert data into the appropriate collection for each partition
for mapping in playlist_music_mapping_data:
    if check_foreign_key_constraints(mapping['playlist_id'], mapping['music_id']):
        partition_number = simple_hash_playlist_id(mapping['playlist_id'], NUM_PARTITIONS)
        collection_name = f"PlaylistMusicMapping_{partition_number + 1}"
        collection = db[collection_name]
        collection.insert_one(mapping)
    else:
        print(f"Skipping insertion for playlist_id={mapping['playlist_id']} and music_id={mapping['music_id']}: Foreign key constraint violated.")

# Close the MongoDB connection
client.close()