from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from werkzeug.security import check_password_hash
from django.utils.dateparse import parse_date, parse_datetime
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count
from django.db.models import Q
from django.contrib import messages

from .models import User, Referral, Blog, Category, Tag


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Attempt to authenticate using Django's authentication system
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)  # Login successful
            return redirect("admin_panel/landing.html")
        
        if user is not None and not user.is_staff:
            return render(request, "admin_panel/forbidden.html")

        # If Django's auth failed, check for Werkzeug hash
        try:
            user = User.objects.get(username=username)
            if check_password_hash(user.password, password):  # Legacy hash match
                # Rehash the password to Django's system
                user.set_password(password)
                user.save()

                # Authenticate the user using the newly hashed password
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)  # Log in the user
                    return redirect("/")
        except User.DoesNotExist:
            # Handle case where user does not exist
            return render(
                request,
                "admin_panel/login.html",
                {"message": "Invalid username or password"},
            )

        return render(
            request,
            "admin_panel/login.html",
            {"message": "Invalid username or password"},
        )

    return render(request, "admin_panel/login.html")


def index(request):
    return render(request, "admin_panel/index.html")

def landing(request):
    return render(request, "admin_panel/landing.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def users(request):
    user_list = User.objects.all().values(
        "id",
        "username",
        "email",
        "verified",
        "date_joined",
        "first_name",
        "last_name",
        "dob",
        "mobile",
        "country",
        "profile",
    )

    paginator = Paginator(user_list, 10)  # Show 10 users per page

    page_number = request.GET.get("page")  # Get the current page number from the URL
    users = paginator.get_page(page_number)  # Get the users for the current page

    return render(request, "admin_panel/users.html", {"users": users, "order": "↑"})


def referrals(request):

    user = {
        "id": 1,
        "username": "user1",
        "first_name": "jon",
        "last_name": "deo",
        "email": "example@mail.com",
        "verified": 1,
        "date_joined": "2024-06-09",
        "dob": "2024-06-09",
        "country": "us",
        "profile": "",
        "mobile": "19th May 2000",
    }

    return render(request, "admin_panel/referrals.html", {"user": user, "order": "↓"})


def set(request):
    users = []

    for user in users:
        username = user["username"]
        email = user["email"]
        first_name = user["first_name"]
        last_name = user["last_name"]
        country = user["country"]
        created_date = user["created_date"]
        dob = parse_date(user["dob"])
        mobile = user["mobile_number"]
        profile_picture = user["profile_picture"]
        is_verified = bool(user["is_verified"])
        werkzeug_hashed_password = user["password"]

        date_joined = parse_datetime(created_date)

        # Using the create method
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            country=country,
            date_joined=date_joined,
            dob=dob,
            mobile=mobile,
            verified=is_verified,
            profile=profile_picture,
            password=werkzeug_hashed_password,  # Store the hashed password directly
        )

        user.save()

        print(f"User {username} created successfully.")

    return render(request, "admin_panel/index.html")


def user_overview(request):
    users = User.objects.all()
    verified_users = users.filter(verified=True).count()
    unverified_users = users.filter(verified=False).count()

    context = {
        "users": users,
        "verified_users": verified_users,
        "unverified_users": unverified_users,
    }

    return render(request, "admin_panel/user_overview.html", context)


@csrf_exempt
def user_api(request, id):

    # Query for requested user
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Return user contents
    if request.method == "GET":
        return JsonResponse(user.serialize())


def referral_overview(request):
    total_referrals = Referral.objects.all()
    successful_referrals = Referral.objects.filter(success=True).count()
    unsuccessful_referrals = Referral.objects.filter(success=False).count()

    context = {
        "total_referrals": total_referrals,
        "successful_referrals": successful_referrals,
        "unsuccessful_referrals": unsuccessful_referrals,
    }

    return render(request, "admin_panel/referral_overview.html", context)


def referral_leaderboard(request):
    leaderboard = User.objects.annotate(referrals_count=Count("referrals")).order_by(
        "-referrals_count"
    )[:10]
    context = {
        "leaderboard": leaderboard,
    }

    return render(request, "admin_panel/referral_leaderboard.html", context)


def user_referrals(request):
    # Initialize variables for the template context
    referrals_by_user = None
    search_user = None
    error_message = None

    # Check if the form was submitted with a GET request
    if "search_term" in request.GET:
        search_term = request.GET.get("search_term")

        try:
            # Find the user with the given username or email
            search_user = User.objects.get(
                Q(username=search_term) | Q(email=search_term)
            )

            # Get all referrals made by this user
            referrals_by_user = Referral.objects.filter(referred_by=search_user)

        except User.DoesNotExist:
            error_message = f"No user found with username or email '{search_term}'."

    if referrals_by_user == None:
        error_message = f"No referrals found with username or email '{search_term}'."

    context = {
        "search_user": search_user,
        "referrals_by_user": referrals_by_user,
        "error_message": error_message,
    }

    return render(request, "admin_panel/user_referrals.html", context)


def search_users(request):
    search_user = None
    error_message = None

    if "search_term" in request.GET:
        search_term = request.GET.get("search_term").strip()

        if search_term:
            try:
                search_user = User.objects.filter(
                    Q(username__icontains=search_term) | Q(email__icontains=search_term)
                )

                if not search_user:
                    error_message = f"No user found with username or email containing '{search_term}'."

            except User.DoesNotExist:
                error_message = f"No user found with username or email '{search_term}'."
        else:
            error_message = "Please enter a valid search term."

    context = {
        "search_term": search_term,
        "users": search_user,
        "error_message": error_message,
    }

    return render(request, "admin_panel/search_user.html", context)


def write(request):
    return render(request, "admin_panel/write.html")


def write_blog(request):
    if request.method == "POST":

        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")
        author = request.user
        publish = request.POST.get("publish") == "on"
        image = request.FILES.get("image")
        
        category = Category.objects.get(pk=category_id) if category_id else None
        
        tag_ids = request.POST.getlist("tags") 
        tags = Tag.objects.filter(id__in=tag_ids) 

        # Create the blog post
        blog = Blog.objects.create(
            title=title,
            content=content,
            category=category,
            cover_image=image,
            author=author,
            is_published=publish
        )

        # Set the many-to-many field (tags)
        blog.tags.set(tags)
        blog.save()

        blogs = Blog.objects.all()
        published_blog = blogs.filter(is_published=True).count()
        unpublished_blog = blogs.filter(is_published=False).count()

        context = {
            "blogs": blogs,
            "published_blog": published_blog,
            "unpublished_blog": unpublished_blog,
        }

        return render(request, "admin_panel/blog_overview.html", context)
    else:
        categories = Category.objects.all()
        tags = Tag.objects.all()

        context = {
            "categories": categories,
            "tags": tags,
            "authors": [
                "claude",
                "jeeordahnoh",
                "bobjohn2129",
                "yashj99",
                "ashmeetsingh98",
                "",
                "",
                "",
            ],
        }
        return render(request, "admin_panel/write_blog.html", context)


def edit_blog(request, id):
    # Retrieve the blog post by its ID
    blog = get_object_or_404(Blog, id=id)
    
    # Handle form submission
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        category_id = request.POST.get("category")
        tags_ids = request.POST.getlist("tags")  # Get list of selected tag IDs
        publish = request.POST.get("publish") == "on"
        image = request.FILES.get("image")

        # Update blog attributes
        blog.title = title
        blog.content = content
        blog.is_published = publish
        
        if category_id:
            blog.category_id = category_id  
        
        
        if tags_ids:
            blog.tags.set(tags_ids)  
        else:
            blog.tags.clear()  

        
        if image:
            blog.cover_image = image

       
        blog.save()
        
        messages.success(request, "Blog post updated successfully!")
        blog = get_object_or_404(Blog, pk=id)

        context = {
            "blog": blog,
        }

        return render(request, "admin_panel/blog.html", context) 

    
    categories = Category.objects.all()  
    tags = Tag.objects.all()  
    context = {
        'blog': blog,
        'categories': categories,
        'tags': tags,
    }
    
    return render(request, 'admin_panel/edit_blog.html', context)


def blog_overview(request):
    blogs = Blog.objects.all()
    published_blog = blogs.filter(is_published=True).count()
    unpublished_blog = blogs.filter(is_published=False).count()

    context = {
        "blogs": blogs,
        "published_blog": published_blog,
        "unpublished_blog": unpublished_blog,
    }

    return render(request, "admin_panel/blog_overview.html", context)


def blog_list(request):
    blog_list = Blog.objects.all()

    paginator = Paginator(blog_list, 10)  # Show 10 users per page

    page_number = request.GET.get("page")  # Get the current page number from the URL
    blogs = paginator.get_page(page_number)

    context = {"blogs": blogs}

    return render(request, "admin_panel/blog_list.html", context)

def edit_blog_list(request):
    blog_list = Blog.objects.all()

    paginator = Paginator(blog_list, 10)  # Show 10 users per page

    page_number = request.GET.get("page")  # Get the current page number from the URL
    blogs = paginator.get_page(page_number)

    context = {"blogs": blogs}

    return render(request, "admin_panel/edit_blog_list.html", context)

def search_blogs(request):
    blogs = None
    search_user = None
    error_message = None

    if "search_term" in request.GET:
        search_term = request.GET.get("search_term")

        try:
            search_user = User.objects.get(
                Q(username=search_term) | Q(email=search_term)
            )

            blogs = Blog.objects.filter(author=search_user)

        except User.DoesNotExist:
            error_message = f"No user found with username or email '{search_term}'."

    context = {
        "search_user": search_user,
        "blogs": blogs,
        "error_message": error_message,
    }

    return render(request, "admin_panel/search_blogs.html", context)


def blog(request, id):
    blog = get_object_or_404(Blog, pk=id)

    context = {
        "blog": blog,
    }

    return render(request, "admin_panel/blog.html", context)


def user(request, id):
    user = get_object_or_404(User, pk=id)

    context = {
        "user": user,
    }

    return render(request, "admin_panel/user.html", context)


def edit_search_blogs(request):
    blogs = None
    search_user = None
    error_message = None

    if "search_term" in request.GET:
        search_term = request.GET.get("search_term")

        try:
            search_user = User.objects.get(
                Q(username=search_term) | Q(email=search_term)
            )

            blogs = Blog.objects.filter(author=search_user)

        except User.DoesNotExist:
            error_message = f"No user found with username or email '{search_term}'."

    context = {
        "search_user": search_user,
        "blogs": blogs,
        "error_message": error_message,
    }

    return render(request, "admin_panel/edit_search_blogs.html", context)