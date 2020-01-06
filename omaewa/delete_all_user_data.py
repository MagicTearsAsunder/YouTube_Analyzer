def delete_all(username):
    import os
    import shutil
    from django.conf import settings
    from .models import (
        StatsZipFiles, YouTubeTextStats, HeatmapFiles,
        WordClouds, Activities, TopChannels, TopVideos
    )

    all_models = [
        StatsZipFiles,
        YouTubeTextStats,
        WordClouds,
        Activities,
        HeatmapFiles,
        TopChannels,
        TopVideos,
    ]

    for the_model in all_models:
        try:
            out_data = the_model.objects.get(username_id=username)
        except the_model.MultipleObjectsReturned:
            out_data = the_model.objects.filter(username_id=username)
        except the_model.DoesNotExist:
            continue
        out_data.delete()

    try:
        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'extracted', username))
    except FileNotFoundError:
        pass
