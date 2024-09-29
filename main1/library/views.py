from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import LibrarySerializer, BookSerializer, LibraryWithBooksSerializer
from .models import Library, Book

class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    @action(detail=True, methods=['get'])
    def books(self, request, pk=None):
        library = self.get_object()
        books = library.books.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
