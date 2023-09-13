import youtube_dl

def download_video(url):
    ydl_opts = {
        'quiet': True,  # Suppress console output from youtube_dl
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            return True
        except:
            return False

def extract_info(url):
    ydl_opts = {
        'quiet': True,  # Suppress console output from youtube_dl
        'extract_flat': True,  # Extract only essential video information
        'force_generic_extractor': True,  # Skip specific extractors for better compatibility
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            video_info = ydl.extract_info(url, download=False)
        except youtube_dl.DownloadError as e:
            print("DownloadError:", e)
            return None

        info = {
            'video_id': video_info.get('id', ''),
            'title': video_info.get('title', ''),
            'channel': video_info.get('uploader', ''),
            'view_count': video_info.get('view_count', 0),
            'duration': video_info.get('duration', 0),
        }

        return info


def get_duration_text(duration_s):
    seconds = duration_s % 60
    minutes = int((duration_s/60)%60)
    hours = int((duration_s/(60*60))%24)
    text = ''
    if hours > 0:
        text += f'{hours:02d}:{minutes:02d}:{seconds:02d}'
    else:
        text += f'{minutes:02d}:{seconds:02d}'
    return text
