from django.urls import path
from . import views
from django.db import models

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('rooms/', views.RoomListView.as_view(), name='rooms'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('rooms/<int:pk>', views.RoomDetailView.as_view(), name='room-detail'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),	
    path('book/<uuid:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('book/<uuid:pk>/borrowfaculty/', views.borrow_book_faculty, name='borrow_book_faculty'),
    path('rooms/<uuid:pk>/borrow/', views.borrow_room, name='borrow_room'),
]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
]