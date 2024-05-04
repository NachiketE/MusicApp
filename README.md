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


## File directory description
README.md: ReadME of the file          
manage.py: File in Django used for administrative tasks such as starting the development server, running database migrations, and managing applications.               
requirements.txt: contains all the requirements(dependencies of the file)

./accounts: (main directory - views has python scripts to handle the operations)

__init__.py             
apps.py: contains accounts app                 
models.py: contains sample models                
views.py: This file defines views and helper functions for managing user authentication, displaying songs and trendy songs, displaying playlists, playlist creation hash function and songs within a playlist, and searching songs and artist in a Django web application, interacting with a MongoDB database.
__pycache__             
data_insertion_scripts  
templates                
admin_views.py: This file defines views and helper functions for an admin interface in a Django web application, enabling functionalities such as editing, deleting, searching, and viewing music, displaying users and banning them, and viewing playlists and songs within them, music insertion hashing with interaction with a MongoDB database for data storage and retrieval.
migrations              
urls.py: contains urls of the system

./accounts/data_insertion_scripts: ( views have python scripts for sample data insertion and urls have front end url - python function mapping)

MusicInsert.py: Scripts for inserting music in the DB
PlaylistInsert.py: Scripts for inserting playlist in the DB               
MusicPlaylistMappingInsert.py: Scripts for inserting MusicPlaylistMappingInsert in the DB   
UserInsert.py: Scripts for inserting users


./accounts/templates:(front end html, css, bootstrap files)

admin-templates         
home.html: contains HTML for home page              
search_results.html: contains HTML for displaying search results page
all_songs.html: contains HTML for displaying all songs page
playlist.html: contains HTML for displaying all songs page
single_playlist.html: contains HTML for displaying all playlists 
create_playlist.html: contains HTML for creating a playlist    
registration            
song_added.html: contains HTML for displaying song added success message

./accounts/templates/admin-templates:

add_music.html: contains HTML for adding music in the system
admin_playlists_page.html: contains HTML for viewing playlists      
delete_user_success.html: user deleted success message
add_music_success.html: music added success message         
admin_single_playlist.html: contains HTML for viewing songs in playlist      
edit_music_success.html: contains HTML for edit music success
admin_control.html: Admin home page             
admin_users_page.html: contains HTML for displaying all users page           
search_music.html: contains HTML for searching songs or artist           
delete_music_success.html: music deleted success message        
view_all_music.html: contains HTML for viewing all music 

./accounts/templates/registration:

login.html: contains HTML for login page
signup.html: contains HTML for signup page
