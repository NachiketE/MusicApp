from pymongo import MongoClient

# MongoDB connection settings
MONGO_HOST = 'localhost'  # MongoDB host
MONGO_PORT = 27017  # MongoDB port
DATABASE_NAME = 'music'  # Name of your MongoDB database

# Sample data to insert
user_data = [
    {"user_id": "1", "username": "john_doe", "password": "hashed_password_1", "email": "john@example.com"},
    {"user_id": "2", "username": "jane_smith", "password": "hashed_password_2", "email": "jane@example.com"},
    {"user_id": "3", "username": "mike_wilson", "password": "hashed_password_3", "email": "mike@example.com"},
    {"user_id": "4", "username": "sara_jones", "password": "hashed_password_4", "email": "sara@example.com"},
    {"user_id": "5", "username": "david_brown", "password": "hashed_password_5", "email": "david@example.com"},
    {"user_id": "6", "username": "emily_rodriguez", "password": "hashed_password_6", "email": "emily@example.com"},
    {"user_id": "7", "username": "alexander_nguyen", "password": "hashed_password_7", "email": "alexander@example.com"},
    {"user_id": "8", "username": "lisa_kim", "password": "hashed_password_8", "email": "lisa@example.com"},
    {"user_id": "9", "username": "peter_anderson", "password": "hashed_password_9", "email": "peter@example.com"},
    {"user_id": "10", "username": "olivia_garcia", "password": "hashed_password_10", "email": "olivia@example.com"}
]


# Connect to MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[DATABASE_NAME]

# Clear the "User" collection
# db["auth_user"].drop()

# Insert data into the "User" collection
db["auth_user"].insert_many(user_data)

# Close the MongoDB connection
client.close()
