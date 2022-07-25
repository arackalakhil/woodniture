
from django.urls import path
from .import views
urlpatterns = [
    path('',views.index_page, name="home"),
    path('chair_list',views.chair_list, name="chair_list"),
    path('bed_list',views.bed_list, name="bed_list"),
    path('single_product/<int:id>/',views.single_product,name="single_product")
]