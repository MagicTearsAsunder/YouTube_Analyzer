from django.contrib import admin
from .models import (
    CustomUser, StatsZipFiles, YouTubeTextStats, HeatmapFiles,
    WordClouds, Activities, TopChannels, TopVideos
)

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(StatsZipFiles)
admin.site.register(YouTubeTextStats)
admin.site.register(HeatmapFiles)
admin.site.register(WordClouds)
admin.site.register(Activities)
admin.site.register(TopChannels)
admin.site.register(TopVideos)
