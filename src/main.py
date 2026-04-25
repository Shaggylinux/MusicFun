import flet      as ft
import yt_dlp    as yt
import Alert     as Al
import Config    as co
import os

def main(page : ft.Page):
    ruta = co.leer("Path")
    
    def clean():
        Image.src               = "NoImage.png"
        DownloadButton.content  = "Search"
        DownloadText.value      = "Title : None"
        DurationText.value      = "Duration : --:--"
        DownloadButton.disabled = False
        DownloadButton.icon     = ft.Icons.SEARCH_OUTLINED
        entry.value             = ""
        DownloadButton.on_click = search
        page.update()

    if not ruta:
        if page.platform == ft.PagePlatform.ANDROID:
            ruta = "/storage/emulated/0/Download"
        else:
            ruta = '$HOME/MusicFun'
        co.editar("Path", ruta)
    
    async def choosepath():
        nonlocal ruta
        selector = ft.FilePicker()
        save = await selector.get_directory_path()
        if save:
            co.editar("Path", save)
            ruta           = save
            PathText.value = f"Path : {ruta}"
            PathText.update()
            page.update()

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

    def viewdownload(e):
        url = entry.value
        nombre = videoinfo(entry.value)
        ruta_completa = "".join(ruta) + "/" + nombre[0] + ".m4a"
        
        DownloadButton.content = "Downloading..."
        DownloadButton.disabled = True
        page.update()

        def rundownload():
            ydl_opts = {
                "format"              : "bestaudio[ext=m4a]",
                "outtmpl"             : f"{ruta}/%(title)s.%(ext)s",
                "fixup"               : "never",
                "nopart"              : True,
                "prefer_ffmpeg"       : False,
                "external_downloader" : None
            }
            if os.path.exists(ruta_completa):
                    clean()
                    page.show_dialog(Al.Alerta.alerta(page, True, "Error", "You have this music."))
                    page.update()
            else:
                with yt.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    clean()
                    page.show_dialog(Al.Alerta.alerta(page, True, "Complete", "Download complete."))
                    DownloadText.remo
                    page.update()

        page.run_thread(rundownload)

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
            DownloadButton.icon = ft.Icons.DOWNLOAD
            page.update()

    Image          = ft.Image(src = "NoImage.png", width = 256, height = 256)
    entry          = ft.TextField(multiline = True)
    DownloadText   = ft.Text("Title : None")
    DurationText   = ft.Text("Duration : --:--")
    DownloadButton = ft.Button("Search", icon=ft.Icons.SEARCH_OUTLINED, on_click = search)
    ButtonChoose   = ft.Button("Choose directory", icon=ft.Icons.FOLDER_OUTLINED, on_click = choosepath)
    PathText       = ft.Text(f"Path : {co.leer("Path")}")

    if co.leer("Aceptar") == 0:
        page.show_dialog(Al.Alerta.update(page, True))

    page.controls.append(Image)
    page.controls.append(entry)
    page.controls.append(DownloadText)
    page.controls.append(DurationText)
    page.controls.append(DownloadButton)
    page.controls.append(ButtonChoose)
    page.controls.append(PathText)

ft.run(main)