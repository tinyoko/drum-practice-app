from django import forms
from .models import Song, Sheet

class SongUploadForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artist', 'audio_file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '楽曲タイトル'}),
            'artist': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'アーティスト名'}),
            'audio_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'audio/mp3'}),
        }

class SheetUploadForm(forms.ModelForm):
    class Meta:
        model = Sheet
        fields = ['pdf_file', 'total_pages']
        widgets = {
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': 'application/pdf'}),
            'total_pages': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'value': 1}),
        }