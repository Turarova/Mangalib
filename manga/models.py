from datetime import date

from django.db import models
from account.models import User

class Genre(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


class Novella(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    text = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    release_date = models.IntegerField()
    author_name = models.CharField(max_length=25)
    author_last_name = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre, related_name='novella')

    class Meta:
        verbose_name = 'Novella'
        verbose_name_plural = 'Novella'


    def __str__(self):
        return self.title


class NovellaImage(models.Model):
    novella = models.ForeignKey(Novella, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='novella', blank=True, null = True)

class Like(models.Model):
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    novella = models.ForeignKey(Novella, related_name='likes', on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    novella = models.ForeignKey(Novella, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.novella.title
