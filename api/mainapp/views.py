from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Post, Comment, UserPreference
from .forms import PostForm, SignupForm, ProfileUpdateForm, ProfilePicForm, CommentForm, UserPreferenceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

def loginintro(request):
    return render(request, 'loginintro.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request, ("You have been Logged In"))
            return redirect('home')
        else:
            messages.success(request, ("Invalid username or password"))
            return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, ("You have been Logged Out"))
    return redirect('loginintro')

def register_user(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            # Log in User
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ('You have successfullt register. Welcome to Lovetamin'))
            return redirect('home')
        

    return render(request, 'register.html', {'form':form})

def home(request):
    if request.user.is_authenticated:

        form = PostForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("Posted successfully..."))
                return redirect('home')
            
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts":posts, "form":form})
    
    elif request.user.is_authenticated:
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts":posts})
    
    else:
        return render(request, 'loginintro.html')
    
# New post start
def newpost(request):
    if request.user.is_authenticated:

        form = PostForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                messages.success(request, ("Posted successfully..."))
                return redirect('home')
            
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'newpost.html', {"posts":posts, "form":form})
    
    elif request.user.is_authenticated:
        posts = Post.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"posts":posts})
    
    else:
        return render(request, 'loginintro.html')
# New post end

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        posts = Post.objects.filter(user_id=pk).order_by("-created_at")

        # post form logic
        if request.method == 'POST':
            # get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            # deside to follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)

            # Save to update form info
            current_user_profile.save()

        return render(request, 'profile.html', {"profile":profile, "posts": posts})
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def update_profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        current_profile = Profile.objects.get(user_id=request.user.id)

        user_form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=current_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            login(request, current_user)
            messages.success(request, ("Profile Updated Successfully..."))
            return redirect('profile', pk=request.user.id)

        return render(request, 'update_profile.html', {'user_form':user_form, 'profile_form':profile_form})
    
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def post_like(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post.likes.filter(id=request.user.id):
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def post_love(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)  
        if post.loves.filter(id=request.user.id):
            post.loves.remove(request.user)
        else:
            post.loves.add(request.user)
        
        return redirect(request.META.get("HTTP_REFERER"))
        
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def post_share(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if post:
            return render(request, "post_share.html", {'post': post})
        else:
            messages.success(request, ("that post not Exist..."))
            return redirect('home')
        
def unfollow(request, pk):
    if request.user.is_authenticated:
        # get the profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow the user from logged in user profile
        request.user.profile.follows.remove(profile)
        # Update logged in user profile
        request.user.profile.save()
        # Return message
        messages.success(request, (f"You have unfollowed this user {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
      
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        # get the profile to follow
        profile = Profile.objects.get(user_id=pk)
        # follow the user from logged in user profile
        # Check already logged ins user followed or not
        if profile not in request.user.profile.follows.all():
            request.user.profile.follows.add(profile)
            # Update logged in user profile
            request.user.profile.save()
            # Return message
            messages.success(request, (f"You have followed this user {profile.user.username}"))
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            messages.success(request, (f"You have already followed this user {profile.user.username}"))
            return redirect(request.META.get("HTTP_REFERER"))
    
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {'profiles':profiles })
        else:
            messages.success(request, ("This is not your profile"))
            return redirect('home')
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {'profiles':profiles })
        else:
            messages.success(request, ("This is not your profile"))
            return redirect('home')
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    

def delete_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user == post.user:
            post.delete()
            messages.success(request, ("Post Deleted"))
            #return redirect(request.META.get("HTTP_REFERER"))
            return render(request, 'profile.html', {"profile":profile})
        
        else:
            messages.success(request, ("You can't delete this post"))
            return redirect('home')
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def edit_post(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)
        if request.user == post.user:
            form = PostForm(request.POST or None, instance=post)
            if request.method == 'POST':
                if form.is_valid():
                    post = form.save(commit=False)
                    post.user = request.user
                    form.save()
                    messages.success(request, ("Post Updated"))
                    return redirect('profile', pk=post.user.id)
                    #return render(request, "edit_post.html", {'form':form ,'post': post})
                else:
                    messages.success(request, ("Post Not Updated"))
                    return redirect('profile', pk=post.user.id)
            else:
                return render(request, "edit_post.html", {'form':form ,'post': post})
        else:
            messages.success(request, ("You can't edit this post"))
            return redirect('home')
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def search_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            search = request.POST['search']
            posts = Post.objects.filter(body__contains=search)
            return render(request, 'search_post.html', {'search':search, 'posts':posts})
        else:
            return render(request, 'search_post.html')
    else:
        messages.success(request, ("You must Logged In."))
        return render(request, "search_post.html", {})
    
def search_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            search_user = request.POST['search_user']
            users = User.objects.filter(username__contains=search_user)
            return render(request, 'search_user.html', {'search_user':search_user, 'users': users})
        else:
            return render(request, 'search_user.html')
    else:
        messages.success(request, ("You must Logged In."))
        return render(request, "search_user.html", {})
    

def post_comments(request, pk):
    if request.user.is_authenticated:
        # Get the particular post and it's comments accordingly
        post = get_object_or_404(Post, id=pk)
        # form for submit comments 
        commentForm = CommentForm()
        if post:
            post_comments = Comment.objects.all()
            return render(request, "post_comments.html", {'post': post, 'post_comments':post_comments, 'commentForm':commentForm})
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')
    
def comment_sent(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=pk)

        if request.method == 'POST':
            commentSent = CommentForm(request.POST or None, request.FILES or None)
            
            if commentSent.is_valid():
                comment = commentSent.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                messages.success(request, ("Comments sent successfully"))
                return redirect('post_comments', pk=post.id)
            else:
                messages.success(request,("Comments not sent"))
                return redirect('post_comments', pk=post.id)
        
        return redirect('post_comments', pk=post.id)
    else:
        messages.success(request, ("You must Logged In."))
        return redirect('post_comments')
        

def update_preferance(request):
    if request.user.is_authenticated:

        if request.method == 'POST':
            user = request.POST.get(request.user)
            preference = request.POST.get('preference')

            create_preference = UserPreference.objects.create(user=user, preference=preference)
            create_preference.save()
            messages.success(request, ("Preferance updated successfully"))
            return redirect('update_preferance',  pk=request.user.id)
            
        return render(request, 'update_preferance.html', {})

    else:
        messages.success(request, ("You must Logged In."))
        return redirect('home')