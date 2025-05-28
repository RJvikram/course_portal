from django.contrib import admin
from courses.models import Courses
# Register your models here.

@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display=("title", "description", "instructor", "created_on")
    list_filter=("title", "description", "instructor", "created_on")
    search_fields=("title", "description", "instructor", "created_on")
