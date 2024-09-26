from django.contrib import admin
from .models import Library, Book

admin.site.register(Book)
admin.site.register(Library)

