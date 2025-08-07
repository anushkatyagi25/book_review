"""
URL configuration for book_review project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from books.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',display_books, name="landing"),
    path('register/',register_user,name="register"),
    path('login/',login_user,name="login"),
    path('logout/',logout_user,name="logout"),
    path('add-book/',add_book,name="add-book"),
    path('update-book/<int:book_id>/',update_book,name="update-book"),
    path('delete-book/<int:book_id>/',delete_book,name="delete-book"),
    path('add-review/<int:book_id>/',add_review,name="add-review"),
    path('update-review/<int:review_id>/',update_review,name="update-review"),
    path('delete-review/<int:review_id>/',delete_review,name="delete-review"),
]
