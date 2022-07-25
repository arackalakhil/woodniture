from django.urls import path
from . import views

urlpatterns = [
    path("", views.signin_admins),
    path("admin_index", views.home_admin ,name ="admin_index"),
    path("admin_logout", views.signout_admin,name="admin_logout"),
    path("listproducts", views.list_products,name="listproducts"),
    path("data_table", views.user_data_table,name="data_table"),
    path("cat_products", views.category_products,name="cat_products"),
    path("block_user/<int:id>/", views.block_user,name="block_user"),
    # path('unblock_user/<int:id>/',views.update_user),
    path("delete_products/<int:id>/", views.delete_products,name="delete_products"),
    path("update_products/<int:id>/", views.update_products,name="update_products"),
    path("add_products", views.add_products,name="add_products"),
    path("add_categories", views.add_category,name="add_categories"),
    path("delete_categories/<int:id>/", views.delete_category,name="delete_categories"),
    path("update_categories/<int:id>/", views.update_category  ,name="update_categories"),
    path("order_management",views.order_management,name="order_management"),
    path("change_status/<int:id>/",views.change_status,name="change_status"),
]
