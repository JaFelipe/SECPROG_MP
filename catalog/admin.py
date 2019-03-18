from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.

from catalog.models import Author, Genre, Book, BookInstance, Room , RoomInstance


#admin.site.register(Book)
#admin.site.register(Author)
admin.site.register(Genre)
#admin.site.register(BookInstance)

class User(admin.ModelAdmin):
     list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]

    
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)
#admin.site.register(Author, AuthorAdmin)

#@admin.register(Book)
#class BookAdmin(admin.ModelAdmin):
 #   list_display = ('title', 'author', 'display_genre')

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    
@admin.register(RoomInstance)
class RoomInstanceInline(admin.ModelAdmin):
    model = RoomInstance
    list_display = ('room' , 'room_code')
    
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    
    fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )