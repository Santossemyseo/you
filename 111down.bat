@echo off

rem "C:\Users\Sahob\yt-dlp.exe" -a vid.txt

rem solo audio el mejor 
"C:\Users\Sahob\yt-dlp.exe" -a 111vid.txt -f "bestaudio" --extract-audio --audio-format mp3 --ffmpeg-location "C:\Program Files\ffmpeg-7.1-essentials_build\bin"

rem la mejor caliudad
rem "C:\Users\Sahob\yt-dlp.exe" -a vid.txt -f "bestvideo+bestaudio/best"

pause
