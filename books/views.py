from django.shortcuts import render,redirect
from django.db.models import *
from books.models import *


# Create your views here.
def display_books(request):
    books=Book.objects.all()
    return render(request,"landing.html",context={'books':books})

def register_user(request):
    if request.method=="POST":
        firstname=request.POST.get("firstname")
        lastname=request.POST.get("lastname")
        email=request.POST.get("mail")
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=CustomUser.objects.create(first_name=firstname,
                                       last_name=lastname,
                                       email=email,
                                       username=username)
        user.set_password(password)

def add_book(request):
    if request.user.type!='ADMIN':
        return redirect('')
    