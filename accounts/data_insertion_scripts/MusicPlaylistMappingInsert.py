from pymongo import MongoClient

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database
NUM_PARTITIONS = 2  # Number of partitions

# Sample data to insert
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
    {"playlist_id": "10", "music_id": "5"}
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