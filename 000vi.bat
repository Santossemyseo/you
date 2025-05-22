@echo off
setlocal enabledelayedexpansion

rem Ruta de yt-dlp
set YTDLP="C:\Users\Sahob\yt-dlp.exe"
set FFMPEG="C:\Program Files\ffmpeg-7.1-essentials_build\bin"

rem Archivo de entrada con URLs
set INPUT_FILE=111vid.txt

rem Archivo de salida con nombres y URLs
set OUTPUT_FILE=descargas.txt

rem Limpiar el archivo de salida antes de empezar
echo. > %OUTPUT_FILE%

rem Descargar en la mejor calidad posible (video+audio)
for /f "delims=" %%i in (%INPUT_FILE%) do (
    echo Descargando: %%i
    %YTDLP% -f "bv*[ext=mp4]+ba[ext=m4a]/bestaudio/best" --merge-output-format mp4 --ffmpeg-location %FFMPEG% -o "%%(title)s.%%(ext)s" "%%i"

    rem Obtener el nombre del archivo descargado
    for /f "delims=" %%A in ('%YTDLP% --get-filename -o "%%(title)s.%%(ext)s" "%%i"') do (
        echo %%i - %%A >> %OUTPUT_FILE%
    )
)

echo Descargas completadas. Revisa %OUTPUT_FILE%
pause
