from django.contrib import admin
from reviews.models import Review
# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("course", "student", "rating", "comment", "created_on")
    list_filter = ("course__title", "student__first_name", "rating", "comment", "created_on")
    search_fields = ("course__title", "student__first_name", "rating", "comment", "created_on")