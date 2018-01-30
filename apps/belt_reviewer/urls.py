#Belt Reviewer URLs
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'add/review/validation/(?P<bookId>\d+)', views.AddReviewValidation),
    url(r'delete/(?P<reviewId>\d+)$', views.DeleteReview),
    url(r'books/(?P<bookId>\d+)$', views.BookBio),
    url(r'books/add/validation', views.AddBookValidation),
    url(r'books/add$', views.AddBook),
    url(r'user/(?P<userId>\d+)', views.UserProfile),
    url(r'logOut', views.LogOut),
    url(r'^', views.index),
]