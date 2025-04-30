from django.contrib import admin
from core.models import Course
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name','description','price','teacher','created_at','updated_at')
    search_fields = ('name',)
    ordering = ('name',)
    date_hierarchy = 'created_at'