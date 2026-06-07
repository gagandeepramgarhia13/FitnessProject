from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path("food/diary", views.foodDiary, name="food"),
    path("food/add_food/<str:meal>", views.addFood, name="addFood"),
    path("food/get_food_info/<str:food_item>", views.get_food_info, name="foodInfo"),
    path("profile/edit_profile", views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name='change_password'),
    path("food/delete/<int:id>",views.deleteFood,name="deleteFood"),
    path("food/edit/<int:id>",views.editFood,name="editFood"),
    ]
                                                                     