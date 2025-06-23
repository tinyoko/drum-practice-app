from django.db import models
import os

class Song(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200, blank=True)
    audio_file = models.FileField(upload_to='audio/')
    duration = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} - {self.artist}" if self.artist else self.title
    
    def get_audio_filename(self):
        return os.path.basename(self.audio_file.name)

class Sheet(models.Model):
    song = models.OneToOneField(Song, on_delete=models.CASCADE, related_name='sheet')
    pdf_file = models.FileField(upload_to='sheets/')
    total_pages = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Sheet for {self.song.title}"
    
    def get_pdf_filename(self):
        return os.path.basename(self.pdf_file.name)

class PageTiming(models.Model):
    sheet = models.ForeignKey(Sheet, on_delete=models.CASCADE, related_name='page_timings')
    page_number = models.IntegerField()
    start_time = models.FloatField()
    
    class Meta:
        ordering = ['page_number']
        unique_together = ['sheet', 'page_number']
    
    def __str__(self):
        return f"Page {self.page_number} at {self.start_time}s"
