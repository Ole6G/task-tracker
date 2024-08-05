from django.contrib import admin
from .models import Task, Tag


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'deadline', 'completed', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('completed', 'tags')
    ordering = ('title', 'deadline')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
