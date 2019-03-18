from django.shortcuts import render
from django.db import models
from catalog.models import Book, Author, BookInstance, Genre , Room , RoomInstance
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from catalog.forms import RegistrationForm
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
import datetime
# Create your views here.

def index(request):
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    
class RoomListView(generic.ListView):
    model = Room
    paginate_by = 5
    
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5

class AuthorDetailView(generic.DetailView):
    model = Author
    
class BookDetailView(generic.DetailView):
    model = Book
    
class RoomDetailView(generic.DetailView):
    model = Room
    
class BorrowBookView(generic.DetailView):
    model = BookInstance

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='r').order_by('due_back')

def register_view(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/accounts/register')
    else:
        form = RegistrationForm()
        
    return render(request, 'registration/register.html', {'form': form})

def borrow_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
		    
            book_instance.borrower = request.user
            book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=1)
            book_instance.status = 'r'
            book_instance.save()
            return HttpResponseRedirect('/catalog/books')

    context = {
       'book_instance': book_instance,
    }

    return render(request, 'catalog/book_detail.html', context)

def borrow_book_faculty(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
		    
            book_instance.borrower = request.user
            book_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=4)
            book_instance.status = 'r'
            book_instance.save()
            return HttpResponseRedirect('/catalog/books')

    context = {
       'book_instance': book_instance,
    }

    return render(request, 'catalog/book_detail.html', context)

def borrow_room(request, pk):
    room_instance = get_object_or_404(RoomInstance, pk=pk)
    if request.method == 'POST':
        if request.user.is_authenticated:
            room_instance.borrower = request.user
            room_instance.due_back = datetime.date.today() + datetime.timedelta(weeks=3)
            room_instance.status = 'r'
            room_instance.save()
            return HttpResponseRedirect('/catalog/rooms')

    context = {
       'room_instance': room_instance,
    }

    return render(request, 'catalog/room_detail.html', context)

def usergroup(request):
    context = {'user': request.user,
               'groups': request.user.groups.all()}
    return render_to_response('book_detail.html', context,
                              context_instance=RequestContext(request))