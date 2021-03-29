from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("register/<str:option>", views.registerOption, name="registerOption"),
    path("profile/", views.profile, name="profile"),
    path("requests/", views.requests, name="requests")
]