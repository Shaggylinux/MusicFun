import flet   as ft
import Config as co

class Alerta:
    def __init__(self : ft.Page, modal : bool, title : str, content : str):
        self.modal   = modal
        self.title   = title
        self.content = content

    def alerta(self : ft.Page, modal : bool, title : str, content : str):
        return ft.AlertDialog (
            modal   = modal,
            title   = ft.Text(title),
            content = ft.Text(content),
            actions = [
                ft.TextButton("No", on_click = lambda e: ft.Page.pop_dialog(self)),
                ft.TextButton("No", on_click = lambda e: ft.Page.pop_dialog(self)),
                ft.TextButton("No", on_click = lambda e: ft.Page.pop_dialog(self))
                ],
            actions_alignment = ft.MainAxisAlignment.END
        )
        self.update()
    
    def update(self : ft.Page, modal : bool):
        def cambiar(e):
            co.editar("Aceptar")
            ft.Page.pop_dialog(self)
            self.update()
        
        return ft.AlertDialog (
            modal   = modal,
            title   = ft.Text(f"Version : {co.leer("Version")}"),
            content = ft.Text("\n".join(co.leer("Changelog"))),
            actions = [ ft.TextButton("Ok",  on_click = cambiar) ],
            actions_alignment = ft.MainAxisAlignment.END
        )
        self.update()