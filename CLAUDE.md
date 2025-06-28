# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django-based drum practice application that synchronizes audio playback with sheet music (PDF) viewing. The app allows users to upload songs and drum sheets, set timing markers for automatic page turning, and practice along with synchronized audio and visual guidance.

## Key Architecture

- **Django Project**: `drum_practice/` - Main Django project directory
- **Core App**: `practice/` - Contains all application logic
- **Models**: 
  - `Song` - Audio files with metadata
  - `Sheet` - PDF drum sheets linked to songs (OneToOne)
  - `PageTiming` - Timing markers for automatic page transitions
- **Media Storage**: `/media/audio/` for audio files, `/media/sheets/` for PDFs
- **Database**: SQLite (`db.sqlite3`)

## Development Setup

The project uses a virtual environment located at `drum_practice_env/` (outside the main project directory).

### Required Dependencies
```
Django==4.2.7
Pillow==10.1.0
python-decouple==3.8
```

### Environment Configuration
- Uses `python-decouple` for environment variables
- Requires `.env` file with `SECRET_KEY` and `DEBUG` settings
- Settings configured in `drum_practice/settings.py`

## Common Commands

```bash
# Activate virtual environment
source drum_practice_env/bin/activate

# Install dependencies
pip install -r drum_practice/requirements.txt

# Run development server
cd drum_practice && python manage.py runserver

# Apply database migrations
cd drum_practice && python manage.py migrate

# Create new migrations
cd drum_practice && python manage.py makemigrations

# Access Django admin
cd drum_practice && python manage.py createsuperuser

# Run tests
cd drum_practice && python manage.py test
```

## Application Flow

1. **Song Upload**: Users upload MP3 audio files via `upload_song` view
2. **Sheet Upload**: After song upload, users upload corresponding PDF drum sheets
3. **Timing Setup**: Users set page timing markers via `set_page_timing` view
4. **Practice Mode**: `song_detail` view provides synchronized audio playback with automatic PDF page turning

## Key Features

- **File Upload**: Audio (MP3) and PDF handling with Django's FileField
- **Timing Synchronization**: JavaScript-driven audio/PDF synchronization
- **Bootstrap UI**: Frontend styled with Bootstrap 5.1.3
- **Japanese Localization**: UI messages and labels in Japanese
- **AJAX API**: JSON endpoint for retrieving page timings (`get_page_timings`)

## WaveSurfer.js Audio Player

The application uses **WaveSurfer.js v7** for advanced audio playback with waveform visualization and region-based practice features.

### Implementation Details
- **Library**: WaveSurfer.js v7 with Regions plugin
- **Module System**: ES6 modules loaded via CDN
- **Integration**: `practice/templates/practice/song_detail.html`

### Audio Player Features
- **Waveform Visualization**: Visual representation of audio with customizable styling
- **Region Selection**: Mouse drag to select practice segments
- **Loop Playback**: Repeat selected regions for focused practice
- **Time Synchronization**: Maintains compatibility with PDF page timing

### Region Management
- **Manual Selection**: Drag on waveform to create regions
- **Button Controls**: "区間設定" for default region, "区間クリア" for removal
- **Visual Feedback**: Golden highlight for selected regions
- **Drag & Resize**: Interactive region boundaries

### Control Interface
- **Play/Pause/Reset**: Standard playback controls adapted for WaveSurfer
- **Region Playback**: "区間再生" plays only selected segment
- **Loop Toggle**: "ループ" enables/disables region looping
- **Time Display**: Current time and duration with monospace font

## Frontend Technologies

### JavaScript Libraries
- **WaveSurfer.js v7**: `https://unpkg.com/wavesurfer.js@7/dist/wavesurfer.esm.js`
- **Regions Plugin**: `https://unpkg.com/wavesurfer.js@7/dist/plugins/regions.esm.js`
- **PDF.js**: `https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js`
- **Bootstrap 5.1.3**: CSS framework for responsive design

### Module System
- Uses ES6 modules (`type="module"`) for WaveSurfer.js
- CDN-based library loading for easy maintenance
- No build process required for frontend dependencies

## Development Notes

### WaveSurfer.js Integration
```javascript
// Initialize with regions plugin
regionsPlugin = RegionsPlugin.create();
wavesurfer = WaveSurfer.create({
    container: '#waveform',
    plugins: [regionsPlugin]
});
```

### PDF Synchronization Compatibility
- WaveSurfer's `audioprocess` event replaces HTML5 audio's `timeupdate`
- Use `wavesurfer.getCurrentTime()` instead of `audioPlayer.currentTime`
- Maintains existing `checkAutoPageTurn()` function compatibility

### Region Loop Implementation
- Custom loop logic in `audioprocess` event handler
- Checks region boundaries and seeks to start when reaching end
- Visual feedback through button state changes

### Error Handling
- Graceful fallback when WaveSurfer fails to load
- Region validation before operations
- User alerts for invalid operations

## File Structure Notes

- Audio files stored in `media/audio/`
- PDF sheets stored in `media/sheets/`  
- Templates in `practice/templates/practice/`
- Static files served via Django's development server
- Database migrations in `practice/migrations/`
- **Main audio interface**: `practice/templates/practice/song_detail.html`