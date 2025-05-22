#valida desde un archivo en local

import yt_dlp

# Opciones para extraer solo metadatos sin descargar
YDL_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'skip_download': True,
    'socket_timeout': 10,
}

def filter_cc_from_file(input_path='url.txt', output_path='creat.txt'):
    # Leer todas las URLs no vacías
    with open(input_path, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    cc_urls = []
    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        for url in urls:
            try:
                info = ydl.extract_info(url, download=False)
                lic = info.get('license') or ''
                if 'Creative Commons' in lic:
                    cc_urls.append(url)
            except Exception as e:
                # Si hay error, lo reportamos y seguimos
                print(f"[WARN] no pude procesar {url}: {e}")

    # Guardar solo las URLs CC en creat.txt
    with open(output_path, 'a', encoding='utf-8') as f:
        for u in cc_urls:
            f.write(u + '\n')

    print(f"Se han encontrado {len(cc_urls)} videos CC. Guardados en '{output_path}'")

if __name__ == '__main__':
    filter_cc_from_file('url.txt', 'creat.txt')
