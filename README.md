# Project description
Music Playlist Management System project is a web-based music management system with two distinct user roles: Music Admins and Music Listeners. Music Admins have unrestricted access to the system, allowing them to manage music and user databases by adding or deleting music and viewing or banning users. Meanwhile, Music Listeners can utilize the web application to search, create, and manage playlists, adding or removing music as desired. To handle large volumes of data, a distributed database system employing MongoDB and a secure hash function for efficient data storage and retrieval will be implemented, ensuring scalability and performance.

You can view the walkthrough of the project and code flow explanation at the following link:
```bash
https://youtu.be/pyy_JM3lvRM
```

## Installation for MongoDB


```bash
brew install mongodb-community
```
```bash
brew services start mongodb/brew/mongodb-community
```
The following command will start MongoDB locally:
```bash
mongosh
```

## Installation for Django
Git clone the project:
```bash
https://github.com/NachiketE/MusicApp
```
Create a virtual environment(optional) and install the requirements:
```bash
pip install -r requirements.txt
```
## Run Django


Run migrations:
```bash
python manage.py migrate
```
Start the development server:
```bash
python manage.py runserver
```

## Usage

The Django web server (Music listener's page) can be found at: 
```bash
http://127.0.0.1:8000/
```

The Django web server (Music admin's page) can be found at: 
```bash
http://127.0.0.1:8000/admin-control/
```