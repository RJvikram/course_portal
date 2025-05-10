from django.contrib import admin
from enrollment.models import Enrollment 
# Register your models here.

@admin.register(Enrollment )
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_on", "completed")
    list_filter = ("student", "course", "enrolled_on", "completed")
    search_fields = ("student", "course", "enrolled_on", "completed")
    