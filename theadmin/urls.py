from django.urls import path
from .import views
urlpatterns = [
    path('',views.signin_admins),
    path('admin_index',views.home_admin),
    path('admin_logout',views.signout_admin),
    path('listproducts',views.list_products),
    path('data_table',views.data_admin),
    path('cat_products',views.cat_products),
    path('block_user/<int:id>/',views.block_user),
    # path('unblock_user/<int:id>/',views.update_user),
    path('delete_products/<int:id>/',views.delete_products),
    path('update_products/<int:id>/',views.update_products),
    path('add_products',views.add_products),
    path('add_categories',views.add_category),
    path('delete_categories/<int:id>/',views.delete_category),
    path('update_categories/<int:id>/',views.update_category),

]
