import flet   as ft
import yt_dlp as yt
import platform
import threading

def main(page : ft.Page):
    def videoname(url):
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }
        with yt.YoutubeDL(ydl_opts) as ydl:
            info      = ydl.extract_info(url, download=False)
            title     = info.get('title', 'No encontrado')
            miniatura = info.get('thumbnail', 'No encontrado') 
            return title, miniatura
    
    def videdownloader():
        url = entry.value
        if page.platform == ft.PagePlatform.ANDROID:
            ydl_opts = {
                        'format': 'bestaudio/best',
                        'outtmpl': '/storage/emulated/0/Download/%(title)s.%(ext)s',
                        'fixup': 'never',
                        'nopart': True,
                        'prefer_ffmpeg': False,
                        'external_downloader': None
                    }
            with yt.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        else:
            ydl_opts = {
                'postprocessors':[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
                }],
                    'format':  'bestaudio/best',
                    'outtmpl': 'Downloads/%(title)s.%(ext)s',
                }
            with yt.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        threading.Thread(target=videdownloader, daemon=True).start()

    def search(e):
        if (entry.value == ""):
            DownloadText.value = "Title : Error"
        else:
            nombre, miniatura  = videoname(entry.value)
            Image.src          = f"{miniatura}"
            DownloadText.value = f"Title : {nombre}"
            DownloadButton.content  = "Download"
            DownloadButton.on_click = videdownloader
            DownloadButton.update()
            Image.update()
            DownloadText.update()

    entry = ft.TextField(multiline = True)
    DownloadText   = ft.Text("Title : ")
    Image          = ft.Image(src="NoImage.png", width=256, height=256)
    DownloadButton = ft.Button("Search", on_click = search)
    
    page.controls.append(Image)
    page.controls.append(entry)
    page.controls.append(DownloadText)
    page.controls.append(DownloadButton)

ft.run(main)