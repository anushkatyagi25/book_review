from django.shortcuts import render,redirect
from django.db.models import *
from books.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .forms import *
from django.contrib.auth.decorators import login_required

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

        user=CustomUser.objects.filter(username=username)
        if user.exists():
            messages.error(request,'User already exists')
            return redirect('/register/')

        user=CustomUser.objects.create(first_name=firstname,
                                       last_name=lastname,
                                       email=email,
                                       username=username)
        user.set_password(password)
        user.save()
        return redirect('/register')
    
    return render(request,'register.html')


def login_user(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not CustomUser.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login')

        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'Invalid password')
        else:
            login(request,user)
            return redirect('/')

    return render(request,'login.html')

def logout_user(request):
    logout(request)
    return redirect('/login')  

@login_required
def add_book(request):

    if request.user.type!='ADMIN':
        return redirect('/')
    if request.method=='POST':
        form=BookForm(request.POST)
        if form.is_valid():
            book=form.save(commit=False)
            book.author=request.user
            book.save()
            return redirect('/')
    else:
        form=BookForm()

    return render (request,'add_book.html',context={'form':form})

@login_required
def update_book(request,book_id):
    book=Book.objects.get(id=book_id)
    if request.user.type!='ADMIN':
        return redirect('/')
    if request.method=='POST':
        form=BookForm(request.POST)
        if form.is_valid():
            book=form.save(commit=False)
            book.author=request.user
            book.save()
            return redirect('/')
    else:
        form=BookForm(instance=book)
    return render(request,'update_book.html', context={'form':form})

@login_required
def delete_book(request,book_id):
    book=Book.objects.get(id=book_id)
    book.delete()
    return redirect('/')
    