from pymongo import MongoClient
import hashlib

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database
NUM_PARTITIONS = 5  # Number of partitions

# Sample data to insert
music_data = [
    {"music_id": "1", "title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock", "duration": "6:07", "release_date": "1975-10-31"},
    {"music_id": "2", "title": "Hotel California", "artist": "Eagles", "genre": "Rock", "duration": "6:30", "release_date": "1976-12-08"},
    {"music_id": "3", "title": "Stairway to Heaven", "artist": "Led Zeppelin", "genre": "Rock", "duration": "8:02", "release_date": "1971-11-05"},
    {"music_id": "4", "title": "Thriller", "artist": "Michael Jackson", "genre": "Pop", "duration": "5:57", "release_date": "1982-11-30"},
    {"music_id": "5", "title": "Yesterday", "artist": "The Beatles", "genre": "Rock", "duration": "2:05", "release_date": "1965-09-13"},
    {"music_id": "6", "title": "Billie Jean", "artist": "Michael Jackson", "genre": "Pop", "duration": "4:54", "release_date": "1983-01-02"},
    {"music_id": "7", "title": "Hey Jude", "artist": "The Beatles", "genre": "Rock", "duration": "7:11", "release_date": "1968-08-26"},
    {"music_id": "8", "title": "Like a Rolling Stone", "artist": "Bob Dylan", "genre": "Rock", "duration": "6:13", "release_date": "1965-07-20"},
    {"music_id": "9", "title": "Smells Like Teen Spirit", "artist": "Nirvana", "genre": "Grunge", "duration": "5:01", "release_date": "1991-09-10"},
    {"music_id": "10", "title": "Piano Man", "artist": "Billy Joel", "genre": "Rock", "duration": "5:38", "release_date": "1973-11-02"},
    {"music_id": "11", "title": "Purple Haze", "artist": "Jimi Hendrix", "genre": "Rock", "duration": "2:50", "release_date": "1967-03-17"},
    {"music_id": "12", "title": "Imagine", "artist": "John Lennon", "genre": "Rock", "duration": "3:03", "release_date": "1971-10-11"}

   ]

# Hashing function
# def consistent_hash_alphabetical(name, num_partitions):
#     first_letter = name[0].lower()
#     ascii_value = ord(first_letter)
#     hash_value = hashlib.sha256(str(ascii_value).encode('utf-8')).hexdigest()
#     hash_int = int(hash_value, 16)
#     partition_number = hash_int % num_partitions
#     return partition_number

def consistent_hash_alphabetical(name, num_partitions):
    # Convert the first letter of the name to lowercase
    first_letter = name[0].lower()
    
    
    # Convert the lowercase letter to an ASCII value
    ascii_value = ord(first_letter)
    
    # Calculate partition number based on ASCII value
    partition_number = ascii_value % num_partitions
    return partition_number


# Connect to MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]

for i in range(NUM_PARTITIONS):
    collection_name = f"Music_{i + 1}"
    db[collection_name].drop()

# Insert data into the appropriate collection for each partition
for music in music_data:
    partition_number = consistent_hash_alphabetical(music['title'], NUM_PARTITIONS)
    collection_name = f"Music_{partition_number + 1}"
    collection = db[collection_name]
    collection.insert_one(music)

# Close the MongoDB connection
client.close()
