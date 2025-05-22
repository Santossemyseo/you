import yt_dlp
import json
from collections import defaultdict

def get_full_video_info(video_url):
    ydl_opts = {'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            return ydl.extract_info(video_url, download=False)
        except Exception as e:
            print(f"Error al extraer info de {video_url}: {e}")
            return None

def scrape_youtube(query, max_results=20):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'default_search': 'ytsearch',
        'dump_single_json': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(query, download=False)
    
    return result.get('entries', [])[:max_results] if result else []

def filter_creative_commons(videos):
    cc_videos = []
    non_cc_videos = []
    channel_counts = defaultdict(int)

    for video in videos:
        video_url = f"https://www.youtube.com/watch?v={video.get('id')}"
        full_info = get_full_video_info(video_url)
        if not full_info:
            continue
        
        title = full_info.get('title', 'No Title')
        description = full_info.get('description', '').lower()
        channel = full_info.get('channel', 'Unknown')
        license_type = full_info.get('license', '').lower()
        
        # Búsqueda de Creative Commons por metadato o descripción
        if 'creative commons' in license_type or \
           'creative commons' in description or \
           'reuse allowed' in description or \
           'cc' in description:
            cc_videos.append({'url': video_url, 'title': title, 'channel': channel})
            channel_counts[channel] += 1
        else:
            non_cc_videos.append({'url': video_url, 'title': title, 'channel': channel})
    
    return cc_videos, non_cc_videos, channel_counts


def save_results(cc_videos, non_cc_videos, channel_counts):
    with open('cc_videos.json', 'w', encoding='utf-8') as f:
        json.dump(cc_videos, f, indent=4, ensure_ascii=False)
    
    with open('non_cc_videos.json', 'w', encoding='utf-8') as f:
        json.dump(non_cc_videos, f, indent=4, ensure_ascii=False)
    
    with open('channel_summary.json', 'w', encoding='utf-8') as f:
        json.dump(channel_counts, f, indent=4, ensure_ascii=False)

def main():
    query = input("Introduce la temática para buscar en YouTube: ")
    videos = scrape_youtube(query, max_results=20)
    
    cc_videos, non_cc_videos, channel_counts = filter_creative_commons(videos)
    save_results(cc_videos, non_cc_videos, channel_counts)
    
    print(f"Se encontraron {len(cc_videos)} videos con licencia Creative Commons.")
    print(f"Resumen por canal guardado en 'channel_summary.json'.")
    print(f"Videos Creative Commons guardados en 'cc_videos.json'.")
    print(f"Videos sin Creative Commons guardados en 'non_cc_videos.json'.")

if __name__ == "__main__":
    main()
