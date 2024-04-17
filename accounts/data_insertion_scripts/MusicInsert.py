from pymongo import MongoClient
import hashlib

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database
NUM_PARTITIONS = 5  # Number of partitions

# Sample data to insert
music_data = [

{
    "music_id": "40",
    "title": "Montero (Call Me By Your Name)",
    "artist": "Lil Nas X",
    "genre": "Pop",
    "duration": "2:17",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "41",
    "title": "Levitating",
    "artist": "Dua Lipa feat. DaBaby",
    "genre": "Pop",
    "duration": "3:23",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "42",
    "title": "Peaches",
    "artist": "Justin Bieber feat. Daniel Caesar & Giveon",
    "genre": "Pop",
    "duration": "3:18",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "43",
    "title": "Save Your Tears",
    "artist": "The Weeknd",
    "genre": "R&B",
    "duration": "3:35",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "44",
    "title": "Kiss Me More",
    "artist": "Doja Cat feat. SZA",
    "genre": "Pop",
    "duration": "3:28",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "45",
    "title": "drivers license",
    "artist": "Olivia Rodrigo",
    "genre": "Pop",
    "duration": "4:02",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "46",
    "title": "Leave The Door Open",
    "artist": "Bruno Mars, Anderson .Paak, Silk Sonic",
    "genre": "R&B",
    "duration": "4:02",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "47",
    "title": "Beat Box",
    "artist": "SpotemGottem",
    "genre": "Hip-Hop",
    "duration": "1:59",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "48",
    "title": "Calling My Phone",
    "artist": "Lil Tjay feat. 6LACK",
    "genre": "Hip-Hop",
    "duration": "3:25",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "49",
    "title": "Heartbreak Anniversary",
    "artist": "Giveon",
    "genre": "R&B",
    "duration": "3:17",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "50",
    "title": "Mood",
    "artist": "24kGoldn feat. iann dior",
    "genre": "Pop",
    "duration": "2:20",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "51",
    "title": "Beautiful Mistakes",
    "artist": "Maroon 5 feat. Megan Thee Stallion",
    "genre": "Pop",
    "duration": "3:47",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "52",
    "title": "Good Days",
    "artist": "SZA",
    "genre": "R&B",
    "duration": "4:39",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "53",
    "title": "Up",
    "artist": "Cardi B",
    "genre": "Hip-Hop",
    "duration": "2:36",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "54",
    "title": "Without You",
    "artist": "The Kid LAROI",
    "genre": "Pop",
    "duration": "2:41",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "55",
    "title": "You Broke Me First",
    "artist": "Tate McRae",
    "genre": "Pop",
    "duration": "2:49",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "56",
    "title": "Favor",
    "artist": "Lonr. feat. 6LACK",
    "genre": "R&B",
    "duration": "3:25",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "57",
    "title": "Solid",
    "artist": "Young Stoner Life, Young Thug, Gunna feat. Drake",
    "genre": "Hip-Hop",
    "duration": "3:11",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "58",
    "title": "Hold On",
    "artist": "Justin Bieber",
    "genre": "Pop",
    "duration": "2:51",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "59",
    "title": "Goosebumps",
    "artist": "Travis Scott & HVME",
    "genre": "Hip-Hop",
    "duration": "2:43",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "60",
    "title": "Blinding Lights",
    "artist": "The Weeknd",
    "genre": "Pop",
    "duration": "3:20",
    "release_date": "2021-04-01",
    "trendy": "1"
},
{
    "music_id": "61",
    "title": "Forever After All",
    "artist": "Luke Combs",
    "genre": "Country",
    "duration": "3:53",
    "release_date": "2021-04-01",
    "trendy": "1"
}


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
    hash_value = 0
    for char in name:
        hash_value += ord(char)    

    hash_value *= 131
    
    bucket_number = hash_value % num_partitions

    return bucket_number


# Connect to MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]


# Insert data into the appropriate collection for each partition
for music in music_data:
    partition_number = consistent_hash_alphabetical(music['title'], NUM_PARTITIONS)
    collection_name = f"Music_{partition_number + 1}"
    collection = db[collection_name]
    collection.insert_one(music)

# Close the MongoDB connection
client.close()