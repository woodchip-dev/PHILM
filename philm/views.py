from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import User
from .models import Film, Genres, Years, Reviews, Person
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate, logout


# AUTH

def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            auth_login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    return render(request, 'philm/login.html', context = {})


@login_required(login_url = '/login/', redirect_field_name = None)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)



# MAIN, MOVIE, USER PAGES

@login_required(login_url = '/login/', redirect_field_name = None)
def index(request):
    genre_list = Genres.objects.all()
    year_list = Years.objects.all()
     
    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        keyword = keyword.split(' ')

        incl_genre = []
        excl_genre = []

        for genre in genre_list:
            genre = str(genre).rstrip()
            idx = request.POST.get(genre, '')
            if idx is '1':
                incl_genre.append(genre)
            elif idx is '2':
                excl_genre.append(genre)

        incl_year = []
        excl_year = []

        for year in year_list:
            year = str(year).rstrip()
            idx = request.POST.get(year, '')
            if idx is '1':
                incl_year.append(year)
            elif idx is '2':
                excl_year.append(year)

        title_query = Q()
        for key in keyword:
            title_query |= Q(film_title__contains = key)

        ingen_query = Q()
        for ingen in incl_genre:
            ingen_query |= Q(film_genres__exact = ingen)

        exgen_query = ~Q()
        for exgen in excl_genre:
            exgen_query &= ~Q(film_genres__exact = exgen)

        inyear_query = Q()
        for inyear in incl_year:
            inyear_query |= Q(film_year__exact = inyear)

        exyear_query = ~Q()
        for exyear in excl_year:
            exyear_query &= ~Q(film_year__exact = exyear)

        film_list = Film.objects.filter(title_query & (exgen_query & ingen_query) & (inyear_query & exyear_query))

    else:
        film_list = Film.objects.all()


    context = {'film_list': film_list, 'genre_list': genre_list, 'year_list': year_list, 'person': request.user}
    return render(request, 'philm/index.html', context)


@login_required(login_url = '/login/', redirect_field_name = None)
def movie(request, film_id):
    film = Film.objects.get(id = film_id)
    reviews = Reviews.objects.filter(reviews_fid = film_id)

    context = {'film': film, 'review_list': reviews, 'person': request.user}
    return render(request, 'philm/movie.html', context)


@login_required(login_url = '/login/', redirect_field_name = None)
def person(request, user_id):
    username = User.objects.get(username = user_id)
    person = Person.objects.get(person_user = username)

    context = {'user': person, 'person': request.user}
    return render(request, 'philm/user.html', context)



# USER ACTIONS

@login_required(login_url = '/login/', redirect_field_name = None)
def post_review(request, film_id):
    if request.method == 'POST':
        rev = request.POST.get('rev', '')
        username = User.objects.get(username = request.user.username)
        person = Person.objects.get(person_user = username)
        film = Film.objects.get(id = film_id)

        Reviews.objects.create(reviews_uid = person, reviews_fid = film, reviews_review = rev)

        # redirect w/JS in html file
        #<script>
        #window.setTimeout(function(){
        #window.location.href = "m/film_id";
        #}, 2000);
        #<script>

        #context = {'film': film, 'review_list': reviews, 'person': request.user}
        return render(request, 'philm/review.html', context={})
    else:
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


@login_required(login_url = '/login/', redirect_field_name = None)
def edit_review(request, terms):
    context = {}
    return render(request, 'philm/movie.html', context)