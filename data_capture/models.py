from django.db import models
from django.conf import settings


class DataSource(models.Model):
    """Model to track data sources"""
    SOURCE_TYPES = [
        ('pdf', 'PDF'),
        ('excel', 'Excel'),
        ('image', 'Image'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]

    # Uses custom user model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    source_type = models.CharField(max_length=20, choices=SOURCE_TYPES)
    file_name = models.CharField(max_length=255, null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source_type} - {self.user.username}"


class ExtractedData(models.Model):
    """
    Store extracted data linked to a DataSource and User
    (this replaces saving to MongoDB)
    """
    source = models.ForeignKey(DataSource, on_delete=models.CASCADE, related_name='extracted_items')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.TextField()  # you can store JSON as text here
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ExtractedData #{self.id} for {self.source}"
