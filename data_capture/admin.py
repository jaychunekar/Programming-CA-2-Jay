from django.contrib import admin
from .models import DataSource, ExtractedData

admin.site.register(DataSource)
admin.site.register(ExtractedData)

