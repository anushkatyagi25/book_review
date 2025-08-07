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
    return render(request,"landing.html",context={'books':books,'page':"Home"})

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
        return redirect('/login')
    
    return render(request,'register.html',{'page':"Register"})


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

    return render(request,'login.html',{'page':'Login'})

@login_required
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

    return render(request,'add_book.html',context={'form':form,'page':'Books'})

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
    return render(request,'update_book.html', context={'form':form,'page':'Books'})

@login_required
def delete_book(request,book_id):
    book=Book.objects.get(id=book_id)
    book.delete()
    return redirect('/',{'page':'Books'})

@login_required
def add_review(request,book_id):
    print(Review.objects.filter(book=book_id))

    book=Book.objects.get(id=book_id)
    avg_rating=book.average_rating
    if request.method=='POST':
        rating=request.POST.get("ratings")
        comment=request.POST.get("comment")
        book=book
        user=request.user

        review=Review.objects.create(rating=rating,comment=comment,book=book,user=user)
        review.save()

    reviews=Review.objects.filter(book=book_id)
    return render(request,'review_page.html',context={'reviews':reviews,'page':'Reviews','avg':avg_rating})
    
@login_required
def update_review(request,review_id):
    review=Review.objects.get(id=review_id)
    book_id=review.book.id
    old_comment=review.comment
    if request.user==review.user:
        if request.method=='POST':
           review.rating=request.POST.get('ratings')
           review.comment=request.POST.get('comment')
           review.save()
           url=f'/add-review/{book_id}'
           return redirect(url)
        return render(request,'update_review.html',context={"old_comment":old_comment,'page':'Update Reviews'})

@login_required
def delete_review(request,review_id):
    review=Review.objects.get(id=review_id)
    book_id=review.book.id
    if request.user==review.user:
        review.delete()
    url=f'/add-review/{book_id}'
    return redirect(url)

@login_required
def display_reviews(request,book_id):
    reviews=Review.objects.get(Review.reviews.id==book_id)
    return render(request,"review_page.html",context={'reviews':reviews,'page':'Reviews'})