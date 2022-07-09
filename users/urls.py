from django.urls import path
from .import views
urlpatterns = [
 
    path('login-register',views.signin,name= 'login-register'),
    path('loginuser',views.signin,name='signin'),
    path('register',views.signup),
    path('logout',views.signout, name="logout"),
    path('number_login',views.numb_login),
    path('otp login',views.otp),
]