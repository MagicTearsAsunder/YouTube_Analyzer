import os
import io
import json
import calendar
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from zipfile import ZipFile, BadZipFile
from wordcloud import WordCloud

from django.conf import settings
from django.core.files.images import ImageFile

from .delete_all_user_data import delete_all


class GenerateStats:
    def __init__(self, user_model):
        user_name = str(user_model.username)
        self.the_path = os.path.join(
            settings.MEDIA_ROOT, 'extracted', user_name
        )

        self.is_error = 0
        self.error_message = []

        path_eng = {
            'liked_dir': ('playlists', 'likes.json'),
            'search_dir': ('history', 'search-history.json'),
            'watched_dir': ('history', 'watch-history.json')
        }

        list_file_exists = [
            'Takeout/YouTube/playlists/likes.json',
            'Takeout/YouTube/history/search-history.json',
            'Takeout/YouTube/history/watch-history.json'
        ]

        try:
            with ZipFile(user_model.file) as f:
                info_list = [
                    i for i in f.namelist() if i.startswith('Takeout/YouTube')
                ]

                for i in list_file_exists:
                    if i not in info_list:
                        self.is_error = 1
                        self.error_message.append('Expected files not found')
                        delete_all(user_name)
                        return

                f.extractall(members=info_list, path=self.the_path)

        except BadZipFile as error:
            print(error)
            self.is_error = 1
            self.error_message.append('Invalid .zip file')
            delete_all(user_name)
            return

        if not os.path.exists(os.path.join(self.the_path, 'heatmap')):
            os.mkdir(os.path.join(self.the_path, 'heatmap'))

        if not os.path.exists(os.path.join(self.the_path, 'activities')):
            os.mkdir(os.path.join(self.the_path, 'activities'))

        self.the_path = os.path.join(self.the_path, 'Takeout', 'YouTube')
        self.path_language = path_eng
        self.text_data = {}
        self.files_data = {
            'wordcloud': None,
            'heatmaps': [],
            'activity_by_hour': None,
            'activity_by_weekday': None
        }

        self.search_history()
        self.liked()
        matplotlib.use('Agg')
        self.watched()

    def search_history(self):
        search_dir = os.path.join(
            self.the_path,
            *(self.path_language['search_dir'])
        )

        all_search = GenerateStats.__extract_json(search_dir)
        if all_search == 1:
            self.is_error = 1
            self.error_message.append('search-history.json decode error')
            return

        count_searches = len(all_search)
        first_search = all_search[-1]['title'][13:]

        self.text_data['count_searches'] = count_searches
        self.text_data['first_search'] = first_search

        all_words = ' '.join([i['title'][13:] for i in all_search])

        wordcloud = WordCloud(
            width=450,
            height=450,
            background_color='white',
            min_font_size=10).generate(all_words)

        stream = io.BytesIO()
        stream.name = 'wordcloud.png'
        wordcloud.to_file(stream)
        file = ImageFile(stream)
        self.files_data['wordcloud'] = file

    def liked(self):
        liked_dir = os.path.join(
            self.the_path,
            *(self.path_language['liked_dir'])
        )

        all_liked = GenerateStats.__extract_json(liked_dir)

        if all_liked == 1:
            self.is_error = 1
            self.error_message.append('likes.json decode error')
            return

        count_liked = len(all_liked)
        first_liked = all_liked[-1]['snippet']['title']
        temp = all_liked[-1]['contentDetails']['videoId']
        first_liked_url = 'https://www.youtube.com/watch?v=' + temp

        self.text_data['count_liked'] = count_liked
        self.text_data['first_liked'] = first_liked
        self.text_data['first_liked_url'] = first_liked_url

    def watched(self):
        watched_dir = os.path.join(
            self.the_path,
            *(self.path_language['watched_dir'])
        )
        all_watched = GenerateStats.__extract_json(watched_dir)

        if all_watched == 1:
            self.is_error = 1
            self.error_message.append('watch-history.json decode error')
            return

        count_watched = len(all_watched)
        first_watched_title = all_watched[-1]['title'][8:]
        first_watched_url = all_watched[-1]['titleUrl']
        first_watched_dt = pd.to_datetime(
            all_watched[-1]['time']
        ).tz_convert('Europe/Moscow').to_pydatetime()

        self.text_data['count_watched'] = count_watched
        self.text_data['first_watched_title'] = first_watched_title
        self.text_data['first_watched_url'] = first_watched_url
        self.text_data['first_watched_dt'] = first_watched_dt

        def cnvrt_time(x):
            x = pd.to_datetime(x).tz_convert('Europe/Moscow')
            return [x.day, x.month_name(), x.year, x.hour, x.day_name()]

        time_list = [cnvrt_time(i["time"]) for i in all_watched]

        all_channels = [
            i['subtitles'][0].values()
            for i in all_watched if i.get('subtitles')
        ]
        all_videos = [
            [i['title'][8:], i['titleUrl']]
            for i in all_watched if i.get('titleUrl')
        ]

        df = pd.DataFrame(data=time_list, columns=[
            'Day', 'Month', 'Year', 'Hour', 'Weekday'
        ])

        frame_channels = pd.DataFrame(
            data=all_channels, columns=['title', 'the_url']
        )
        frame_videos = pd.DataFrame(
            data=all_videos, columns=['title', 'the_url']
        )

        def the_heatmap(the_frame):
            list_of_years = list(df.Year.drop_duplicates())
            list_of_years.sort()
            sns.set()

            monthes = [
                'January', 'February', 'March', 'April',
                'May', 'June', 'July', 'August',
                'September', 'October', 'November', 'December'
            ]

            for year in list_of_years:
                frame_year = df[['Day', 'Month']][df['Year'] == year]
                frame_year = frame_year.groupby(
                    frame_year.columns.tolist()).size().reset_index().rename(
                    columns={0: 'Counts'}
                )
                list_to_be_appended = []

                for idx, month in enumerate(monthes):
                    temp_month = set(
                        frame_year['Day'][frame_year['Month'] == month]
                    )
                    days_in_month = set(
                        range(1, (calendar.monthrange(year, idx+1)[1] + 1))
                    )
                    month_differ = days_in_month - temp_month

                    while month_differ:
                        list_to_be_appended.append(
                            [month_differ.pop(), month, 0]
                        )

                appending_frame = pd.DataFrame(
                    data=list_to_be_appended,
                    columns=['Day', 'Month', 'Counts']
                )

                frame_year = frame_year.append(appending_frame)
                frame_year['Month'] = pd.Categorical(
                    frame_year['Month'], categories=monthes, ordered=True
                )
                frame_year.sort_values(by='Month', inplace=True)

                htmap = frame_year.pivot("Month", "Day", "Counts")
                f, ax = plt.subplots(figsize=(18, 7))  # 10 6
                new = sns.heatmap(
                    htmap, annot=True, fmt='.0f', linewidths=.5, ax=ax
                )
                new.set_title(f'{year}')

                stream = io.BytesIO()
                new.get_figure().savefig(stream, format='png', quality=95)
                stream.name = f'{year}.png'
                file = ImageFile(stream)
                self.files_data['heatmaps'].append(file)

        def activity_by_hour(the_frame):
            the_frame = the_frame.groupby(the_frame.columns.tolist()).size()
            sns.set(style="white", context="talk")

            f, ax = plt.subplots(1, 1, figsize=(10, 4), sharex=True)
            x = list(the_frame.index)
            y = list(the_frame)
            sns.barplot(x=x, y=y, palette="rocket", ax=ax)
            ax.axhline(0, color="k", clip_on=False)
            ax.set_ylabel("Overview")
            ax.set_title("ACTIVITY BY HOUR OF DAY")

            stream = io.BytesIO()
            ax.get_figure().savefig(stream, format='png')
            stream.name = 'activity_by_hour.png'
            file = ImageFile(stream)
            self.files_data['activity_by_hour'] = file

        def activity_by_weekday(the_frame):
            the_frame = the_frame.groupby(
                the_frame.columns.tolist()).size()
            weekdays = ['Monday', 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday']
            the_frame.index = pd.Categorical(
                the_frame.index, categories=weekdays, ordered=True
            )
            the_frame.sort_index(inplace=True)
            sns.set(style="white", context="talk")

            f, ax = plt.subplots(1, 1, figsize=(10, 4), sharex=True)
            x = list(the_frame.index)
            y = list(the_frame)
            sns.barplot(x=x, y=y, palette="rocket", ax=ax)
            ax.axhline(0, color="k", clip_on=False)
            ax.set_ylabel("Overview")
            ax.set_title("ACTIVITY BY DAY OF WEEK")

            stream = io.BytesIO()
            ax.get_figure().savefig(stream, format='png')
            stream.name = 'activity_by_weekday.png'
            file = ImageFile(stream)
            self.files_data['activity_by_weekday'] = file

        def top_five_watched(the_frame):
            the_frame = the_frame.groupby(
                the_frame.columns.tolist()).size().reset_index().rename(
                columns={0: 'counts'}
            )
            the_frame = the_frame.sort_values(by='counts', ascending=False)
            the_frame = the_frame.head()
            return the_frame

        plt.rcParams['figure.dpi'] = 60
        plt.rcParams.update({'font.size': 12})

        the_heatmap(df[['Day', 'Month', 'Year']])
        activity_by_hour(df[['Hour']])
        activity_by_weekday(df[['Weekday']])
        plt.close('all')
        self.frame_channels = top_five_watched(frame_channels)
        self.frame_videos = top_five_watched(frame_videos)

    def __extract_json(directory):
        with open(directory, 'r') as f:
            try:
                all_json = json.load(f)
            except json.decoder.JSONDecodeError as error:
                print(error)
                return 1
            else:
                return all_json
