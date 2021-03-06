import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt 

from .models import User, Post, Like, UserFollowing
from .forms import PostForm

# global variables
n_posts = 10

def index(request):

    # get all posts
    posts = Post.objects.all()

    # limit to n_posts per page
    paginator = Paginator(posts, n_posts)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # render new post form
    form = PostForm()

    return render(request, "network/index.html", {'page_obj': page_obj, 'form': form})

def following(request):
    '''
    similar to index, but returns the posts from users currently followed
    '''
    
    if request.user.is_authenticated:
        # get the users being followed by request.user
        following = [userfollowing.following_user_id for userfollowing in request.user.following.all()]
        following.append(request.user)

        # get the relevant posts
        posts = Post.objects.filter(user__in=following)
        paginator = Paginator(posts, n_posts)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # render new post form
        form = PostForm()

        return render(request, 'network/index.html', {'page_obj': page_obj, 'form': form})

    else:
        return HttpResponseRedirect(reverse('login'))

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

@csrf_exempt
def post(request, post_id):
    '''
    query for specific post
    '''

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": 'Post not found.'}, status=404)
    
    # return post contents
    if request.method == 'GET':
        result = post.serialize()
        result['likes'] = post.likes.count()
        return JsonResponse(result)
    
    # edit post contents
    elif request.method == 'PUT':
        data = json.loads(request.body)
        post.content = data['content']
        post.save()
        return HttpResponse(status=204)

    else:
        return JsonResponse({
            'error': 'GET or PUT request required'
        }, status=400)


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
    try:
        followers.get(user_id=request.user)
        follow_btn = False

    except ObjectDoesNotExist:
        follow_btn = True

    # check if user is self
    if request.user == user:
        is_self = True
    else:
        is_self = False

    return render(request, "network/user.html", {'user': user, 'n_followers': n_followers, 
    'n_following': n_following, 'posts': posts, 'follow_btn': follow_btn, 'is_self': is_self})


def follow_user(request, user_id):
    if request.user.is_authenticated:
        target_user = User.objects.get(id=user_id)
        followers = target_user.followers.all()

        # unfollow
        try:
            curr_record = followers.get(user_id=request.user)
            curr_record.delete()

        # follow
        except ObjectDoesNotExist:
            user_following = UserFollowing(user_id=request.user, following_user_id=target_user)
            user_following.save()

        return HttpResponseRedirect(reverse("get_user", kwargs={"user_id": user_id}))

    # if not logged in, redirect to login page
    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
def like_post(request, post_id):
    '''
    create entry in Like table
    '''
    if request.method == 'POST':
        try:
            post = Post.objects.get(id=post_id)
            like = Like.objects.get(post=post, user=request.user)
        except Like.DoesNotExist:
            # if does not exist, create new entry
            like = Like.objects.create(post=post, user=request.user)
            like.save()
            return HttpResponse(status=204)
    return HttpResponseRedirect(reverse('index'))




