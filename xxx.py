import yt_dlp

def get_video_urls(query, max_results=10):
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,  # No analiza videos profundamente
        'default_search': 'ytsearch',
        'noplaylist': True
    }

    urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(f"ytsearch{max_results}:{query}", download=False)
            entries = result.get('entries', [])
            for entry in entries:
                video_url = entry.get('url')
                if video_url:
                    # Aseguramos que sea URL completa
                    if not video_url.startswith('http'):
                        video_url = f"https://www.youtube.com/watch?v={video_url}"
                    urls.append(video_url)
        except Exception as e:
            print(f"Error al obtener resultados: {e}")

    return urls

def save_urls_to_file(urls, filename='urls.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        for url in urls:
            f.write(url + '\n')

def main():
    query = input("Introduce la temática para buscar en YouTube: ")
    urls = get_video_urls(query)
    save_urls_to_file(urls)
    print(f"Se guardaron {len(urls)} URLs en 'urls.txt'.")

if __name__ == "__main__":
    main()
