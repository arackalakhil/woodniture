from django.urls import path
from . import views

urlpatterns = [
    path("login-register", views.signin, name="login-register"),
    path("loginuser", views.signin, name="signin"),
    path("user-register", views.signup, name="user-register"),
    path("logout", views.signout, name="logout"),
    path("number_login", views.numb_login,name="number_login"),
    path("otp login", views.otp,name="otp login"),
    path("add_address", views.add_address, name="add_address"),
    path("user_profile",views.user_profile,name="user_profile"),
]
