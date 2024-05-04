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
README.md:
db.sqlite3:              
manage.py               
requirements.txt

./accounts: (main directory - views has python scripts to handle the operations)

__init__.py             apps.py                 models.py               views.py
__pycache__             data_insertion_scripts  templates
admin.py                forms.py                tests.py
admin_views.py          migrations              urls.py

./accounts/data_insertion_scripts: ( views have python scripts for sample data insertion and urls have front end url - python function mapping)

MusicInsert.py                  PlaylistInsert.py               sample.py
MusicPlaylistMappingInsert.py   UserInsert.py


./accounts/templates:(front end html, css, bootstrap files)

admin-templates         home.html               search_results.html
all_songs.html          playlist.html           single_playlist.html
create_playlist.html    registration            song_added.html

./accounts/templates/admin-templates:

add_music.html                  admin_playlists_page.html       delete_user_success.html
add_music_success.html          admin_single_playlist.html      edit_music_success.html
admin_control.html              admin_users_page.html           search_music.html
admin_music_page.html           delete_music_success.html       view_all_music.html

./accounts/templates/registration:

login.html      signup.html
