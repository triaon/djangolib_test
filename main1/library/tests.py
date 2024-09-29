from django.test import TestCase
from django.urls import reverse
from .models import Library, Book
from rest_framework.test import APITestCase
from rest_framework import status
from .serializers import BookSerializer
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

class LibraryModelTest(TestCase):
    def setUp(self):
        self.library = Library.objects.create(address="test")

    def test_library_creation(self):
        self.assertEqual(self.library.address, "test")
        self.assertIsInstance(self.library, Library)

class BookModelTest(TestCase):
    def setUp(self):
        self.library = Library.objects.create(address="test")
        self.book = Book.objects.create(
            title="test_title",
            description="test_description",
            file="books/test_file.pdf",
            library=self.library
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "test_title")
        self.assertEqual(self.book.library, self.library)
        self.assertIsInstance(self.book, Book)

class BookSerializerTest(TestCase):
    def setUp(self):
        self.library = Library.objects.create(address="test")
        self.book_data = {
            "title": "test_title",
            "description": "test_description",
            "file": SimpleUploadedFile("test_file.pdf", b"file_content", content_type="application/pdf"),
            "library": self.library.id
        }

    def test_book_serialization(self):
        book = Book.objects.create(
            title=self.book_data['title'],
            description=self.book_data['description'],
            file=self.book_data['file'],
            library=self.library
        )
        serializer = BookSerializer(book)
        expected_data = {
            "id": book.id,
            "title": "test_title",
            "description": "test_description",
            "file": "books/file.pdf",
            "created_at": book.created_at,
            "library": self.library.id
        }
        self.assertEqual(serializer.data['title'], expected_data['title'])

    def test_book_deserialization(self):
        serializer = BookSerializer(data=self.book_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        book = serializer.save()
        self.assertEqual(book.title, "test_title")

class BookAPITest(APITestCase):
    def setUp(self):
        self.library = Library.objects.create(address="test")
        self.book_data = {
            "title": "test_title",
            "description": "test_description",
            "file": SimpleUploadedFile("file.pdf", b"file_content", content_type="application/pdf"),
            "library": self.library.id
        }

    def test_create_book(self):
        url = reverse('book-list')
        response = self.client.post(url, self.book_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 1)
        self.assertEqual(Book.objects.get().title, "test_title")


class LibraryAPITest(APITestCase):
    def setUp(self):
        self.library = Library.objects.create(address="test")

    def test_get_library_list(self):
        url = reverse('library-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_library(self):
        url = reverse('library-list')
        data = {"address": "test"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_library = Library.objects.latest('id')
        self.assertEqual(created_library.address, "test")

