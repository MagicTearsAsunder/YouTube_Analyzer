from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.user_registration, name='user_registration'),
    path('login', views.user_login, name='user_login'),
    path('logout', views.user_logout, name='user_logout'),
    path('confirm/<uuid:the_uid>', views.conf_reg, name='conf_reg'),
    path('category', views.category_page, name='category_page'),
    path('posting', views.post_page, name='post_page'),
    path('youtube', views.youtube, name='youtube')
]
