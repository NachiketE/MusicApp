from djongo import models

class Song(models.Model):
    music_id = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    release_date = models.DateField()

    def __str__(self):
        return self.title
