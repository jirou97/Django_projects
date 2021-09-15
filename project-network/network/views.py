import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from .models import *
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return posts(request)
    #return render(request, "network/index.html")

@login_required
def user(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user)
    comments = Comment.objects.filter(user=user)
    follows = Follow.objects.filter(user=user)
    likes = Likes.objects.filter(user=user)
    return render(request, 'network/profile.html', {
        'profile_user': user,
        'posts':posts,
        'comments': comments,
        'follows': follows,
        'likes': likes
        })
    #return render(request, "network/index.html")
@login_required
def follow(request):
    if request.method == "POST":
        user = User.objects.get(pk = int(request.POST['user_id']))
        follow = Follow.objects.create(user=request.user, follower = user)
        follow.save()
        return render(request, 'network/following.html', {
            'followings': [x.follower for x in Follow.objects.filter(user=request.user)],
            'followers':  [x.user for x in Follow.objects.filter(follower=request.user)]
            }) 
    elif request.method == "GET":
        return render(request, 'network/following.html', {
            'followings': [x.follower for x in Follow.objects.filter(user=request.user)],
            'followers':  [x.user for x in Follow.objects.filter(follower=request.user)]
            }) 

@login_required
def unfollow(request):
    if request.method == "POST":
        user = User.objects.get(pk = int(request.POST['user_id']))
        follow = Follow.objects.get(user=request.user, follower = user)
        follow.delete()
        return render(request, 'network/following.html', {
            'followings': [x.follower for x in Follow.objects.filter(user=request.user)],
            'followers':  [x.user for x in Follow.objects.filter(follower=request.user)]
            })
@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk = int(post_id))
    if request.user != post.user :
        #Someone else is trying to delete your post
        return index(request)
    else :
        post.delete()
        return index(request)

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(pk = int(post_id))
    if request.method == "GET":
        return render(request, 'network/edit_post.html', {
            'post':post,
            })
    else :
        if request.user != post.user :
            #Someone else is trying to delete your post
            return index(request)
        else :
            post.body = request.POST['post_body']
            post.save()
            return index(request)

@csrf_exempt
@login_required
def compose_post(request):
    # Composing a new post must be via POST request
    if request.method not in ["POST","DELETE"]:
        return JsonResponse({"error": "POST request required."}, status=400)


    # Get data from request.body
    data = json.loads(request.body)
    types = data.get("types", "")

    if request.method == "DELETE":
        post_id = int(data.get("post", ""))
        post = Post.objects.get(id=post_id)
        user = request.user
        try :
            like = Likes.objects.get(user=user, post=post)
            like.delete()
            return JsonResponse({"message": "Unlike was made successfully."}, status=201)
        except Likes.DoesNotExist:
            return JsonResponse({"message": "Like doesn't exist to delete it."}, status=400)
    elif types == "post":
        # Get contents of post
        body = data.get("body", "")
        user = request.user

        # Create the post
        post = Post(user=user, body=body)
        post.save()
        user.posts.add(post)
        request.method = "GET"
        index(request)
        return JsonResponse({"message": "Post was made successfully.","id": post.id}, status=201)
    elif types == "like":
        post_id = int(data.get("post", ""))
        post = Post.objects.get(id=post_id)
        try :
            like = Likes.objects.get(user=request.user, post=post)
            return JsonResponse({"message": f"A like already exists for this post {post_id}"}, status=400)
        except Likes.DoesNotExist :
            like = Likes(user=request.user, post=post)
            like.save()
            user = request.user
            user.likes.add(like)
            post.has_likes.add(like)
            return JsonResponse({"message": "Like was made successfully."}, status=201)
    else:
        return JsonResponse({"message": "Wrong type"}, status=400)


#@csrf_exempt
@login_required
def posts(request):
    #if request.method == "GET":
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp_created").all()
    posts = [post.serialize() for post in posts]
    paginator = Paginator(posts, 10)  # Show 10 posts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/index.html', {'page_obj': page_obj})

#@csrf_exempt
@login_required
def put_somestuff(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("body") is not None:
            post.body = data["body"]
            post.save()
        return HttpResponse(status=204)
    if request.method == "GET":
         return render(request, "network/post.html", {
             "post": post,
             "comments": Comment.objects.filter(post=post)
         })

#@csrf_exempt
@login_required
def comment(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=int(post_id))
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        
        comment = request.POST["comment"]
        new_comment = Comment(user=request.user, post=post, comment=comment)
        new_comment.save()
        return render(request, "network/post.html", {
             "post": post,
             "comments": Comment.objects.filter(post=post)
         })
    elif request.method == "DELETE":
        comment = Comment.objects.get(pk = int(post_id))
        post = comment.post
        if request.user == comment.user :
            comment.delete()
        return render(request, "network/post.html", {
             "post": post,
             "comments": Comment.objects.filter(post=post)
         })
@login_required
def delete_comment(request,comment_id):
    if request.method == "POST":
        comment = Comment.objects.get(pk = int(comment_id))
        post = comment.post
        if request.user == comment.user :
            comment.delete()
        return render(request, "network/post.html", {
            "post": post,
            "comments": Comment.objects.filter(post=post)
        })
#@csrf_exempt
@login_required
def email(request, email_id):

    # Query for requested email
    try:
        email = Email.objects.get(user=request.user, pk=email_id)
    except Email.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    # Return email contents
    if request.method == "GET":
        return JsonResponse(email.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("read") is not None:
            email.read = data["read"]
        if data.get("archived") is not None:
            email.archived = data["archived"]
        email.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

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

@login_required
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
