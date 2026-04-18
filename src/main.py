import flet      as ft
import yt_dlp    as yt
import threading as th

def main(page : ft.Page):
    ruta = ""
    async def choosepath():
        nonlocal ruta
        selector       = ft.FilePicker()
        save           = await selector.get_directory_path()
        ruta           = save
        PathText.value = f"Path : {ruta}"
        PathText.update()

    def videoinfo(url):
        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt.YoutubeDL(ydl_opts) as ydl:
            info      = ydl.extract_info(url, download = False)
            title     = info.get('title', 'No found')
            miniatura = info.get('thumbnail', 'No found')
            duracion  = info.get('duration', 0)
            return title, miniatura, duracion

    def viewdownload():
        url = entry.value
        def rundownload():
            nonlocal ruta
            if ruta == "":
                if page.platform == ft.PagePlatform.ANDROID:
                    ruta = "/storage/emulated/0/Download/"
                else:
                    ruta = "Downloads/"
            ydl_opts = {
                        'format': 'bestaudio[ext=m4a]',
                        'outtmpl': f'{ruta}/%(title)s.%(ext)s',
                        'fixup': 'never',
                        'nopart': True,
                        'prefer_ffmpeg': False,
                        'external_downloader': None
                    }
            with yt.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        th.Thread(target = rundownload, daemon = True).start()

    def search():
        if (entry.value == ""):
            DownloadText.value = "Title : Error"
        else:
            nombre, miniatura, duracion  = videoinfo(entry.value)
            Image.src                    = f"{miniatura}"
            DownloadText.value           = f"Title : {nombre}"
            DurationText.value           = f"Duration : {duracion // 60}:{duracion % 60}"
            DownloadButton.content       = "Download"
            DownloadButton.on_click      = viewdownload
            page.update()

    Image          = ft.Image(src = "NoImage.png", width = 256, height = 256)
    entry          = ft.TextField(multiline = True)
    DownloadText   = ft.Text("Title : None")
    DurationText   = ft.Text("Duration : --:--")
    DownloadButton = ft.Button("Search", on_click = search)
    ButtonChoose   = ft.Button("Choose directory", on_click = choosepath)
    PathText       = ft.Text("Path : ")

    page.controls.append(Image)
    page.controls.append(entry)
    page.controls.append(DownloadText)
    page.controls.append(DurationText)
    page.controls.append(DownloadButton)
    page.controls.append(ButtonChoose)
    page.controls.append(PathText)

ft.run(main)