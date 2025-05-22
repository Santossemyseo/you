#valida desde youtube

import yt_dlp

# Opciones para la búsqueda (ytsearch)
YDL_SEARCH_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'extract_flat': True,    # sólo metadatos básicos
    'default_search': 'ytsearch',
    'noplaylist': True,
    'socket_timeout': 10,    # timeout HTTP en segundos
}

# Opciones para extraer info de cada video
YDL_INFO_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'skip_download': True,   # no descarga el vídeo
    'socket_timeout': 10,
}

def get_video_urls(query, max_results=20):
    """Busca videos en YouTube por query y devuelve lista de URLs."""
    urls = []
    with yt_dlp.YoutubeDL(YDL_SEARCH_OPTS) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            entries = result.get('entries') or []
            for entry in entries:
                vid = entry.get('url')
                if not vid:
                    continue
                # Asegura URL completa
                if not vid.startswith('http'):
                    vid = f"https://www.youtube.com/watch?v={vid}"
                urls.append(vid)
        except Exception as e:
            print(f"[ERROR] al buscar '{query}': {e}")
    return urls

def filter_cc_only(urls):
    """
    Filtra y devuelve solo las URLs con licencia 'Creative Commons'.
    """
    cc_urls = []
    with yt_dlp.YoutubeDL(YDL_INFO_OPTS) as ydl:
        for url in urls:
            try:
                info = ydl.extract_info(url, download=False)
                lic = info.get('license') or ''
                if 'Creative Commons' in lic:
                    cc_urls.append(url)
            except Exception as e:
                # Ignoramos errores y no guardamos estas URLs
                print(f"[WARN] no pude procesar {url}: {e}")
    return cc_urls

def save_urls_to_file(urls, filename):
    """Guarda la lista de URLs en un archivo de texto."""
    with open(filename, 'w', encoding='utf-8') as f:
        for u in urls:
            f.write(u + '\n')

def main():
    query = input("Introduce la temática para buscar en YouTube: ")
    urls = get_video_urls(query, max_results=20)
    print(f"Se obtuvieron {len(urls)} URLs.")

    cc_urls = filter_cc_only(urls)
    save_urls_to_file(cc_urls, 'cc_videos.txt')

    print(f"Videos CC: {len(cc_urls)} → cc_videos.txt")

if __name__ == '__main__':
    main()
