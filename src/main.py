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
            info      = ydl.extract_info(url, download = False)
            title     = info.get('title', 'No encontrado')
            miniatura = info.get('thumbnail', 'No encontrado')
            duracion = info.get('duration', 0)
            return title, miniatura, duracion
    
    def videdownloader():
        url = entry.value
        ruta = ""
        if page.platform == ft.PagePlatform.ANDROID:
            ruta = "/storage/emulated/0/Download/"
        else:
            ruta = "Downloads/"
        ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{ruta}%(title)s.%(ext)s',
                    'fixup': 'never',
                    'nopart': True,
                    'prefer_ffmpeg': False,
                    'external_downloader': None
                }
        with yt.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        threading.Thread(target=videdownloader, daemon=True).start()

    def search(e):
        if (entry.value == ""):
            DownloadText.value = "Title : Error"
        else:
            nombre, miniatura, duracion  = videoname(entry.value)
            Image.src          = f"{miniatura}"
            DownloadText.value = f"Title : {nombre}"
            DurationText.value = f"Duration : {duracion // 60}:{duracion % 60}"
            DownloadButton.content  = "Download"
            DownloadButton.on_click = videdownloader
            DownloadButton.update()
            Image.update()
            DownloadText.update()
            DurationText.update()

    entry          = ft.TextField(multiline = True)
    DownloadText   = ft.Text("Title : None")
    Image          = ft.Image(src = "NoImage.png", width = 256, height = 256)
    DownloadButton = ft.Button("Search", on_click = search)
    DurationText   = ft.Text("Duration : 0:00")
    
    page.controls.append(Image)
    page.controls.append(entry)
    page.controls.append(DownloadText)
    page.controls.append(DurationText)
    page.controls.append(DownloadButton)

ft.run(main)