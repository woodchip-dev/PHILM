from django.urls import path, include
from . import views


app_name = 'philm'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('m/<slug:film_id>/', views.movie, name = 'movie'),
    path('u/<slug:user_id>/', views.person, name = 'person'),
    path('m/<slug:film_id>/post_review/', views.post_review, name = 'post_review'),
    path('login/', views.login, name = 'login'),
    path('logout/', views.logout_view, name='logout_view'),
]
