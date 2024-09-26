from rest_framework import serializers
from .models import Library, Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'description', 'file', 'created_at', 'library']

class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'address']

class LibraryWithBooksSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Library
        fields = ['id', 'address', 'books']
