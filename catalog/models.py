from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User, Group
import uuid # Required for unique book instances
from datetime import date
from catalog.choices import *
from django.contrib.auth.models import AbstractUser
import datetime

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Room(models.Model):
    
    name = models.CharField(max_length=200);

    description = models.CharField(max_length=200);
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('room-detail', args=[str(self.id)])
    
class RoomInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    room = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
    room_code = models.CharField(max_length=10)
    LOAN_STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    due_back = models.DateField(null=True, blank=True)
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )
    
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set room as returned"),) 

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.room.name})'
    
    
class Book(models.Model):
    
    title = models.CharField(max_length=200)


    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
 
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    
    LOCATION_DEWEY = (
        ('000-099', 'Generalities'),
        ('100-199', 'Philosophy'),
        ('200-299', 'Religion'),
        ('300-399', 'Social Science'),
        ('400-499', 'Language'),
        ('500-599', 'Science & Math'),
        ('600-699', 'Technology'),
        ('700-799', 'The Arts'),
        ('800-899', 'Literature'),
        ('900-999', 'Geography & History'),
    )
    
    location = models.CharField(
        max_length = 7,
        choices = LOCATION_DEWEY,
        blank=True,
        help_text='Book Location'
    )
    
    tags = models.CharField(max_length=10,help_text='Tags',default='Tag')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.title
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
             return True
        return False

    LOAN_STATUS = (
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),) 

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.book.title})'
    

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']
    
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    """Model representing a Language (e.g. English, French, Japanese, etc.)"""
    name = models.CharField(max_length=200,
                            help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")

    def __str__(self):
        """String for representing the Model object (in Admin site etc.)"""
        return self.first_name

class Profile(models.Model):
    
    User.first_name = models.OneToOneField(User, on_delete=models.CASCADE)
    User.last_name = models.OneToOneField(User, on_delete=models.CASCADE)
    User.username = models.OneToOneField(User, on_delete=models.CASCADE)
    User.email = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    secretAnswer = models.CharField(max_length=100)   
    