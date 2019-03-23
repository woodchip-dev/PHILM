# Generated by Django 2.1.5 on 2019-03-22 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import philm.models
import philm.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('film_title', models.CharField(max_length=200, verbose_name='Title')),
                ('film_poster', models.ImageField(null=True, storage=philm.storage.OverwriteStorage(), upload_to=philm.models.Film.get_poster_path, verbose_name='Poster')),
                ('film_imdb', models.SlugField(null=True, verbose_name='IMDB ID')),
            ],
            options={
                'ordering': ['film_title', 'film_year'],
            },
        ),
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('genres_genre', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True, verbose_name='Genre')),
            ],
            options={
                'verbose_name_plural': 'Genres',
                'ordering': ['genres_genre'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_avatar', models.ImageField(null=True, storage=philm.storage.OverwriteStorage(), upload_to=philm.models.Person.get_avatar_path, verbose_name='Avatar')),
                ('person_user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'People',
                'ordering': ['person_user'],
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviews_review', models.TextField(max_length=5000, verbose_name='Review')),
                ('reviews_fid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='philm.Film', verbose_name='Film')),
                ('reviews_uid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='philm.Person', verbose_name='User')),
            ],
            options={
                'verbose_name_plural': 'Reviews',
                'ordering': ['reviews_uid', 'reviews_fid'],
            },
        ),
        migrations.CreateModel(
            name='Years',
            fields=[
                ('years_year', models.PositiveSmallIntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Year')),
            ],
            options={
                'verbose_name_plural': 'Years',
                'ordering': ['years_year'],
            },
        ),
        migrations.AddField(
            model_name='film',
            name='film_genres',
            field=models.ManyToManyField(to='philm.Genres', verbose_name='Genres'),
        ),
        migrations.AddField(
            model_name='film',
            name='film_year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='philm.Years', verbose_name='Year'),
        ),
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together={('reviews_uid', 'reviews_fid')},
        ),
    ]