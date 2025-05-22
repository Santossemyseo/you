@echo off
setlocal enabledelayedexpansion

rem Ruta de yt-dlp y FFMPEG
set YTDLP="C:\Users\Sahob\yt-dlp.exe"
set FFMPEG="C:\Program Files\ffmpeg-7.1-essentials_build\bin"

rem Archivo de entrada con URLs
set INPUT_FILE=111vid.txt

rem Archivo de salida con nombres y URLs
set OUTPUT_FILE=descargas.txt

rem Limpiar el archivo de salida antes de empezar
echo. > %OUTPUT_FILE%

rem Menú interactivo
cls
echo ==========================================
echo       SELECCIONA UNA OPCIÓN DE DESCARGA
echo ==========================================
echo [1] Descargar solo el mejor AUDIO (MP3)
echo [2] Descargar solo el mejor VIDEO (MP4 sin audio)
echo [3] Descargar el mejor VIDEO + AUDIO (MP4 completo)
echo ==========================================
set /p choice="Elige una opción (1-3): "

rem Definir formato de descarga según elección
if "%choice%"=="1" (
    set FORMAT=bestaudio
    set EXTENSION=mp3
    set MERGE_OPTION=
)
if "%choice%"=="2" (
    set FORMAT=bestvideo
    set EXTENSION=mp4
    set MERGE_OPTION=
)
if "%choice%"=="3" (
    set FORMAT="bv*+ba/best"
    set EXTENSION=mp4
    set MERGE_OPTION=--merge-output-format mp4
)

rem Validar entrada
if "%choice%" NEQ "1" if "%choice%" NEQ "2" if "%choice%" NEQ "3" (
    echo Opción no válida. Intenta de nuevo.
    pause
    exit /b
)

rem Descargar los archivos según la elección del usuario
for /f "delims=" %%i in (%INPUT_FILE%) do (
    echo Descargando: %%i

    rem Descargar el archivo seleccionado
    %YTDLP% -f %FORMAT% %MERGE_OPTION% --ffmpeg-location %FFMPEG% -o "%%(title)s.%%(ext)s" "%%i"

    rem Obtener el nombre del archivo descargado
    for /f "delims=" %%A in ('%YTDLP% --get-filename -o "%%(title)s.%EXTENSION%" "%%i"') do (
        echo %%i - %%A >> %OUTPUT_FILE%
    )
)

echo ==========================================
echo Descargas completadas. Revisa %OUTPUT_FILE%
echo ==========================================
pause
