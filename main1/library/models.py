from django.db import models

class Library(models.Model):
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.address

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='books/')
    created_at = models.DateTimeField(auto_now_add=True)
    library = models.ForeignKey(Library, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
