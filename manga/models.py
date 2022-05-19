from django.db import models


class Genre(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Novella(models.Model):
    genre = models.ForeignKey(Genre, related_name='mangas', on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    created_at = models.DateTimeField()
    author_name = models.CharField(max_length=25)
    author_last_name = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class NovellaImage(models.Model):
    novell = models.ForeignKey(Novella, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='novells', blank=True, null = True)


