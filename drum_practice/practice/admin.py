from django.contrib import admin
from .models import Song, Sheet, PageTiming

class PageTimingInline(admin.TabularInline):
    model = PageTiming
    extra = 1

class SheetInline(admin.StackedInline):
    model = Sheet
    extra = 0

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'duration', 'created_at']
    list_filter = ['created_at', 'artist']
    search_fields = ['title', 'artist']
    inlines = [SheetInline]

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ['song', 'total_pages', 'created_at']
    list_filter = ['created_at', 'total_pages']
    inlines = [PageTimingInline]

@admin.register(PageTiming)
class PageTimingAdmin(admin.ModelAdmin):
    list_display = ['sheet', 'page_number', 'start_time']
    list_filter = ['sheet']
    ordering = ['sheet', 'page_number']
