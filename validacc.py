import yt_dlp
import time
import random
import subprocess

YDL_OPTS = {
    'quiet': True,
    'no_warnings': True,
    'skip_download': True,
    'socket_timeout': 10,
}


def filter_cc_from_file(input_path='url.txt', output_path='creat.txt', block_size=5):
    # Leer todas las líneas
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    # Filtrar URLs que no estén marcadas
    pending_urls = []
    for i, line in enumerate(lines):
        if not line.endswith('*a') and not line.endswith('*validado'):
            lines[i] = line + ' *a'
            pending_urls.append(line.strip())

    # Guardar cambios de marcación "*a"
    with open(input_path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + '\n')

    with yt_dlp.YoutubeDL(YDL_OPTS) as ydl:
        for i in range(0, len(pending_urls), block_size):
            block = pending_urls[i:i + block_size]

            for url in block:
                try:
                    info = ydl.extract_info(url, download=False)
                    lic = info.get('license') or ''

                    if 'Creative Commons' in lic:
                        with open(output_path, 'a', encoding='utf-8') as out:
                            out.write(url + '\n')
                        print(f"✅ CC: {url}")

                        # Reemplazar *a por *validado
                        for j in range(len(lines)):
                            if lines[j].startswith(url) and lines[j].endswith('*a'):
                                lines[j] = url + ' *validado'
                                break
                    else:
                        print(f"⛔️ No CC: {url}")

                except Exception:
                    pass  # Silenciar errores

                time.sleep(random.uniform(2, 3))  # Delay aleatorio

            # Guardar el archivo actualizado después de cada bloque
            with open(input_path, 'w', encoding='utf-8') as f:
                for line in lines:
                    f.write(line + '\n')

            # Ejecutar scripts externos en nueva consola
            ejecutar_en_nueva_ventana('1.py', tipo='py')
            ejecutar_en_nueva_ventana('1.bat', tipo='bat')

    print("🟢 Proceso completado.")


def ejecutar_en_nueva_ventana(archivo, tipo='py'):
    if tipo == 'py':
        comando = f'start powershell -NoExit -Command "python \'{archivo}\'"'
    elif tipo == 'bat':
        comando = f'start cmd /k "{archivo}"'
    else:
        return
    subprocess.call(comando, shell=True)


if __name__ == '__main__':
    filter_cc_from_file()
