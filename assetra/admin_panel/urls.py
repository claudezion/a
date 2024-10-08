from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("landing", views.landing, name="landing"),
    path("users", views.users, name="users"),
    path("referrals", views.referrals, name="referrals"),
    path("set", views.set, name="set"),
    path("user_overview", views.user_overview, name="user_overview"),
    path("search_users", views.search_users, name="search_users"),
    path("referral_overview", views.referral_overview, name="referral_overview"),
    path(
        "referral_leaderboard", views.referral_leaderboard, name="referral_leaderboard"
    ),
    path("user_referrals", views.user_referrals, name="user_referrals"),
    path("write", views.write, name="write"),
    path("blog_list", views.blog_list, name="blog_list"),
    path("edit_blog_list", views.edit_blog_list, name="edit_blog_list"),
    path("blog_overview", views.blog_overview, name="blog_overview"),
    path("write_blog", views.write_blog, name="write_blog"),
    path("edit_blog/<int:id>", views.edit_blog, name="edit_blog"),
    path("search_blogs", views.search_blogs, name="search_blogs"),
    path("edit_search_blogs", views.edit_search_blogs, name="edit_search_blogs"),
    path("user/<int:id>", views.user, name="user"),
    path("blog/<int:id>", views.blog, name="blog"),
]
