from pymongo import MongoClient
import hashlib

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database
NUM_PARTITIONS = 2  # Number of partitions

# Sample data to insert
playlist_data = [
    {"playlist_id": "1", "user_id": "1", "playlist_name": "Favorites"},
    {"playlist_id": "2", "user_id": "2", "playlist_name": "Workout Mix"},
    {"playlist_id": "3", "user_id": "3", "playlist_name": "Chill Vibes"},
    {"playlist_id": "4", "user_id": "4", "playlist_name": "Road Trip"},
    {"playlist_id": "5", "user_id": "5", "playlist_name": "Study Jams"},
    {"playlist_id": "6", "user_id": "6", "playlist_name": "Party Hits"},
    {"playlist_id": "7", "user_id": "7", "playlist_name": "Relaxing Piano"},
    {"playlist_id": "8", "user_id": "8", "playlist_name": "90s Classics"},
    {"playlist_id": "9", "user_id": "9", "playlist_name": "Indie Vibes"},
    {"playlist_id": "10", "user_id": "10", "playlist_name": "Feel Good"},
    {"playlist_id": "11", "user_id": "1", "playlist_name": "Road Trip"},
    {"playlist_id": "12", "user_id": "1", "playlist_name": "Coding Playlist"},
    {"playlist_id": "13", "user_id": "1", "playlist_name": "Relaxing Sounds"},
    {"playlist_id": "14", "user_id": "6", "playlist_name": "Workout Mix"},
    {"playlist_id": "15", "user_id": "6", "playlist_name": "Focus Music"},
    {"playlist_id": "16", "user_id": "6", "playlist_name": "Throwback Hits"},
    {"playlist_id": "17", "user_id": "7", "playlist_name": "Jazz Classics"},
    {"playlist_id": "18", "user_id": "8", "playlist_name": "Acoustic Sessions"},
    {"playlist_id": "19", "user_id": "7", "playlist_name": "Hip Hop Favorites"},
    {"playlist_id": "20", "user_id": "10", "playlist_name": "Morning Motivation"}
]

# Hashing function for user ID
# def hash_user_id(user_id, num_partitions):
#     hash_object = hashlib.sha256(user_id.encode())
#     hash_digest = int(hash_object.hexdigest(), 16)
#     return hash_digest % num_partitions

def hash_user_id(user_id, num_partitions):
    # Convert user ID to integer
    user_id_int = int(user_id)
    
    # Calculate the hash value
    hash_value = user_id_int % num_partitions
    
    return hash_value

# Connect to MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]

# Clear all previous tables (collections)
for i in range(NUM_PARTITIONS):
    collection_name = f"Playlist_{i + 1}"
    db[collection_name].drop()

# Insert data into the appropriate collection for each partition
for playlist in playlist_data:
    partition_number = hash_user_id(playlist['user_id'], NUM_PARTITIONS)
    collection_name = f"Playlist_{partition_number + 1}"
    collection = db[collection_name]
    collection.insert_one(playlist)

# Close the MongoDB connection
client.close()
