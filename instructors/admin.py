from django.contrib import admin
from instructors.models import Instructor
# Register your models here.

# Create your models here.
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user', 'bio')
    list_filter = ('user', 'bio')