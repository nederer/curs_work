from django.contrib import admin
from .models import User, Assignment

# Register your models here.

admin.site.register(User)


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("master", "slave", "description")
