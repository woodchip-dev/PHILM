import os
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from philm.storage import OverwriteStorage


class Genres(models.Model):
    genres_genre =  models.CharField(max_length=15, unique=True, primary_key=True, verbose_name='Genre')

    def __str__(self):
        return u'%s' % (self.genres_genre)

    class Meta:
        ordering = ['genres_genre']
        verbose_name_plural = 'Genres'


class Years(models.Model):
    years_year =  models.PositiveSmallIntegerField(unique=True, primary_key=True, verbose_name='Year')

    def __str__(self):
        return u'%s' % (self.years_year)

    class Meta:
        ordering = ['years_year']
        verbose_name_plural = 'Years'


class Film(models.Model):
    def get_poster_path(self, filename):
        ext = filename.split('.')[-1]
        filename = '%s_%s.%s' % (self.film_title, self.film_year, ext)
        return os.path.join('static/philm/img/posters/', filename)

    film_title   = models.CharField(max_length=200, verbose_name='Title') # default max_length=200
    film_year    = models.ForeignKey(Years, on_delete=models.SET_NULL, null=True, verbose_name='Year')
    film_poster  = models.ImageField(upload_to=get_poster_path, storage=OverwriteStorage(), null=True, verbose_name='Poster')
    film_genres  = models.ManyToManyField(Genres, verbose_name='Genres')
    film_imdb    = models.SlugField(null=True, verbose_name='IMDB ID')

    def __str__(self):
        return u'%s (%s)' % (self.film_title, self.film_year)

    class Meta:
        ordering = ['film_title', 'film_year']


class Person(models.Model):
    def get_avatar_path(self, filename):
        ext = filename.split('.')[-1]
        filename = '%s.%s' % (self.person_user, ext)
        return os.path.join('static/philm/img/avatars/', filename)

    person_user   = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, verbose_name='User')
    person_avatar = models.ImageField(upload_to=get_avatar_path, storage=OverwriteStorage(), null=True, verbose_name='Avatar')

    def __str__(self):
        return u'%s' % (self.person_user)

    class Meta:
        ordering = ['person_user']
        verbose_name_plural = 'People'


class Reviews(models.Model):
    reviews_uid     = models.ForeignKey(Person, on_delete=models.SET_NULL, null=True, verbose_name='User')
    reviews_fid     = models.ForeignKey(Film, on_delete=models.SET_NULL, null=True, verbose_name='Film')
    reviews_review  = models.TextField(max_length=5000, verbose_name='Review')
    reviews_created = models.DateTimeField(default = datetime.now, blank = True, null = True)

    def __str__(self):
        return u'%s :: %s' % (self.reviews_uid, self.reviews_fid)

    class Meta:
        ordering = ['reviews_uid', 'reviews_fid']
        verbose_name_plural = 'Reviews'
        unique_together = ("reviews_uid", "reviews_fid")