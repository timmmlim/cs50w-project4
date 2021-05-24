from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages

from .models import User, Post
from .forms import PostForm

def index(request):

    # get all posts
    posts = Post.objects.all()

    # render new post form
    form = PostForm()

    return render(request, "network/index.html", {'posts': posts, 'form': form})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def post(request, post_id):
    '''
    renders specific view for individual posts
    '''
    pass

def add_post(request):
    form = PostForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        else:
            messages.error(request, "Please enter some text!")

    return HttpResponseRedirect(reverse("index"))
    

def get_user(request, user_id):
    user = User.objects.get(id=user_id)

    print(request.user)
    print(user)
    
    # no. of followers
    followers = user.followers.all()
    following = user.following.all()

    n_followers = len(followers)
    n_following = len(following)

    # posts
    posts = user.posts.all()

    # check if current user can follow user_id
    if (request.user in followers) or (request.user==user):
        follow_btn = False
    else:
        follow_btn = True

    return render(request, "network/user.html", {'user': user, 'n_followers': n_followers, 
    'n_following': n_following, 'posts': posts, 'follow_btn': follow_btn})