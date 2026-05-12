import flet   as ft
import yt_dlp as yt
import Alert  as Al
import Config as co
import os

def main(page : ft.Page):
    
    def OneDownload():
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
                DownloadButton.icon          = ft.Icons.DOWNLOAD
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
        
        return ft.Column(
            controls=[
                Image,
                entry,
                DownloadText,
                DurationText,
                DownloadButton,
                ButtonChoose,
                PathText
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
            expand=True
        )

    def PlayListDownload():
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
                'skip_download': True,
                "extract_flat" : "in_playlist"
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
                        "format": "bestaudio[ext=m4a]/best[ext=mp4]/best",
                        "outtmpl": f"{ruta}/%(playlist_title)s/%(title)s.%(ext)s" if "list=" in url else f"{ruta}/%(title)s.%(ext)s",
                        "noplaylist": False,
                        "ignoreerrors": True,
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
                        page.update()

            page.run_thread(rundownload)

        def search(e):
            url = entry.value
            if (entry.value == ""):
                DownloadText.value = "Title : Error"
                page.update()
            else:
                yt_opts = {
                    "extract_flat" : True,
                    "quiet" : True
                }
                lista = ft.Column(expand=True, scroll=ft.ScrollMode.ALWAYS)
                page.add(lista)
                
                with yt.YoutubeDL(yt_opts) as f:
                    info = f.extract_info(url, download=False)
                    for entrada in info["entries"]:
                        titulo = entrada.get("title")
                        miniatura = entrada.get("thumbnail", "No found")
                        u = entrada.get("url")
                        lista.controls.extend([
                                ft.Image(src = miniatura, width = 200, height = 200),
                                ft.Text(f"Title : {titulo}"),
                                ft.Text(f"url : {u}"),
                                ft.Button("Download"),
                                ft.Divider()
                                ]
                            )
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
        

        return ft.Column(
            controls=[
                entry,
                DownloadButton,
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )
        
    navbar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.PLAY_ARROW),
            ft.NavigationBarDestination(icon=ft.Icons.PLAYLIST_PLAY)
        ],
        on_change=  lambda e : route_change(e)
    )
    page.navigation_bar = navbar
    
    
    def route_change(e=None):
        page.views.clear()
        match navbar.selected_index:
            case 0:
                page.views.append(
                    ft.View(
                        route="/",
                        controls=[
                                ft.SafeArea(
                                    OneDownload()
                                )
                            ],
                        navigation_bar = navbar
                    )
                )
            case 1:
                page.views.append(
                    ft.View(
                        route="/playlist",
                        controls=[
                                ft.SafeArea(
                                    PlayListDownload()
                                )
                            ],
                        navigation_bar = navbar
                    )
                )
        page.update()
    
    async def view_pop(e):
        if e.view is not None:
            print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    
    route_change()

ft.run(main)