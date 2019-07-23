from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import Http404, HttpResponse
# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.core.mail import send_mail

from grumblr.models import *
from grumblr.forms import *
from django.conf import settings
from mimetypes import guess_type


@login_required
def post_new(request):
    context = {}

    # no new posts, just view global stream
    if request.method == 'GET':
        context['username'] = request.user.username
        posts = Post.objects.all().order_by('-time')
        context['posts_with_commts'] = get_posts_with_commts(posts)
        return render(request, 'globalstream.html', context)

    form = PostForm(request.POST)
    context['form'] = form

    if form.is_valid():
        newPost = Post(text=request.POST['text'], user=request.user)
        newPost.save()

    context['username'] = request.user.username
    posts = Post.objects.all().order_by('-time')

    context['posts_with_commts'] = get_posts_with_commts(posts)

    return render(request, 'globalstream.html', context)


@login_required
def profile(request):
    context = {}

    # return if method is post
    if request.method == 'POST':
        return render(request, 'profile.html', context)

    if 'username' in request.GET and request.GET['username']:
        # get username in GET parameters
        username = request.GET['username']
    else:
        # if no username in GET, return his own profile
        username = request.user.username

    context['username'] = username
    # get user object
    p_user = get_object_or_404(User, username=username)

    # get profile object
    user_profile = UserProfile.objects.get(user=p_user)
    context['user_profile'] = user_profile

    # return user and posts for this profile
    context['user'] = request.user
    posts = Post.objects.filter(user=p_user).order_by('-time')
    context['posts_with_commts'] = get_posts_with_commts(posts)

    if UserProfile.objects.filter(user=request.user, followed=p_user):
        context['isfollow'] = True
    else:
        context['isfollow'] = False

    return render(request, 'profile.html', context)


@login_required
def edit_profile(request):
    context = {}
    print("here")
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    # return user and profile if request is GET
    if request.method == 'GET':
        context['user'] = user
        context['user_profile'] = user_profile
        return render(request, 'edit_profile.html', context)

    # validate profile form
    form = ProfileForm(request.POST, request.FILES, instance=user_profile)
    context['form'] = form
    if not form.is_valid():
        print("not valid")
        return render(request, 'edit_profile.html', context)

    # edit information in profile
    user_profile.age = form.cleaned_data['age']
    user_profile.last_name = form.cleaned_data['last_name']
    user_profile.first_name = form.cleaned_data['first_name']
    user_profile.bio = form.cleaned_data['bio']
    user_profile.photo = form.cleaned_data['photo']
    user_profile.save()

    # edit information in user
    user.last_name = form.cleaned_data['last_name']
    user.first_name = form.cleaned_data['first_name']
    user.save()

    context['user'] = user
    context['user_profile'] = user_profile
    return render(request, 'edit_profile.html', context)


@login_required
def get_photo(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)
    if not user_profile.photo:
        raise Http404
    content_type = guess_type(user_profile.photo.name)
    return HttpResponse(user_profile.photo, content_type=content_type)


@login_required
def follow(request, username):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    followed_user = get_object_or_404(User, username=username)
    user_profile.followed.add(followed_user)

    context['user'] = request.user
    context['user_profile'] = user_profile
    context['username'] = username
    p_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=p_user).order_by('-time')
    context['posts_with_commts'] = get_posts_with_commts(posts)
    context['isfollow'] = True
    return render(request, 'profile.html', context)


@login_required
def unfollow(request, username):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    followed_user = get_object_or_404(User, username=username)
    user_profile.followed.remove(followed_user)

    context['user'] = request.user
    context['user_profile'] = user_profile
    context['username'] = username
    p_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=p_user).order_by('-time')
    context['posts_with_commts'] = get_posts_with_commts(posts)
    context['isfollow'] = False
    return render(request, 'profile.html', context)


@login_required
def follow_stream(request):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    all_followed = user_profile.followed.all()
    posts = Post.objects.filter(user__in=all_followed).order_by('-time')
    context['username'] = request.user.username
    context['posts_with_commts'] = get_posts_with_commts(posts)
    return render(request, 'follow_stream.html', context)


@login_required
def reset_pwd(request, username, token):
    context = {}
    user = request.user

    # check token
    if not default_token_generator.check_token(user, token):
        raise Http404

    context['token'] = token
    context['user'] = user
    if request.method == 'GET':
        return render(request, 'reset_pwd.html', context)

    # validate reset password form
    form = ResetPwdForm(request.POST, instance=user)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'reset_pwd.html', context)

    # set new password in user object
    new_password = form.cleaned_data['password']
    user.set_password(new_password)
    user.save()

    # redirect to globalstream page if success
    login(request, user)
    return redirect('/')


@login_required
def send_email(request):
    context = {}
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    token = default_token_generator.make_token(user)
    context['user'] = user
    context['user_profile'] = user_profile

    email_body = """
        Please reset your password by clicking on the following link:
        http://%s%s
        """ % (request.get_host(), reverse('reset_pwd', args=(user.username, token)))

    send_mail(subject="Reset your password", message=email_body,
              from_email="luxingj@andrew.cmu.edu",
              recipient_list=[user.email])

    context['reset'] = True
    return render(request, 'edit_profile.html', context)


def register(request):
    context = {}

    # Just display the register form if this is GET request
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'registration.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'registration.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password'],
                                        last_name=form.cleaned_data['last_name'],
                                        first_name=form.cleaned_data['first_name'],
                                        email=form.cleaned_data['email'])
    new_user.is_active = False
    new_user.save()

    # send an email to confirm registration
    token = default_token_generator.make_token(new_user)
    email_body = """
        Please confirm your registration by clicking on the following link:
        http://%s%s
        """ % (request.get_host(), reverse('confirm_register', args=(new_user.username, token)))

    print(new_user.email)
    send_mail(subject="Please verify your email address",
              message=email_body,
              from_email="luxingj@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['sentemail'] = True
    return render(request, 'registration.html', context)


def confirm_register(request, username, token):
    user = get_object_or_404(User, username=username)
    # check token
    if not default_token_generator.check_token(user, token):
        raise Http404

    # create a new profile user
    new_profile = UserProfile.objects.create(user=user,
                                             last_name=user.last_name,
                                             first_name=user.first_name)
    new_profile.save()
    user.is_active = True
    user.save()

    login(request, user)
    return redirect('/')


@login_required
def comment(request, post_id):
    context = {}
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "GET":
        raise Http404
    form = CommentForm(request.POST)
    context['form'] = form
    if not form.is_valid():
        return render(request, 'comment.xml', context)
    text = form.cleaned_data['text']
    new_comment = Comment(user=request.user, post=post,
                          text=text)
    new_comment.save()
    context['comment'] = new_comment
    return render(request, 'comment.xml', context)


@login_required
def get_new_posts(request, post_id):
    context = {}
    post = get_object_or_404(Post, pk=post_id)
    context['posts'] = Post.objects.filter(time__gt=post.time)\
        .order_by('-time')
    return render(request, 'get_new_posts.xml', context)


def get_posts_with_commts(posts):
    list = []
    for post in posts:
        tuple = {}
        tuple['post'] = post
        comments = Comment.objects.filter(post=post)
        tuple['comments'] = comments
        list.append(tuple)
    return list
