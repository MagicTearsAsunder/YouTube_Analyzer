import os
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    username = models.CharField(
        verbose_name='Username',
        primary_key=True,
        max_length=50
    )
    password = models.CharField(verbose_name='Password', max_length=100)

    email = models.EmailField(verbose_name='Email', unique=True, max_length=50)

    first_name = models.CharField(
        verbose_name='First name',
        max_length=50,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=50,
        null=True,
        blank=True
    )
    is_confirmed = models.BooleanField(
        verbose_name='Is confirmed',
        default=False
    )
    random_url = models.UUIDField(default=uuid.uuid4, null=True, blank=True)


class StatsZipFiles(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/zipfiles/<username>.zip
        filename = instance.username_id + '.zip'
        return os.path.join('zipfiles', f'{filename}')

    file = models.FileField(
        verbose_name='ZipFile',
        upload_to=user_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['zip'])],
        blank=False
    )
    username = models.OneToOneField(
        'CustomUser',
        verbose_name='Username_id',
        on_delete=models.CASCADE,
        blank=False
    )


class YouTubeTextStats(models.Model):
    username = models.OneToOneField(
        'CustomUser',
        verbose_name='Username',
        on_delete=models.CASCADE,
        blank=False
    )
    count_searches = models.PositiveIntegerField(
        verbose_name='Count_Searches',
        blank=False
    )
    first_search = models.CharField(
        max_length=200,
        verbose_name='First_Search',
        blank=True,
        null=True
    )
    count_liked = models.PositiveIntegerField(
        verbose_name='Count_Liked',
        blank=False
    )
    first_liked = models.CharField(
        max_length=200,
        verbose_name='First_Liked',
        blank=True,
        null=True
    )
    first_liked_url = models.URLField(
        verbose_name='First_Liked_Url',
        blank=True,
        null=True
    )
    count_watched = models.PositiveIntegerField(
        verbose_name='Count_Watched',
        blank=False
    )
    first_watched_title = models.CharField(
        max_length=200,
        verbose_name='First_Watched_Title',
        blank=True,
        null=True
    )
    first_watched_url = models.URLField(
        verbose_name='First_Watched_Url',
        blank=True,
        null=True
    )
    first_watched_dt = models.DateTimeField(
        verbose_name='First_Watched_Dt',
        blank=True,
        null=True
    )


class HeatmapFiles(models.Model):
    def user_directory_path(instance, filename):
        # will be uploaded to MEDIA_ROOT/extracted/<username>/heatmap/<fname>
        return os.path.join(
            'extracted', f'{instance.username_id}', 'heatmap', f'{filename}'
        )

    username = models.ForeignKey(
        'CustomUser',
        verbose_name='Username',
        on_delete=models.CASCADE,
        blank=False
    )
    file = models.ImageField(
        verbose_name='Heatmap',
        upload_to=user_directory_path,
        blank=False
    )


class WordClouds(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/extracted/<username>/wordcloud/
        return os.path.join(
            'extracted', f'{instance.username_id}', 'wordcloud', f'{filename}'
        )
    username = models.OneToOneField(
        'CustomUser',
        verbose_name='Username',
        on_delete=models.CASCADE,
        blank=False
    )
    file = models.ImageField(
        verbose_name='WordCloud',
        upload_to=user_directory_path,
        blank=False
    )


class Activities(models.Model):
    def user_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/extracted/<username>/activities/
        return os.path.join(
            'extracted', f'{instance.username_id}', 'activities', f'{filename}'
        )

    username = models.OneToOneField(
        'CustomUser',
        verbose_name='Username',
        on_delete=models.CASCADE,
        blank=False
    )
    activity_by_hour = models.ImageField(
        verbose_name='Activity_By_Hour',
        upload_to=user_directory_path,
        blank=False
    )
    activity_by_weekday = models.ImageField(
        verbose_name='Activity_By_Weekday',
        upload_to=user_directory_path,
        blank=False
    )


class TopChannels(models.Model):
    username = models.ForeignKey(
        'CustomUser',
        verbose_name='Username',
        on_delete=models.CASCADE,
        blank=False
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Title',
        blank=True,
        null=True
    )
    the_url = models.URLField(
        verbose_name='Channel_Url',
        blank=True,
        null=True
    )
    counts = models.PositiveIntegerField(
        verbose_name='Counts',
        blank=False
    )


class TopVideos(models.Model):
    username = models.ForeignKey(
        'CustomUser',
        verbose_name='Username',
        on_delete=models.CASCADE,
        blank=False
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Title',
        blank=True,
        null=True
    )
    the_url = models.URLField(
        verbose_name='Video_Url',
        blank=True,
        null=True
    )
    counts = models.PositiveIntegerField(
        verbose_name='Counts',
        blank=False
    )
