#Belt_Reviewer Views
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import *
from ..login_registration.models import User
from django.contrib import messages

# Create your views here.
def index(request):
    if "user" not in request.session:
        return redirect('/')
    recentReviews = []
    counter = 3
    orderedReviews = Review.objects.all().order_by("created_at")
    for i in orderedReviews:
        recentReviews.append(i)
        counter -= 1
        if counter == 0:
            break
    context = {
        "user" : User.objects.get(id = request.session["user"]),
        "recentReviews" : recentReviews,
        "books" : Book.objects.all()
        }
    return render(request, 'belt_reviewer/index.html', context)

def CountStars(rating):
    i = []
    while rating > 0:
        i.append("i")
    return i

def UserProfile(request, userId):
    context = {
        "user" : User.objects.get(id=userId),
        "userReviews" : Review.objects.filter(user_id = userId)
        }
    return render(request, 'belt_reviewer/userprofile.html', context)

def AddBook(request):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "authors" : Author.objects.all()
        }
    return render(request, 'belt_reviewer/add_book.html', context)

def AddBookValidation(request):
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    response = Book.objects.add_book_validator(request.POST, userId)
    if len(response["errors"]) > 0:
        for val in response["errors"]:
            messages.error(request, val)
        return redirect('/belt_reviewer/books/add')
    else:
        bookId = response["bookId"]
        return redirect('/belt_reviewer/books/{}'.format(bookId))

def AddReviewValidation(request, bookId):
    if "user" not in request.session:
        return redirect('/')
    userId = request.session["user"]
    response = Book.objects.add_review_validator(request.POST, userId, bookId)
    if len(response["errors"]) > 0:
        for val in response["errors"]:
            messages.error(request, val)
        return redirect('/belt_reviewer/books/{}'.format(bookId))
    else:
        return redirect('/belt_reviewer/books/{}'.format(bookId))
 
def BookBio(request, bookId):
    if "user" not in request.session:
        return redirect('/')
    context = {
        "book" : Book.objects.get(id = bookId),
        "author" : Author.objects.get(books = bookId),
        "reviews" : Review.objects.filter(book = bookId),
        "curUser" : User.objects.get(id = request.session["user"]).id
        }
    return render(request, 'belt_reviewer/book_bio.html', context)

def DeleteReview(request, reviewId):
    if "user" not in request.session:
        return redirect('/')
    userId = Review.objects.get(id = reviewId).user_id
    if userId != int(request.session["user"]):
        return redirect('/')
    else:
        bookId = Review.objects.get(id = reviewId).book.id
        Review.objects.get(id = reviewId).delete()
    return redirect('/belt_reviewer/books/{}'.format(bookId))

def LogOut(request):
    request.session.clear()
    return redirect('/')