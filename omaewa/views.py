from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserForm, UploadFileForm
from .email_confirmation import send_email_confirmation
from .handle_zip_file import GenerateStats
from .delete_all_user_data import delete_all
from .models import (
    CustomUser, StatsZipFiles, YouTubeTextStats, HeatmapFiles,
    WordClouds, Activities, TopChannels, TopVideos
)


def user_registration(request, *args, **kwargs):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    data_from_form = CustomUserForm(request.POST or None)
    message = None

    if data_from_form.is_valid():
        new_user = data_from_form.save()
        new_user.set_password(new_user.password)
        new_user.save()
        send_email_confirmation(new_user, request.get_host())
        message = "Please, check your e-mail."
        data_from_form = CustomUserForm()

    context = {
        'form': data_from_form,
        'message': message
    }
    return render(request, 'omaewa/register.html', context)


def conf_reg(request, the_uid, *args, **kwargs):
    the_user = get_object_or_404(CustomUser, random_url=the_uid)
    if not the_user.is_confirmed:
        the_user.is_confirmed = True
        the_user.random_url = None
        the_user.save()
    else:
        raise ValueError(f'An unexpected error: {the_user}')

    return HttpResponseRedirect(reverse('user_login'))


def user_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('index'))

    message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_confirmed:
                message = 'Please, confirm your e-mail.'
            elif user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                message = 'Your account was inactive.'
        else:
            message = 'Incorrect username and/or password'

    context = {
        'message': message
    }

    return render(request, 'omaewa/login.html', context)


@login_required
def user_logout(request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


@login_required
def youtube(request, *args, **kwargs):
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            delete_all(request.user.username)
            new_zip = StatsZipFiles.objects.update_or_create(
                username=request.user,
                defaults={'file': form.cleaned_data['file']}
            )

            yt_dt = GenerateStats(new_zip[0])

            del new_zip

            if yt_dt.is_error:
                context = {
                    'form': UploadFileForm(),
                    'message': yt_dt.error_message
                }
                return render(request, 'omaewa/youtube.html', context)

            YouTubeTextStats.objects.update_or_create(
                username=request.user,
                defaults=yt_dt.text_data
            )

            try:
                htmap = HeatmapFiles.objects.filter(username=request.user)
            except HeatmapFiles.DoesNotExist:
                pass
            else:
                htmap.delete()
            finally:
                for i in yt_dt.files_data['heatmaps']:
                    HeatmapFiles.objects.create(username=request.user, file=i)

            WordClouds.objects.update_or_create(
                username=request.user,
                defaults={'file': yt_dt.files_data['wordcloud']}
            )

            defies = {
                'activity_by_hour': yt_dt.files_data['activity_by_hour'],
                'activity_by_weekday': yt_dt.files_data['activity_by_weekday']
            }

            try:
                activs = Activities.objects.get(username=request.user)
            except Activities.DoesNotExist:
                pass
            else:
                activs.delete()
            finally:
                Activities.objects.create(username=request.user, **defies)

            tops = {
                TopChannels: yt_dt.frame_channels,
                TopVideos: yt_dt.frame_videos
            }

            for the_model in tops:
                try:
                    top_five = the_model.objects.filter(username=request.user)
                except top_five.DoesNotExist:
                    pass
                else:
                    top_five.delete()
                finally:
                    for index, row in tops[the_model].iterrows():
                        the_model.objects.create(
                            username=request.user,
                            title=row['title'],
                            the_url=row['the_url'],
                            counts=row['counts']
                        )

            del yt_dt

            return HttpResponseRedirect(reverse('index'))

    return render(request, 'omaewa/youtube.html', {'form': form})


def index(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_login'))

    if request.method == 'POST':
        username = request.user.username
        delete_all(username)
        return HttpResponseRedirect(reverse('youtube'))
    else:
        username = request.user
        all_models = {
            YouTubeTextStats: 'ytts',
            WordClouds: 'wrdcld',
            Activities: 'activs',
            HeatmapFiles: 'htmap',
            TopChannels: 'topchs',
            TopVideos: 'topvids',
        }

        context = {}

        for the_model in all_models.keys():
            try:
                out_data = the_model.objects.get(username_id=username)
            except the_model.MultipleObjectsReturned:
                out_data = the_model.objects.filter(username_id=username)
            except the_model.DoesNotExist:
                return HttpResponseRedirect(reverse('youtube'))

            context[all_models[the_model]] = out_data
        return render(request, 'omaewa/index.html', context)


def category_page(request, *args, **kwargs):
    return render(request, 'omaewa/category-page.html', {})


def post_page(request, *args, **kwargs):
    return render(request, 'omaewa/post-page.html', {})
