from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Song, Sheet, PageTiming
from .forms import SongUploadForm, SheetUploadForm

def index(request):
    songs = Song.objects.all()
    return render(request, 'practice/index.html', {'songs': songs})

def upload_song(request):
    if request.method == 'POST':
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            song = form.save()
            messages.success(request, f'楽曲「{song.title}」をアップロードしました。')
            return redirect('practice:upload_sheet', song_id=song.id)
    else:
        form = SongUploadForm()
    return render(request, 'practice/upload_song.html', {'form': form})

def upload_sheet(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    
    if request.method == 'POST':
        form = SheetUploadForm(request.POST, request.FILES)
        if form.is_valid():
            sheet = form.save(commit=False)
            sheet.song = song
            sheet.save()
            messages.success(request, f'楽譜をアップロードしました。')
            return redirect('practice:song_detail', song_id=song.id)
    else:
        form = SheetUploadForm()
    
    return render(request, 'practice/upload_sheet.html', {'form': form, 'song': song})

def song_detail(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    return render(request, 'practice/song_detail.html', {'song': song})

def set_page_timing(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    sheet = get_object_or_404(Sheet, song=song)
    
    if request.method == 'POST':
        # タイミングデータの保存
        timing_data = request.POST.getlist('timing')
        sheet.page_timings.all().delete()  # 既存のタイミングを削除
        
        for i, timing in enumerate(timing_data):
            if timing:  # 空でない場合のみ保存
                try:
                    timing_float = float(timing)
                    sheet.page_timings.create(
                        page_number=i + 1,
                        start_time=timing_float
                    )
                except ValueError:
                    pass  # 無効な値はスキップ
        
        messages.success(request, 'ページタイミングを設定しました。')
        return redirect('practice:song_detail', song_id=song.id)
    
    # 既存のタイミングデータを取得
    existing_timings = {}
    for timing in sheet.page_timings.all():
        existing_timings[timing.page_number] = timing.start_time
    
    return render(request, 'practice/set_page_timing.html', {
        'song': song,
        'sheet': sheet,
        'existing_timings': existing_timings
    })

def get_page_timings(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    try:
        sheet = song.sheet
        timings = list(sheet.page_timings.values('page_number', 'start_time'))
        return JsonResponse({'timings': timings})
    except Sheet.DoesNotExist:
        return JsonResponse({'timings': []})
