#Belt_reviewer Models
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_registration.models import User

# Create your models here.
class AuthorBookReviewManager(models.Manager):
    def add_book_validator(self, postData, userId):
        response = {
            'errors' : []
            }
        userPosting = User.objects.get(id = userId)
        try:
            title = Book.objects.get(title = postData["title"])
        except:
            title = None
        if title:
            response["errors"].append("Title is already in database!")
        try:
            authorOld = Author.objects.get(name = postData["addAuthor"])
        except:
            authorOld = None
        if authorOld:
            response["errors"].append("Author is already in database!")
        if len(postData["title"]) == 0 or len(postData["review"]) == 0:
            response["errors"].append("All fields must be entered!")
        if len(postData["title"]):
             if postData["title"][0] == " " or postData["title"][len(postData['title']) -1] == " ":
                response["errors"].append("Non-valid title name (watch for spaces at beginning and end!)")
        if len(postData["author"]) == 0 and len(postData["addAuthor"]) == 0:
            response["errors"].append("Author must be chosen!")
        if len(postData["addAuthor"]):
            if postData["addAuthor"][0] == " " or postData["addAuthor"][len(postData['addAuthor']) -1] == " ":
                response["errors"].append("Non-valid author name (watch for spaces at beginning and end!)")
        if len(response["errors"]) == 0:
            #Checks if a new author is being added or if a pre-existing author is being used
            try:
                authorNew = Author.objects.get(name = postData["addAuthor"])
            except:
                authorNew = None
            if not authorNew and len(postData["addAuthor"]) > 0:
                createdAuthor = Author.objects.create(name = postData["addAuthor"])
                bookCreated = Book.objects.create(title = postData["title"],
                                    author = createdAuthor)
                Review.objects.create(review = postData["review"],
                                        rating = int(postData["rating"]),
                                        user = userPosting,
                                        book = bookCreated)
                response["bookId"] = bookCreated.id
            else:
                authorOld = Author.objects.get(name = postData["author"])
                bookCreated = Book.objects.create(title = postData["title"],
                                    author = authorOld)
                Review.objects.create(review = postData["review"],
                                        rating = int(postData["rating"]),
                                        user = userPosting,
                                        book = bookCreated)
                curUser = User.objects.get(id=userId)
                curUser.review_count = len(Review.objects.filter(user_id = userId))
                curUser.save()
                response["bookId"] = bookCreated.id
        return response
    
    def add_review_validator(self, postData, userId, bookId):
        response = {
            'errors' : []
            }
        userPosting = User.objects.get(id = userId)
        bookReceiving = Book.objects.get(id = bookId)
        if len(postData["review"]) == 0:
          response["errors"].append("Review field must be entered!")
        if len(response["errors"]) == 0:
            Review.objects.create(review = postData["review"],
                                        rating = int(postData["rating"]),
                                        user = userPosting,
                                        book = bookReceiving)
            curUser = User.objects.get(id=userId)
            curUser.review_count = len(Review.objects.filter(user_id = userId))
            curUser.save()
        return response
        
class Author(models.Model):
    name = models.CharField(max_length=255)
    objects = AuthorBookReviewManager()


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books")
    objects = AuthorBookReviewManager()

class Review(models.Model):
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    objects = AuthorBookReviewManager()
